# xiara/core/memory_manager.py
"""
Memory Manager for Xiara
Currently uses ConversationBufferMemory (in-memory),
but can be switched to RedisMemory by changing USE_REDIS to True.
"""

from langchain.memory import ConversationBufferMemory

# Toggle this to switch memory backends later
USE_REDIS = False

def get_memory(session_id: str = "default_session"):
    """
    Returns a memory object for storing conversation context.
    """
    if USE_REDIS:
        from langchain.memory.chat_message_histories import RedisChatMessageHistory

        history = RedisChatMessageHistory(
            url="redis://localhost:6379/0",  # adjust if needed
            session_id=session_id
        )

        return ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            chat_memory=history
        )

    else:
        # Default: In-memory buffer (no persistence)
        return ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
