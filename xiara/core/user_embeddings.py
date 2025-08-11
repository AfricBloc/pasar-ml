from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from xiara.core.user_profile_manager import get_user_profile
import os
import re

USER_EMBEDDINGS_PATH = "xiara/data/user_embeddings"
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def sanitize_user_id(user_id: str) -> str:
    """Sanitize user_id to prevent path traversal attacks."""
    return re.sub(r'[^a-zA-Z0-9_-]', '', user_id)

def generate_user_embedding(user_id: str):
    """Generate and save user embedding based on profile data."""
    safe_user_id = sanitize_user_id(user_id)
    profile = get_user_profile(user_id)
    if not profile:
        return
    
    text_representation = (
        " ".join(profile.liked_categories) + " " +
        (profile.purchase_intent or "") + " " +
        " ".join(profile.history)
    )
    
    try:
        vectorstore = FAISS.from_texts([text_representation], embedding_model)
        os.makedirs(USER_EMBEDDINGS_PATH, exist_ok=True)
        vectorstore.save_local(f"{USER_EMBEDDINGS_PATH}/{safe_user_id}")
    except Exception as e:
        print(f"Error generating embedding for user {user_id}: {e}")

def load_user_embedding(user_id: str):
    """Load user embedding from storage."""
    safe_user_id = sanitize_user_id(user_id)
    path = f"{USER_EMBEDDINGS_PATH}/{safe_user_id}"
    if os.path.exists(path):
        try:
            return FAISS.load_local(path, embedding_model)
        except Exception as e:
            print(f"Error loading embedding for user {user_id}: {e}")
    return None
