from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from xiara.core.llm_config import llm

# Load & embed product data 
loader = TextLoader("C:/Users/MOSES/Desktop/PASAR Agentic AI/pasar-ml/xiara/data/products.txt")
documents = loader.load()

splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_documents(documents)

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(docs, embedding_model)
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
     "- Budget considerations if mentioned (e.g., under ₦10,000)\n\n"
     "Be helpful and clear, like a product expert guiding a shopper."),
    ("human", "{question}")
])

# Global QA Chain with memory placeholder (we isolate memory using session_id at runtime)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
qa = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    return_source_documents=False,
    verbose=False
)

# Per-user handler
def handle_product_query(query: str, user_id: str) -> str:
    return qa.invoke({"question": query}, config={"configurable": {"session_id": user_id}})["answer"]

