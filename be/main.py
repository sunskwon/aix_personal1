from modules import news_crawling
from modules import summary
from modules import pick_keyword
from modules import rag_answering

art_dic = news_crawling.art_crawl("https://n.news.naver.com/article/005/0001720865?ntype=RANKING")

text_summary = summary.art_summary(art_dic)

keywords = pick_keyword.pick_keyword(text_summary)
