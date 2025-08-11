from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from xiara.core.product_loader import load_all_products
from langchain.text_splitter import CharacterTextSplitter
from xiara.core.llm_config import llm
from xiara.core.vectorstore_loader import get_vectorstore
from xiara.core.user_profile_manager import get_user_profile, save_user_profile, UserProfile
import os

# Load & embed product data
documents = load_all_products("xiara/data")

splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_documents(documents)
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
VECTORSTORE_PATH = "xiara/core/faiss_index"
if not os.path.exists(VECTORSTORE_PATH):
    vectorstore = FAISS.from_documents(docs, embedding_model)
    vectorstore.save_local(VECTORSTORE_PATH)
else:
    vectorstore = FAISS.load_local(VECTORSTORE_PATH, embedding_model)

vectorstore = get_vectorstore()
retriever = vectorstore.as_retriever()

# Add memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Define prompt
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

# Global QA Chain
qa = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    return_source_documents=True,
    verbose=False
)

# Helper: update user profile history
def update_user_history(user_id: str, query: str):
    profile = get_user_profile(user_id)
    if profile is None:
        profile = UserProfile(user_id=user_id)

    if not hasattr(profile, "history"):
        profile.history = []

    profile.history.append(query)
    profile.history = profile.history[-10:]  # Keep last 10 queries
    save_user_profile(profile)

# Per-user handler with snippet formatting + profile update
def handle_product_query(query: str, user_id: str) -> str:
    # Update personalization history
    update_user_history(user_id, query)

    # Get LLM answer
    result = qa.invoke({"question": query}, config={"configurable": {"session_id": user_id}})
    answer = result["answer"]
    sources = result.get("source_documents", [])

    if sources:
        snippets = "\n\n Related Products:\n"
        for i, doc in enumerate(sources[:3], start=1):
            content = doc.page_content.strip().replace("\n", " ")
            snippets += f"{i}. {content}\n"
        return f"{answer}{snippets}"

    return answer
