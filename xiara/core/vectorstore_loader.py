import os
import time
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from xiara.core.product_loader import load_all_products

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data")
VECTORSTORE_PATH = os.path.join(os.path.dirname(__file__), "faiss_index")

def get_vectorstore():
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    index_file = os.path.join(VECTORSTORE_PATH, "index.faiss")
    pkl_file = os.path.join(VECTORSTORE_PATH, "index.pkl")

    # Check for both files
    if os.path.exists(index_file) and os.path.exists(pkl_file):
        try:
            if data_is_newer(DATA_PATH, VECTORSTORE_PATH):
                print("Product data changed — rebuilding FAISS index...")
                return rebuild_vectorstore(embedding_model)
            return FAISS.load_local(
                VECTORSTORE_PATH,
                embedding_model,
                allow_dangerous_deserialization=True
            )
        except ValueError as e:
            if "allow_dangerous_deserialization" in str(e):
                print("Pickle restriction detected. Rebuilding FAISS index for safety...")
                return rebuild_vectorstore(embedding_model)
            else:
                raise e

    # No complete index found — build from scratch
    return rebuild_vectorstore(embedding_model)

def data_is_newer(data_path, index_path):
    index_mtime = latest_modified_time(index_path)
    data_mtime = latest_modified_time(data_path)
    return data_mtime > index_mtime

def latest_modified_time(path):
    if os.path.isfile(path):
        return os.path.getmtime(path)
    latest_time = 0
    for root, _, files in os.walk(path):
        for f in files:
            full_path = os.path.join(root, f)
            latest_time = max(latest_time, os.path.getmtime(full_path))
    return latest_time

def rebuild_vectorstore(embedding_model):
    documents = load_all_products(DATA_PATH)
    if not documents:
        print("No product documents found. Cannot build vectorstore.")
        return None

    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    vectorstore = FAISS.from_documents(chunks, embedding_model)
    vectorstore.save_local(VECTORSTORE_PATH)
    print(f"Vectorstore rebuilt and saved to {VECTORSTORE_PATH}")
    return vectorstore