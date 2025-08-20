# xiara/tools/rag_tester.py
import os
from dotenv import load_dotenv
from xiara.core.prompt_chain import handle_product_query

def test_query(query: str, user_id: str = "rag_test_user"):
    """Test query with both RAG enabled and disabled."""
    load_dotenv()

    print("\n==============================")
    print(f"Testing query: {query}")
    print("==============================\n")

    # Test with RAG ON
    os.environ["USE_RAG"] = "true"
    from importlib import reload
    import xiara.core.prompt_chain as prompt_chain
    reload(prompt_chain)
    rag_response = prompt_chain.handle_product_query(query, user_id)

    print("RAG ENABLED RESPONSE:")
    print(rag_response)
    print("\n------------------------------\n")

    # Test with RAG OFF
    os.environ["USE_RAG"] = "false"
    reload(prompt_chain)
    no_rag_response = prompt_chain.handle_product_query(query, user_id)

    print(" RAG DISABLED RESPONSE:")
    print(no_rag_response)
    print("\n==============================\n")


if __name__ == "__main__":
    # Example test cases
    test_query("I want waterproof hiking boots under ₦20,000")
    test_query("Recommend a good budget smartphone")
    test_query("What is something durable for rainy season?")
