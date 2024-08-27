import requests
from bs4 import BeautifulSoup

def ex_tag(sid):
    ### 뉴스 분야(sid)와 페이지(page)를 입력하면 그에 대한 링크들을 리스트로 추출하는 함수 ###
    
    ## 1.
    url = f"https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1={sid}"
    html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"\
    "(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "\
    "Chrome/110.0.0.0 Safari/537.36"})
    soup = BeautifulSoup(html.text, "lxml")
    a_tag = soup.find_all("a")
    
    ## 2.
    tag_lst = []
    for a in a_tag:
        if "href" in a.attrs:  # href가 있는것만 고르는 것
            if "article" in a["href"]:
                tag_lst.append(a["href"])
                
    return tag_lst

def re_tag(sid):
    ### 특정 분야의 뉴스의 링크를 수집하여 중복 제거한 리스트로 변환하는 함수 ###
    re_lst = ex_tag(sid)

    # # 중복 제거
    re_set = set(re_lst)
    re_lst = list(re_set)
    
    return re_lst

def art_crawl(url):
    """
    sid와 링크 인덱스를 넣으면 기사제목, 날짜, 본문을 크롤링하여 딕셔너리를 출력하는 함수 
    
    Args: 
        all_hrefs(dict): 각 분야별로 100페이지까지 링크를 수집한 딕셔너리 (key: 분야(sid), value: 링크)
        sid(int): 분야 [100: 정치, 101: 경제, 102: 사회, 103: 생활/문화, 104: 세계, 105: IT/과학]
        index(int): 링크의 인덱스
    
    Returns:
        dict: 기사제목, 날짜, 본문이 크롤링된 딕셔너리
    
    """
    art_dic = {}
    
    ## 1.
    title_selector = "#title_area > span"
    main_selector = "#dic_area"
    
    html = requests.get(url, headers = {"User-Agent": "Mozilla/5.0 "\
    "(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"\
    "Chrome/110.0.0.0 Safari/537.36"})
    soup = BeautifulSoup(html.text, "lxml")
    
    ## 2.
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
    
    ## 3.
    art_dic["title"] = title_str
    art_dic["main"] = main_str
    
    return art_dic