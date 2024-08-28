import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
import torch
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# BeautifulSoup : HTML 및 XML 문서를 파싱하고 구문 분석하는 데 사용되는 파이썬 라이브러리. 주로 웹 스크레이핑(웹 페이지에서 데이터 추출) 작업에서 사용되며, 웹 페이지의 구조를 이해하고 필요한 정보를 추출하는 데 유용
loader = WebBaseLoader(
    web_paths=(
        "https://n.news.naver.com/article/011/0004385099?cds=news_media_pc&type=editn",
               ),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            attrs={"id": ["dic_area"]}, # 태그의 ID 값들
        )
    ),
)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=30)
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-m3",
    model_kwargs = {'device': 'cuda' if torch.cuda.is_available() else 'cpu'}, # 모델이 CPU에서 실행되도록 설정. GPU를 사용할 수 있는 환경이라면 'cuda'로 설정할 수도 있음
    encode_kwargs = {'normalize_embeddings': True}, # 임베딩 정규화. 모든 벡터가 같은 범위의 값을 갖도록 함. 유사도 계산 시 일관성을 높여줌
)
prompt = PromptTemplate.from_template(
    """당신은 질문-답변(Question-Answering)을 수행하는 친절한 AI 어시스턴트입니다. 당신의 임무는 주어진 문맥(context) 에서 주어진 질문(question) 에 답하는 것입니다.
검색된 다음 문맥(context) 을 사용하여 질문(question) 에 답하세요. 만약, 주어진 문맥(context) 에서 답을 찾을 수 없다면, 답을 모른다면 `주어진 정보에서 질문에 대한 정보를 찾을 수 없습니다` 라고 답하세요.
한글로 답변해 주세요. 단, 기술적인 용어나 이름은 번역하지 않고 그대로 사용해 주세요. Don't narrate the answer, just answer the question. Let's think step-by-step.

#Question: 
{question} 

#Context: 
{context} 

#Answer:"""
)
llm = ChatOllama(model="llama3.1:latest")

data = loader.load()
splits = text_splitter.split_documents(data)

vectorstore = FAISS.from_documents(documents = splits, embedding = embeddings)

# 로컬에 DB 저장
# MY_FAISS_INDEX = "MY_FAISS_INDEX"
# vectorstore.save_local(MY_FAISS_INDEX)

# vectors = FAISS.load_local(MY_FAISS_INDEX,
#                            embeddings,
#                            allow_dangerous_deserialization=True
#                            # 잠재적으로 위험한 데이터 구조나 객체를 포함할 수 있는 인덱스 파일의 로딩을 허용. 주로 자신이 직접 생성하고 저장한 인덱스 파일을 로드할 때 사용
#                            )

retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5}) 

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
result = chain.invoke('업계의 설명?')

print(result)