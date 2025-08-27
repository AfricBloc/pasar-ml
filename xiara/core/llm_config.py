# xiara/core/llm_config.py
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
    verbose=False,
    n_threads=os.cpu_count() or 8,  # Use all CPU threads
    n_batch=512,  # Larger batch → faster throughput
    max_tokens=512,  # Prevent long rambles
)
