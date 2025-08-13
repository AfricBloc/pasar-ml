import os
from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from xiara.core.product_loader import load_all_products
from xiara.core.llm_config import llm
from xiara.core.vectorstore_loader import get_vectorstore
from xiara.core.user_profile_manager import get_user_profile, save_user_profile, UserProfile
from xiara.core.memory_manager import get_memory  # 🔹 New centralized memory import

# Load & embed product data (if vectorstore is missing)
documents = load_all_products()
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
    raise ValueError("Vectorstore could not be loaded. Please check the vectorstore initialization.")

retriever = vectorstore.as_retriever()

# Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are Xiara, a knowledgeable and friendly AI assistant for product discovery on the Pasar marketplace.\n"
     "Understand the user's intent and product needs from natural language, even when no specific category is mentioned.\n\n"
     "Respond concisely and professionally, focusing on:\n"
     "- Product features and qualities (e.g., durable, waterproof, compact)\n"
     "- Product comparisons or recommendations\n"
     "- Budget considerations if mentioned (e.g., under ₦10,000)\n"
     "Be helpful and clear, like a product expert guiding a shopper. When appropriate, include product snippets to support your suggestions."),
    ("human", "{question}")
])

# Build QA Chain per user
def build_user_chain(user_id: str):
    """Return a QA chain with memory isolated per user."""
    memory = get_memory(session_id=user_id)
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=False,
        verbose=False
    )

# Update user profile history
def update_user_history(user_id: str, query: str):
    profile = get_user_profile(user_id)
    if profile is None:
        profile = UserProfile(user_id=user_id)

    if not hasattr(profile, "history"):
        profile.history = []

    profile.history.append(query)
    profile.history = profile.history[-10:]  # Keep last 10 queries
    save_user_profile(profile)

# Handle queries
# Per-user handler with snippet formatting + profile update
def handle_product_query(query: str, user_id: str) -> str:
    # Update personalization history
    update_user_history(user_id, query)

    # Build user-specific QA chain
    qa = build_user_chain(user_id)
    memory = qa.memory  # For debug logging below

    # Get LLM answer
    result = qa.invoke({"question": query}, config={"configurable": {"session_id": user_id}})
    answer = result["answer"]
    sources = result.get("source_documents", [])

    # DEBUG: Log current conversation memory for this user
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
