import random
from datetime import datetime
from fastapi import Depends, FastAPI, Request
from modules import ext_keyword
from modules import lang_detect
from modules import news_crawling
from modules import rag_answering

app = FastAPI()

def log_request_time(request: Request):
    start_time = datetime.now()
    request.state.start_time = start_time
    print(f"Request started at: {start_time}")
    yield
    end_time = datetime.now()
    duration = end_time - start_time
    print(f"Request ended at: {end_time}")
    print(f"Request duration: {duration}")

@app.get("/keyword")
async def gen_keyword(sid: str):
    
    # 뉴스 리스트를 검색하고 그 중 두 기사의 url과 keyword들을 반환
    art_list = news_crawling.art_list(sid)
    
    main_title = ''
    sub_title = ''
    main_keywords = []
    sub_keywords = []
    
    # 영문 기사가 선택되면 다시 선택
    while (main_title == '') or (sub_title == ''):
        
        random_art = random.sample(art_list, 2)
        
        main_art = news_crawling.art_crawl(random_art[0])
        sub_art = news_crawling.art_crawl(random_art[1])
    
        main_title = lang_detect.detect_language(main_art['title'])
        sub_title = lang_detect.detect_language(sub_art['title'])
    
    main_keywords.extend(ext_keyword.extract_keywords(main_art))
    sub_keywords.extend(ext_keyword.extract_keywords(sub_art))
    
    return {
        "selected_arts": random_art,
        "main_keywords": main_keywords,
        "sub_keywords": sub_keywords,
    }

@app.post("/ask", dependencies=[Depends(log_request_time)])
async def ask_test(urls: list[str], query: str):
    
    # url 주소와 질문을 기반으로 rag 처리
    answer = rag_answering.answer_from_context(urls, query)
    
    return {
        "answer": answer,
    }
    
# 테스트용 코드:

# def gen_keyword_test(sid: str):
    
#     art_list = news_crawling.art_list(sid)
    
#     main_title = ''
#     sub_title = ''
#     main_keywords = []
#     sub_keywords = []
    
#     while (main_title == '') or (sub_title == ''):
        
#         random_art = random.sample(art_list, 2)
        
#         main_art = news_crawling.art_crawl(random_art[0])
#         sub_art = news_crawling.art_crawl(random_art[1])
    
#         main_title = lang_detect.detect_language(main_art['title'])
#         sub_title = lang_detect.detect_language(sub_art['title'])
    
#     main_keywords.extend(ext_keyword.extract_keywords(main_art))
#     sub_keywords.extend(ext_keyword.extract_keywords(sub_art))
    
#     return {
#         "selected_arts": random_art,
#         # "main_art": random_art[0],
#         # "sub_art": random_art[1],
#         # "main_title": main_art['title'],
#         # "sub_title": sub_art['title'],
#         # "main_cont": main_art['main'],
#         # "sub_cont": sub_art['main'],
#         "main_keywords": main_keywords,
#         "sub_keywords": sub_keywords,
#     }

# def ask_test(urls: list, query: str):
    
#     return rag_answering.answer_from_context(urls, query)

# test_url = "https://n.news.naver.com/mnews/ranking/article/293/0000057948?ntype=RANKING"

# art_dic = news_crawling.art_crawl(test_url)
# keywords = ext_keyword.extract_keywords(art_dic)
# print(art_dic)
# print(keywords)

# generated_keyword = gen_keyword_test(103)
# print(generated_keyword)

# generated_answer = ask_test("", "누구에 대한 내용이야?")
# print(generated_answer)