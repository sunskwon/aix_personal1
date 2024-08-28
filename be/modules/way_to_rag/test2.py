LANGCHAIN_TRACING_V2=True
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY=""
LANGCHAIN_PROJECT="pr-virtual-congregation-16"

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(openai_api_key="")
response = llm.invoke("Hello, world!")
print(response)