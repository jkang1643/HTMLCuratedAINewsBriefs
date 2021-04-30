import newspaper
from newspaper import Article
import nltk
from datetime import date
import spacy
import csv
import pandas as pd
import numpy as np
from django.shortcuts import render
import os

nltk.download('punkt')

today = date.today()
d2 = today.strftime("%B %d, %Y")
extraction_date = today.strftime("%B %d, %Y")

'''with open(" Update for " + today.strftime("%B %d, %Y" + ".csv"), 'w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Summary","Keywords", "Summary Topics",  "Url", "Publishdate", "ExtractionDate"])'''


article_list = []
corpus = []


# Function to convert
def listToString(s):
    # initialize an empty string
    str1 = ", "
    # return string
    return (str1.join(s))


#list iteration for pnadas dataframe on trending topics
named_entities = []
temp_entity_name = ''
temp_named_entity = None

#list to string function
def converttostr(input_seq, seperator):
   # Join all the strings in list
   final_str = seperator.join(input_seq)
   return final_str

separator = ', '

Article_title = []
Article_summary = []
Article_keyword = []
Article_URL = []

news_repo = [
    'https://www.manifoldtimes.com',
    'https://www.marineinsight.com',
    'https://www.maritime-executive.com',
    'http://www.bunkerworld.com/',
    'https://shipandbunker.com/news',
    'https://splash247.com',
    'https://www.bunkerspot.com/latest-news',
    'https://theloadstar.com/category/news/',
    "https://smartmaritimenetwork.com/category/news/",
    "https://www.seatrade-maritime.com",
    "https://theloadstar.com/category/news/",
    "https://gcaptain.com",
    "https://www.freightwaves.com/american-shipper",
    "https://jpt.spe.org/latest-news",
    "https://unctad.org/publications",
    "https://www.bimco.org/news-and-trends/priority-news",
    "https://iumi.com/news/news",
    "https://cmacgm-group.com/en/news-medias",
    "https://iumi.com/news/news",
    "https://www.imo.org/en/MediaCentre/Pages/default.aspx",
    "https://www.amsa.gov.au/news-community/news-and-media-releases",
    "https://namepa.net/news/",
    "https://www.worldoil.com",
    "https://www.tradewindsnews.com/news"]


for repo in news_repo:
    scrape_article_links = newspaper.build(repo, memoize_articles=True)

    for article in scrape_article_links.articles:

        article_list.append(article.url)
        print(repo)


print(article_list)
print(scrape_article_links.size())


#now we use article features in newspaper to extract what we need

for x in article_list:
    try:
        article_parse = Article(x)
    except Exception:
        pass

    try:
        article_parse.download()
    except Exception:
        pass

    try:
        article_parse.parse()
    except Exception:
        pass

    try:
        article_parse.nlp()
    except Exception:
        pass

    url = x
    title = article_parse.title
    author = article_parse.authors
    summary = article_parse.summary
    keywords = article_parse.keywords
    publishdate = article_parse.publish_date

    #keywordlist
    user_list = ['lng',
                 'lngfuelled',
                 'gaspowered',
                 'vlsfo',
                 'vlsfos',
                 'climate',
                 'ammonia',
                 'decarbonization',
                 'decarbonisation',
                 'imo',
                 'insurance',
                 'bluetech',
                 'imo2020',  #can you search dual terms?
                 'imo2021',
                 'imo2023',
                 'imo2025',
                 'imo2050'
                 'scrubber',
                 'scrubbers',
                 'wind',
                 'liquidnaturalgas',
                 'lngpowered',
                 'fraud',
                 'offspec',
                 'biofuel',
                 'biofuels',
                 'hydrogenpowered',
                 'hydrogen',
                 'lpg',
                 'chain',
                 'ghg',
                 'blue',
                 'cybersecurity',
                 'zeroemission',
                 'stability',
                 'compatibility',
                 'catfines',
                 'blockchain',
                 'ai',
                 'carbon',
                 'zero',
                 'regulatory',
                 'regulations',
                 'regulation',
                 'renewable',
                 'emissions',
                 'green',
                 'sustainability',
                 'offsets',
                 'additives',
                 'supplier',
                 'datasharing',
                 'dualfuel',
                 'dualengine',
                 ]

    matching = []
    for j in keywords:
        for i in user_list:
            if i == j:
                matching.append(j)
    if len(matching) ==0:
        continue

    nlp = spacy.load('en_core_web_sm')
    summary_nlp = nlp(summary)
    summary_nlp_topics = [(word, word.ent_type_) for word in summary_nlp if word.ent_type_]
    corpus.append(summary_nlp_topics)

    write_entity_to_csv = []
    for word in summary_nlp:
        term = word.text
        tag = word.ent_type_
        if tag:
            temp_entity_name = ' '.join([temp_entity_name, term]).strip()
            temp_named_entity = (temp_entity_name, tag)
        else:
            if temp_named_entity:
                named_entities.append(temp_named_entity)
                write_entity_to_csv.append(temp_named_entity)
                temp_entity_name = ''
                temp_named_entity = None

    with open("News Update for " + today.strftime("%B %d, %Y" + ".csv"), 'a', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([extraction_date, title, listToString(matching), summary, url, listToString(keywords), summary_nlp_topics, publishdate])


    print(x)

    Article_title.append(title)
    Article_keyword.append(converttostr(matching, separator))
    Article_summary.append(summary)
    Article_URL.append(url)


    articles_master = list(zip(Article_title, Article_keyword, Article_summary, Article_URL))

def index(req):
    return render(req, 'news/index.html', {'onion_news':articles_master, 'cd_news': Article_URL})
