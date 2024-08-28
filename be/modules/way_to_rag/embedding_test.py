from langchain_community.embeddings import HuggingFaceEmbeddings
import torch

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-m3",
    model_kwargs = {'device': 'cuda' if torch.cuda.is_available() else 'cpu'}, # 모델이 CPU에서 실행되도록 설정. GPU를 사용할 수 있는 환경이라면 'cuda'로 설정할 수도 있음
    encode_kwargs = {'normalize_embeddings': True}, # 임베딩 정규화. 모든 벡터가 같은 범위의 값을 갖도록 함. 유사도 계산 시 일관성을 높여줌
)
embed = embeddings.embed_documents(
    [
        "안녕 영광",
        "동해물과 백두산",
        "마르고 닳도록",
        "하느님이 보우하사",
        "우리나라 만세"
    ]
)
print(f"len(embed): {len(embed)}")
print(f"len(embed[0]): {len(embed[0])}")
print(f"len(embed[1]): {len(embed[1])}")
print(f"embed: {embed}")