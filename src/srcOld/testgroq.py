from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

llm = ChatGroq(api_key="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", model_name="llama-3.3-70b-versatile")

response = llm.invoke([
    HumanMessage(content="¿Cuál es la capital de Colombia?")
])

print(response.content)
