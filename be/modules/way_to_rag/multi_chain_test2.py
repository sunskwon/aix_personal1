from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

llm = ChatOllama(model="llama3.1:latest")

joke_chain = (
    ChatPromptTemplate.from_template("{topic}에 관련해서 짧은 농담 말해줘") 
    | llm
    | StrOutputParser())
poem_chain = (
    ChatPromptTemplate.from_template("{topic}에 관련해서 시 2줄 써줘") 
    | llm
    | StrOutputParser())

# map_chain = {"joke": joke_chain, "poem": poem_chain} # 체인에서 이처럼 사용할 때, 자동으로 RunnableParallel 사용됨
# map_chain = RunnableParallel({"joke": joke_chain, "poem": poem_chain})
map_chain = RunnableParallel(joke=joke_chain, poem=poem_chain)

result = map_chain.invoke({"topic": "애플"})
print(result)