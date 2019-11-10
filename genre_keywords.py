# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 13:10:54 2019

@author: Arunav Saikia
"""

import bs4
import pandas as pd
import json
from requests import get
import re
import difflib
from time import sleep

df = pd.read_csv('./extra_movies.csv')

def scrape_genre_keywords(name):
    print(name)
    clean_name = name.replace(' ', '+')
    url =  'https://www.the-numbers.com/search?searchterm=' + clean_name
    try:
        response = get(url)
    except:
        sleep(600)
        response = get(url)
        
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    
    try:
        movie_name = soup.find_all('h1')[0].text
    except: 
        movie_name = None
    try:
        movie_container = soup.find_all('table')[3].find_all('tr')
    except:
        genre = None
        keywords = None
    
    def getIndexGenre(movie_container):
        for index, value in enumerate(movie_container):
            if value.td.b.text == 'Genre:':
                return index
            
    def getIndexKeyword(movie_container):
        for index, value in enumerate(movie_container):
            if value.td.b.text == 'Keywords:':
                return index
    try:
        i = getIndexGenre(movie_container)
        genre = movie_container[i].find_all('td')[1].text
    except:
        genre = None
    try:
        j = getIndexKeyword(movie_container)
        keywords_tmp = movie_container[j].find_all('a')
        keywords = [keyword.text for keyword in keywords_tmp]
    except: 
        keywords = None
    return [name,movie_name, genre, keywords]

new_df = pd.DataFrame(list(map(scrape_genre_keywords, df['Movie'])),\
                  columns = ['query_name', 'scrapped_name', 'genre', 'keywords'])

scrapped_name = actor_container.find_all('td')[1].text
scrapped_url = 'https://www.the-numbers.com' + actor_container.find_all('td')[1].a.get('href') \+ '#tab=acting'
scrapped_match = actor_container.find_all('td')[0].text