from langchain_community.llms import LlamaCpp

llm = LlamaCpp(
    model_path="C:/Users/MOSES/Desktop/PASAR Agentic AI/llama-2-7b.Q4_K_M.gguf",  # install "llama-2-7b.Q4_K_M.gguf" and set the path 
    n_ctx=2048,
    temperature=0.7,
    top_p=0.95,
    verbose=True,
    n_threads=4  
)
