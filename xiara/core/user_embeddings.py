from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from xiara.core.user_profile_manager import get_user_profile
import os

USER_EMBEDDINGS_PATH = "xiara/data/user_embeddings"
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def generate_user_embedding(user_id: str):
    profile = get_user_profile(user_id)
    text_representation = (
        " ".join(profile.liked_categories) + " " +
        (profile.purchase_intent or "") + " " +
        " ".join(profile.last_queries)
    )
    vectorstore = FAISS.from_texts([text_representation], embedding_model)
    os.makedirs(USER_EMBEDDINGS_PATH, exist_ok=True)
    vectorstore.save_local(f"{USER_EMBEDDINGS_PATH}/{user_id}")

def load_user_embedding(user_id: str):
    path = f"{USER_EMBEDDINGS_PATH}/{user_id}"
    if os.path.exists(path):
        return FAISS.load_local(path, embedding_model)
    return None
