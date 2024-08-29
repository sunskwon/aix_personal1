import re
from konlpy.tag import Okt
from krwordrank.word import KRWordRank

min_count = 1   # 단어의 최소 출현 빈도수 (그래프 생성 시)
max_length = 10 # 단어의 최대 길이
beta = 0.85    # PageRank의 decaying factor beta
max_iter = 20

def split_noun_sentences(text):
    okt = Okt()
    sentences = text.replace(". ",".")
    sentences = re.sub(r'([^\n\s\.\?!]+[^\n\.\?!]*[\.\?!])', r'\1\n', sentences).strip().split("\n")
    
    result = []
    for sentence in sentences:
        if len(sentence) == 0:
            continue
        sentence_pos = okt.pos(sentence, stem=True)
        nouns = [word for word, pos in sentence_pos if pos == 'Noun']
        if len(nouns) == 1:
            continue
        result.append(' '.join(nouns) + '.')
        
    return result

def extract_keywords(art_dic):
    
    # 기사에서 사용 빈도 순의 keyword를 2개 추출
    text = art_dic['main']
    texts = split_noun_sentences(text)

    wordrank_extractor = KRWordRank(min_count=min_count, max_length=max_length)
    keywords, rank, graph = wordrank_extractor.extract(texts, beta, max_iter)
        
    return list(keywords.keys())[:2]

#테스트용 코드:

# import news_crawling

# urls = [
#     "https://n.news.naver.com/mnews/ranking/article/448/0000474464?ntype=RANKING",
#     "https://n.news.naver.com/mnews/article/016/0002355828"
# ]

# for url in urls:
#     temp_art = news_crawling.art_crawl(url)
#     temp_keywords = extract_keywords(temp_art)
#     print(temp_keywords)

# url1 = "https://n.news.naver.com/mnews/ranking/article/448/0000474464?ntype=RANKING"
# url2 = "https://n.news.naver.com/mnews/article/016/0002355828"

# art1 = news_crawling.art_crawl(url1)
# art2 = news_crawling.art_crawl(url2)

# temp1 = extract_keywords(art1)
# temp2 = extract_keywords(art2)

# print(temp1)
# print(temp2)