import torch
from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings
from text_chunking import split_text
from web_loading import load_from_web

# pipeline 생성
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-m3",
    model_kwargs = {'device': 'cuda' if torch.cuda.is_available() else 'cpu'},
    # 임베딩 정규화
    # 모든 벡터가 같은 범위의 값을 갖도록 함
    # 유사도 계산 시 일관성을 높여줌
    encode_kwargs = {'normalize_embeddings': True}, 
)
llm = ChatOllama(model="llama3.1:latest")

# prompt template 생성
prompt = PromptTemplate.from_template(
"""
당신은 질문에 대한 답변(Question-Answering)을 수행하는 친절한 AI 어시스턴트입니다.
당신의 임무는 주어진 문맥(context)에서 주어진 질문(question)에 답하는 것입니다.
검색된 다음 문맥(context)을 사용하여 질문(question)에 답하세요.
만약, 주어진 문맥(context)에서 답을 찾을 수 없거나 답을 모른다면 `질문에 대한 정보를 찾을 수 없습니다` 라고 답하세요.
한글로 답변해 주세요.
단, 기술적인 용어나 이름은 번역하지 않고 그대로 사용해 주세요.
Don't narrate the answer, just answer the question.
Let's think step-by-step.

#Question: 
{question} 

#Context: 
{context} 

#Answer:
"""
)

def answer_from_context(url, query):

    # 기사 url과 질문을 받으면 기사 내용을 기반으로 답변
    data = load_from_web(url)
    split_data = split_text(data)
        
    vectorstore = FAISS.from_documents(documents = split_data, embedding = embeddings)
    # vertordb에서 가장 연관성이 높은 5개 추출
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain.invoke(query)

# 테스트용 코드:

# print(answer_from_context("https://n.news.naver.com/article/011/0004385099?cds=news_media_pc&type=editn", "업계의 설명은?"))