import os
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

# Load env vars
load_dotenv()
DATA_PATH = os.getenv("DATA_PATH")
USE_RAG = os.getenv("USE_RAG", "true").lower() == "true"  # Toggle: true/false in .env
ambiguity_detector = AmbiguityDetector()

# Load & embed product data (if RAG is enabled)
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
    retriever = None  # fallback mode

# Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are Xiara, a knowledgeable and friendly AI assistant for product discovery on the Pasar marketplace.\n"
     "Understand the user's intent and product needs from natural language.\n\n"
     "If a query is ambiguous:\n"
     "- Ask for clarification about product type or category\n"
     "- Maintain context from previous messages\n"
     "- Guide users towards specific product details\n\n"
     "For clear queries, respond concisely focusing on:\n"
     "- Product features and qualities\n"
     "- Product comparisons or recommendations\n"
     "- Budget considerations if mentioned\n"
     "When appropriate, include product snippets."),
    ("human", "{question}")
])

def build_user_chain(user_id: str):
    """Return chain depending on USE_RAG flag."""
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
        return LLMChain(
            llm=llm,
            prompt=prompt,
            memory=memory,
            verbose=False
        )

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
    """Main handler with ambiguity + RAG toggle."""
    # Check for ambiguity
    is_ambiguous, ambiguity_type = ambiguity_detector.is_ambiguous(query, user_id=user_id)
    if is_ambiguous:
        clarification_type = ambiguity_type if ambiguity_type else "general"
        return ambiguity_detector.generate_clarification(clarification_type)

    # Update profile history
    update_user_history(user_id, query)

    # Build user chain
    qa = build_user_chain(user_id)

    # Run query
    try:
        if USE_RAG:
            result = qa.invoke({"question": query}, config={"configurable": {"session_id": user_id}})
            
            # Handle different response formats gracefully
            if isinstance(result, dict):
                answer = result.get("answer") or result.get("text") or result.get("response") or "I'm sorry, I couldn't generate a response."
                sources = result.get("source_documents", [])
                
                if sources:
                    snippets = "\n\nRelated Products:\n"
                    for i, doc in enumerate(sources[:3], start=1):
                        content = doc.page_content.strip().replace("\n", " ")
                        snippets += f"{i}. {content}\n"
                    return f"{answer}{snippets}"
                
                return f"{answer}\n\nI couldn't find exact product matches. Could you specify the product type, features, or budget?"
            else:
                # Handle string responses
                return str(result)
                
        else:
            result = qa.invoke({"question": query})
            
            # Handle different response formats gracefully
            if isinstance(result, dict):
                response_text = result.get("text") or result.get("answer") or result.get("response") or str(result)
                return str(response_text)
            else:
                return str(result)
                
    except KeyError as e:
        # Fallback for any KeyError issues
        return f"I'm sorry, I encountered an issue processing your request. Please try rephrasing your question."
    except Exception as e:
        # General error handling
        return f"I'm sorry, I encountered an error processing your request. Please try again."

def get_conversation_context(user_id: str) -> str:
    memory = get_memory(session_id=user_id)
    if not hasattr(memory, "chat_memory") or not memory.chat_memory.messages:
        return ""
    context = []
    for msg in memory.chat_memory.messages[-3:]:
        role = "User" if msg.type == "human" else "Xiara"
        context.append(f"{role}: {msg.content}")
    return "\n".join(context)
