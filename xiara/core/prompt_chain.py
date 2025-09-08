# xiara/core/prompt_chain.py
import os
import re
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from xiara.core.product_loader import load_all_products
from xiara.core.llm_config import llm
from xiara.core.vectorstore_loader import get_vectorstore
from xiara.core.user_profile_manager import get_user_profile, save_user_profile, UserProfile
from xiara.core.memory_manager import get_memory
from xiara.core.ambiguity_detector import AmbiguityDetector
import re
from xiara.core.memory_manager import get_last_query, set_last_query
from xiara.core.memory_manager import (
    get_memory,
    set_last_query,
    get_last_query,
    clear_last_query,
    cache_search_result,
    get_cached_result,
    clear_cached_result,
)
# Load env vars
load_dotenv()
DATA_PATH = os.getenv("DATA_PATH")
USE_RAG = os.getenv("USE_RAG", "true").lower() == "true"
ambiguity_detector = AmbiguityDetector()

# Helper: split multi-product queries
def split_multi_product_query(query: str):
    """
    Splits a query into sub-queries if multiple products are mentioned,
    and propagates shared constraints (budget, brand, etc.) to all parts.

    Example:
      "I want waterproof hiking boots under ₦20,000 and a backpack"
      -> ["I want waterproof hiking boots under ₦20,000",
          "I want a backpack under ₦20,000"]
    """
    # Normalize
    q = query.strip()

    # Detect budget/constraints
    budget_match = re.search(r"(under|below|less than)\s*₦?\s*[\d,]+", q, re.IGNORECASE)
    budget_text = budget_match.group(0) if budget_match else ""

    # Replace connectors with |
    connectors = [" and ", ",", " as well as ", " plus ", " together with "]
    q_lower = q.lower()
    for conn in connectors:
        q_lower = q_lower.replace(conn, "|")

    # Split parts
    parts = [p.strip().capitalize() for p in q_lower.split("|") if p.strip()]

    sub_queries = []
    for i, part in enumerate(parts):
        if not re.search(r"(buy|want|looking|need|search|recommend)", part, re.IGNORECASE):
            part = "I want " + part

        # If a budget/constraint exists in original query but not this part, add it
        if budget_text and budget_text.lower() not in part.lower():
            part = f"{part} {budget_text}"

        sub_queries.append(part)

    return sub_queries


# Load vectorstore if RAG enabled
if USE_RAG:
    documents = load_all_products(DATA_PATH)
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    VECTORSTORE_PATH = "xiara/core/faiss_index"

    if not os.path.exists(VECTORSTORE_PATH):
        vectorstore = FAISS.from_documents(docs, embedding_model)
        vectorstore.save_local(VECTORSTORE_PATH)
    else:
        vectorstore = get_vectorstore()

    if vectorstore is None:
        raise ValueError("Vectorstore could not be loaded. Please check initialization.")
    retriever = vectorstore.as_retriever()
else:
    retriever = None

# Prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are Xiara, a conversational and friendly AI shopping assistant for the Pasar marketplace.\n"
     "Understand user intent and respond naturally in multi-turn conversations.\n"
     "If query is ambiguous, ask for clarification.\n"
     "If query is clear, respond with useful product recommendations.\n"
     "Keep responses conversational, concise, and engaging."),
    ("human", "{question}")
])

def build_user_chain(user_id: str):
    memory = get_memory(session_id=user_id)
    if USE_RAG:
        return ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            memory=memory,
            return_source_documents=True,
            verbose=False
        )
    else:
        return LLMChain(llm=llm, prompt=prompt, memory=memory, verbose=False)

def update_user_history(user_id: str, query: str):
    profile = get_user_profile(user_id)
    if profile is None:
        profile = UserProfile(user_id=user_id)
    if not hasattr(profile, "history"):
        profile.history = []
    profile.history.append(query)
    profile.history = profile.history[-10:]
    save_user_profile(profile)

def handle_product_query(query: str, user_id: str) -> str:
    """Main handler with ambiguity, multi-product, context updates, and RAG toggle."""
    # Check cache first
    cached = get_cached_result(query)
    if cached:
        return f"(cached)\n{cached}"
    # Check for ambiguity first
    is_ambiguous, ambiguity_type = ambiguity_detector.is_ambiguous(query, user_id=user_id)
    if is_ambiguous:
        clarification_type = ambiguity_type if ambiguity_type else "general"
        return ambiguity_detector.generate_clarification(clarification_type)
    
     # Retrieve last query context
    last_query = get_last_query(user_id)

    # Detect update words like "actually", "make it", "instead", "change"
    if last_query and re.search(r"(actually|instead|make it|change|update|no,)", query.lower()):
        # Merge by replacing budget or product details in last query
        updated_query = re.sub(r"(under\s*₦?\d+)", query, last_query, flags=re.IGNORECASE)
        if updated_query == last_query:
            # if no budget pattern found, append modification
            updated_query = f"{last_query}, but {query}"
        query = updated_query

    # Save structured query in memory
    set_last_query(user_id, query)


    # Update profile history
    update_user_history(user_id, query)

    # Build chain
    qa = build_user_chain(user_id)

    # Split multi-product queries
    sub_queries = split_multi_product_query(query)
    all_responses = []

    for sub_q in sub_queries:
        try:
            if USE_RAG:
                result = qa.invoke({"question": sub_q}, config={"configurable": {"session_id": user_id}})
                if isinstance(result, dict):
                    answer = (
                        result.get("answer")
                        or result.get("result")
                        or result.get("text")
                        or result.get("response")
                        or "I'm not sure."
                    )
                    sources = result.get("source_documents", [])
                    if sources:
                        snippets = []
                        for i, doc in enumerate(sources[:2], start=1):  # max 2 per product
                            content = doc.page_content.strip().replace("\n", " ")
                            snippets.append(f"- {content}")
                        if snippets:
                            answer += "\n  Related products:\n  " + "\n  ".join(snippets)
                else:
                    answer = str(result)
            else:
                result = qa.invoke({"question": sub_q})
                answer = (
                    result.get("answer")
                    or result.get("result")
                    or result.get("text")
                    or result.get("response")
                    or str(result)
                    if isinstance(result, dict) else str(result)
                )

            all_responses.append((sub_q, answer))

        except Exception as e:
            all_responses.append((sub_q, f"Sorry, I had trouble with that query: {e}"))

    # Merge into conversational flow
    if len(all_responses) == 1:
        return all_responses[0][1]  # just one product, return directly
    else:
        final = "Here's what I found for you:\n\n"
        for sub_q, ans in all_responses:
            final += f"For **{sub_q}**:\n{ans}\n\n"
        cache_search_result(query, final)
        return final.strip()


def get_conversation_context(user_id: str) -> str:
    memory = get_memory(session_id=user_id)
    if not hasattr(memory, "chat_memory") or not memory.chat_memory.messages:
        return ""
    context = []
    for msg in memory.chat_memory.messages[-3:]:
        role = "User" if msg.type == "human" else "Xiara"
        context.append(f"{role}: {msg.content}")
    return "\n".join(context)
