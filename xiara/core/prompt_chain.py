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
from xiara.core.ambiguity_detector import AmbiguityDetector

# Initialize core components
load_dotenv()
DATA_PATH = os.getenv("DATA_PATH")
ambiguity_detector = AmbiguityDetector()

# Load & embed product data
documents = load_all_products(DATA_PATH)
splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_documents(documents)
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
VECTORSTORE_PATH = "xiara/core/faiss_index"

# Initialize or load vectorstore
if not os.path.exists(VECTORSTORE_PATH):
    vectorstore = FAISS.from_documents(docs, embedding_model)
    vectorstore.save_local(VECTORSTORE_PATH)
else:
    vectorstore = get_vectorstore()

if vectorstore is None:
    raise ValueError("Vectorstore could not be loaded. Please check initialization.")

retriever = vectorstore.as_retriever()

# Enhanced prompt template with clarification handling
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
    """Update user profile with query history."""
    profile = get_user_profile(user_id)
    if profile is None:
        profile = UserProfile(user_id=user_id)
    if not hasattr(profile, "history"):
        profile.history = []
    profile.history.append(query)
    profile.history = profile.history[-10:]  # Keep last 10 queries
    save_user_profile(profile)

def handle_product_query(query: str, user_id: str) -> str:
    """
    Main query handler with ambiguity detection and multi-turn conversation support.
    """
    # Check for ambiguity
    is_ambiguous, ambiguity_type = ambiguity_detector.is_ambiguous(query, user_id=user_id)
    if is_ambiguous:
        return ambiguity_detector.generate_clarification(ambiguity_type)

    # Update user history
    update_user_history(user_id, query)

    # Build and execute chain
    qa = build_user_chain(user_id)
    result = qa.invoke(
        {"question": query}, 
        config={"configurable": {"session_id": user_id}}
    )
    
    answer = result["answer"]
    sources = result.get("source_documents", [])

    # Debug: Print conversation history
    memory = qa.memory
    if hasattr(memory, "chat_memory"):
        print(f"\n--- Chat history for {user_id} ---")
        for idx, msg in enumerate(memory.chat_memory.messages, start=1):
            role = msg.type.capitalize() if hasattr(msg, "type") else "Unknown"
            print(f"{idx}. [{role}] {msg.content}")
        print("--- End of history ---\n")

    # Add relevant product snippets if available
    if sources:
        snippets = "\n\nRelated Products:\n"
        for i, doc in enumerate(sources[:3], start=1):
            content = doc.page_content.strip().replace("\n", " ")
            snippets += f"{i}. {content}\n"
        return f"{answer}{snippets}"

    return answer

def get_conversation_context(user_id: str) -> str:
    """Get formatted conversation context for a user."""
    memory = get_memory(session_id=user_id)
    if not hasattr(memory, "chat_memory") or not memory.chat_memory.messages:
        return ""
    
    context = []
    for msg in memory.chat_memory.messages[-3:]:  # Last 3 messages
        role = "User" if msg.type == "human" else "Xiara"
        context.append(f"{role}: {msg.content}")
    
    return "\n".join(context)