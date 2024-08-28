import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
import torch
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy

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
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-m3",
    model_kwargs = {'device': 'cuda' if torch.cuda.is_available() else 'cpu'}, # 모델이 CPU에서 실행되도록 설정. GPU를 사용할 수 있는 환경이라면 'cuda'로 설정할 수도 있음
    encode_kwargs = {'normalize_embeddings': True}, # 임베딩 정규화. 모든 벡터가 같은 범위의 값을 갖도록 함. 유사도 계산 시 일관성을 높여줌
)

data = loader.load()
splits = text_splitter.split_documents(data)
for i in range(len(splits)):
    print(splits[i])

vectorstore = FAISS.from_documents(splits, embedding = embeddings,)

# 로컬에 DB 저장
MY_FAISS_INDEX = "MY_FAISS_INDEX"
vectorstore.save_local(MY_FAISS_INDEX)
print(vectorstore.save_local(MY_FAISS_INDEX))