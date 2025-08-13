from langchain_community.llms import LlamaCpp
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env

model_path = os.getenv("MODEL_PATH")

llm = LlamaCpp(
    model_path=model_path,
    n_ctx=2048,
    temperature=0.7,
    top_p=0.95,
    verbose=True,
    n_threads=4
)