from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# pipeline 생성:
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=30)

def split_text(data):
    
    # 입력된 document type의 page_content를 일정 간격으로 분리
    return text_splitter.split_documents(data)

# 테스트용 코드:

# from web_loading import load_from_web

# data = load_from_web("https://n.news.naver.com/article/011/0004385099?cds=news_media_pc&type=editn")
# print(f'type : {type(data)} / len : {len(data)}')
# print(f'data : {data}')
# for d in data:
#     print(f'page_content : {d.page_content}')

# split_data = split_text(data)
# for content in split_data:
#     print(content)