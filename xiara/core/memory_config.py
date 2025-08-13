from langchain.memory import ConversationBufferMemory

# Single point of memory creation — easy to swap with RedisMemory later
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)
