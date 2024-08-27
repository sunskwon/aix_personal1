from modules import news_crawling
from modules import summary
from modules import pick_keyword
from modules import context_answer

art_dic = news_crawling.art_crawl("https://n.news.naver.com/article/005/0001720865?ntype=RANKING")

text_summary = summary.art_summary(art_dic)

keywords = pick_keyword.pick_keyword(text_summary)

answer = context_answer.context_answer("어떤 일이 일어났습니까?", art_dic)