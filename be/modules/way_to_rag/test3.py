from langchain_community.chat_models import ChatOllama

llm = ChatOllama(model="llama3.1:latest")
result = llm.invoke("'인천'은 '마계'인가요?")
print(result)