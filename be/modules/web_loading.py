import bs4
from langchain_community.document_loaders import WebBaseLoader

def load_from_web(url):
    
    # 기사의 url 주소를 받으면 기사 내용을 document type으로 반환

    loader = WebBaseLoader(
        web_paths=(
            url,
        ),
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(
                attrs={"id": ["dic_area"]},
            )
        ),
    )
    
    return loader.load()

# 테스트용 코드:

# data = load_from_web("https://n.news.naver.com/article/011/0004385099?cds=news_media_pc&type=editn")

# print(f'type : {type(data)} / len : {len(data)}')
# print(f'data : {data}')
# for d in data:
    # print(f'page_content : {d.page_content}')
