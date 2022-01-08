import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
import requests
import streamlit as sl

main_url = "https://www.moneycontrol.com/news/business/stocks/page-"

def get_url_list(main_url):

    url_list = []

    for i in range(1,10):
        page_url = main_url+str(i)+'/'
        page_response = requests.get(page_url)
        page_soup = bs(page_response.content,"html.parser")

        for link in page_soup.find_all('a'):
            text = link.text
            if "Hot Stocks" in text:
                parent = link.parent.parent
                date = parent.span.text
                url_list.append([date,text,link.get('href')])
    
    return url_list

def get_price_list(page_url):

    price_list = []
    page_response = requests.get(page_url)
    page_soup = bs(page_response.content,"html.parser")

    for heading in page_soup.find_all('strong'):
        text = heading.text
        ltp = "LTP"
        target = "Target"

        if ltp in text:
            split = text.split(":")
            price_list.append(split)
        elif target in text:
            split = text.split(":")
            price_list.append(split)
    
    return price_list

url_list = get_url_list(main_url)

def make_table():
    
    datewise_list = []

    for i in range(len(url_list)):
            date = url_list[i][0]
            price_list = get_price_list(url_list[i][2])
            datewise_list.append([date,price_list])
    
    return datewise_list

make_table()