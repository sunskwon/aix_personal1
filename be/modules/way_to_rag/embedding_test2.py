from langchain_community.embeddings import HuggingFaceEmbeddings
import torch
from langchain_core.documents import Document
from langchain.vectorstores import FAISS

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-m3",
    model_kwargs = {'device': 'cuda' if torch.cuda.is_available() else 'cpu'}, # 모델이 CPU에서 실행되도록 설정. GPU를 사용할 수 있는 환경이라면 'cuda'로 설정할 수도 있음
    encode_kwargs = {'normalize_embeddings': True}, # 임베딩 정규화. 모든 벡터가 같은 범위의 값을 갖도록 함. 유사도 계산 시 일관성을 높여줌
)
docs_for_test_embed = [
    Document(page_content="사과", metadata=dict(page=1)),
    Document(page_content="애플", metadata=dict(page=1)),
    Document(page_content="바나나", metadata=dict(page=2)),
    Document(page_content="오렌지", metadata=dict(page=2)),
    Document(page_content="고양이", metadata=dict(page=3)),
    Document(page_content="야옹", metadata=dict(page=3)),
    Document(page_content="강아지", metadata=dict(page=4)),
    Document(page_content="멍멍", metadata=dict(page=4)),
    Document(page_content="해", metadata=dict(page=5)),
    Document(page_content="달", metadata=dict(page=5)),
    Document(page_content="물", metadata=dict(page=6)),
    Document(page_content="불", metadata=dict(page=6)),
]

db = FAISS.from_documents(docs_for_test_embed, embeddings)

def similarity_search_with_score(keyword: str) -> None:
    results_with_scores = db.similarity_search_with_score(keyword, k=5)
    print(f"Keyword: {keyword}")
    for doc, score in results_with_scores:
        print(f" > Content: {doc.page_content} / Metadata: {doc.metadata} / Score: {score}({score:.10f})")
        
similarity_search_with_score("사과")
similarity_search_with_score("강아지")
similarity_search_with_score("해")