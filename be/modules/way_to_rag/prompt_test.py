from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(model="llama3.1:latest")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful, professional assistant named 'bot'. Introduce yourself first, and answer the questions. answer me in Korean no matter what. "),
    ("user", "{input}")
])

chain = prompt | llm | StrOutputParser()
result = chain.invoke({"input": "What is stock?"})
print(result)