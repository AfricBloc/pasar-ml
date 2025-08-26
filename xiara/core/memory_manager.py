# xiara/core/memory_manager.py
"""
Memory Manager for Xiara
Supports in-memory (default) or Redis-backed conversation history,
structured query persistence, and caching of product search results.
"""

from langchain.memory import ConversationBufferMemory

# Toggle this to switch memory backends later
USE_REDIS = False  # Set to True to use RedisMemory

# Store per-user memories here
_memory_store = {}

# Fallback storage for last queries and cached results
_last_queries = {}
_query_cache = {}


def get_memory(session_id: str = "default_session"):
    """
    Returns a memory object for storing conversation context.
    Each user/session_id gets its own memory buffer.
    """
    if USE_REDIS:
        from langchain.memory.chat_message_histories import RedisChatMessageHistory

        if session_id not in _memory_store:
            history = RedisChatMessageHistory(
                url="redis://localhost:6379/0",
                session_id=session_id
            )
            _memory_store[session_id] = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                chat_memory=history,
                output_key="answer"
            )
        return _memory_store[session_id]

    else:
        # Default: In-memory buffer (per session)
        if session_id not in _memory_store:
            _memory_store[session_id] = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                output_key="answer"
            )
        return _memory_store[session_id]


# -------------------------------
# Structured Query Persistence
# -------------------------------

def set_last_query(user_id: str, query: str):
    """Save last structured query in Redis or memory."""
    if USE_REDIS:
        import redis, json
        global redis_client
        if "redis_client" not in globals():
            redis_client = redis.Redis.from_url("redis://localhost:6379/0")
        redis_client.set(f"xiara:last_query:{user_id}", json.dumps({"query": query}))
    else:
        _last_queries[user_id] = query


def get_last_query(user_id: str):
    """Retrieve last structured query from Redis or memory."""
    if USE_REDIS:
        import redis, json
        global redis_client
        if "redis_client" not in globals():
            redis_client = redis.Redis.from_url("redis://localhost:6379/0")
        data = redis_client.get(f"xiara:last_query:{user_id}")
        if data:
            return json.loads(data).get("query")
        return None
    else:
        return _last_queries.get(user_id)


def clear_last_query(user_id: str):
    """Clear stored query for a user."""
    if USE_REDIS:
        import redis
        global redis_client
        if "redis_client" not in globals():
            redis_client = redis.Redis.from_url("redis://localhost:6379/0")
        redis_client.delete(f"xiara:last_query:{user_id}")
    else:
        if user_id in _last_queries:
            del _last_queries[user_id]


# -------------------------------
# Product Search Caching
# -------------------------------

def cache_search_result(query: str, result: str, ttl: int = 600):
    """
    Cache a product search result for a given query.
    Default TTL = 600s (10 minutes).
    """
    if USE_REDIS:
        import redis, json
        global redis_client
        if "redis_client" not in globals():
            redis_client = redis.Redis.from_url("redis://localhost:6379/0")
        redis_client.setex(f"xiara:query_cache:{query}", ttl, json.dumps({"result": result}))
    else:
        _query_cache[query] = result


def get_cached_result(query: str):
    """Retrieve cached result if available."""
    if USE_REDIS:
        import redis, json
        global redis_client
        if "redis_client" not in globals():
            redis_client = redis.Redis.from_url("redis://localhost:6379/0")
        data = redis_client.get(f"xiara:query_cache:{query}")
        if data:
            return json.loads(data).get("result")
        return None
    else:
        return _query_cache.get(query)


def clear_cached_result(query: str):
    """Remove a query result from cache."""
    if USE_REDIS:
        import redis
        global redis_client
        if "redis_client" not in globals():
            redis_client = redis.Redis.from_url("redis://localhost:6379/0")
        redis_client.delete(f"xiara:query_cache:{query}")
    else:
        if query in _query_cache:
            del _query_cache[query]
