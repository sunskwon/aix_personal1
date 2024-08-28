LANGCHAIN_TRACING_V2=True
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY="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"
LANGCHAIN_PROJECT="pr-virtual-congregation-16"

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(openai_api_key="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")
response = llm.invoke("Hello, world!")
print(response)