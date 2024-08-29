import requests
from bs4 import BeautifulSoup

def all_list(sid):
    
    # 뉴스 분야(sid)를 입력하면 그에 대한 링크들을 리스트로 추출
    
    # 1. <a> tag 전체 추출
    url = f"https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1={sid}"
    html = requests.get(url, 
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }
    )
    soup = BeautifulSoup(html.text, "lxml")
    a_list = soup.find_all("a")
    
    # 2. <a> tag 중 href attrs. 값만 추출
    url_list = []
    for a in a_list:
        if "href" in a.attrs:
            if "article" in a["href"] and 'comment' not in a["href"]:
                url_list.append(a["href"])
                
    return url_list

def art_list(sid):
    
    # 뉴스 링크를 수집하고 중복 제거
    re_lst = all_list(sid)

    re_set = set(re_lst)
    re_lst = list(re_set)
    
    return re_lst

def art_crawl(url):
    
    # 뉴스 url을 입력하면 기사제목과 본문 내용을 크롤링
    art_dic = {}
    
    # 제목과 본문의 tag(id)
    title_selector = "#title_area > span"
    main_selector = "#dic_area"
    
    html = requests.get(url, 
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }
    )
    soup = BeautifulSoup(html.text, "lxml")
    
    # 제목 수집
    title = soup.select(title_selector)
    title_lst = [t.text for t in title]
    title_str = "".join(title_lst)
    
    # 본문 수집
    main = soup.select(main_selector)
    main_lst = []
    for m in main:
        m_text = m.text
        m_text = m_text.strip()
        main_lst.append(m_text)
    main_str = "".join(main_lst)
    
    art_dic["title"] = title_str
    art_dic["main"] = main_str
    
    return art_dic