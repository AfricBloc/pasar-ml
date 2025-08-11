from langchain_community.llms import LlamaCpp

llm = LlamaCpp(
    model_path="C:\\Users\\OLALERE\\Desktop\\pasar-ml\\tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",  #  tinyllama alternative and set the path
    n_ctx=2048,
    temperature=0.7,
    top_p=0.95,
    verbose=True,
    n_threads=4  
)


