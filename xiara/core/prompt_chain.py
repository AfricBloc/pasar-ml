import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from xiara.core.product_loader import load_all_products
from xiara.core.llm_config import llm
from xiara.core.vectorstore_loader import get_vectorstore
from xiara.core.user_profile_manager import get_user_profile, save_user_profile, UserProfile
from xiara.core.memory_manager import get_memory
from xiara.core.ambiguity_detector import is_ambiguous  # 🔹 Use improved ambiguity detection

load_dotenv()
DATA_PATH = os.getenv("DATA_PATH")

# Load & embed product data (if vectorstore missing)
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

# Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are Xiara, a knowledgeable and friendly AI assistant for product discovery on the Pasar marketplace.\n"
     "Understand the user's intent and product needs from natural language.\n\n"
     "Respond concisely and professionally, focusing on:\n"
     "- Product features and qualities\n"
     "- Product comparisons or recommendations\n"
     "- Budget considerations if mentioned\n"
     "When appropriate, include product snippets."),
    ("human", "{question}")
])

def build_user_chain(user_id: str):
    """Return QA chain with per-user memory."""
    memory = get_memory(session_id=user_id)
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=False,
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
    """Main query handler with ambiguity detection + multi-turn memory."""
    
    # Ambiguity check first
    if is_ambiguous(query, user_id=user_id):
        return f"Xiara Could you clarify? For example, what type of product are you referring to when you say: '{query}'?"

    # Update personalization history
    update_user_history(user_id, query)

    # Build chain and answer
    qa = build_user_chain(user_id)
    result = qa.invoke({"question": query}, config={"configurable": {"session_id": user_id}})
    answer = result["answer"]
    sources = result.get("source_documents", [])

    # DEBUG: Print current conversation history
    memory = qa.memory
    if hasattr(memory, "chat_memory"):
        print(f"\n--- Chat history for {user_id} ---")
        for idx, msg in enumerate(memory.chat_memory.messages, start=1):
            role = msg.type.capitalize() if hasattr(msg, "type") else "Unknown"
            print(f"{idx}. [{role}] {msg.content}")
        print("--- End of history ---\n")

    if sources:
        snippets = "\n\n Related Products:\n"
        for i, doc in enumerate(sources[:3], start=1):
            content = doc.page_content.strip().replace("\n", " ")
            snippets += f"{i}. {content}\n"
        return f"{answer}{snippets}"

    return answer
