from langchain.prompts import PromptTemplate
from langchain_community.llms.fake import FakeListLLM

# Static responses for demonstration
STATIC_RESPONSES = [
    "Here are some noise-cancelling headphones: Product A, Product B.",
    "For travel, I recommend Product C and Product D.",
    "Sorry, I couldn't find any matching products."
]

# Use a fake LLM for static responses (for demo)
llm = FakeListLLM(responses=STATIC_RESPONSES)

prompt = PromptTemplate(
    input_variables=["query"],
    template="User asked: {query}\nSuggest relevant products."
)

# Create a pipeline using the | operator
chain = prompt | llm

def handle_product_query(query: str) -> str:
    # This is for to invoke the chain with the query
    return chain.invoke({"query": query})