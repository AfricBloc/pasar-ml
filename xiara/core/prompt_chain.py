from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms.fake import FakeListLLM

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

chain = LLMChain(llm=llm, prompt=prompt)

def handle_product_query(query: str) -> str:
    # This will cycle through STATIC_RESPONSES for each call
    return chain.run(query=query)