import pandas as pd
import numpy as np
import bs4
from bs4 import BeautifulSoup as bs
import requests
import streamlit as sl

stocks_page_response = requests.get("https://www.moneycontrol.com/news/business/stocks/")
stocks_soup = bs(stocks_page_response.content,"html.parser")

hot_stocks_url = ""
date = ""
for link in stocks_soup.find_all('a'):
    text = link.text
    substring = "Hot Stocks"

    if substring in text:
        hot_stocks_url = link.get('href')
        parent = link.parent.parent
        date = parent.span.get_text()
        break

url_page_response = requests.get(hot_stocks_url)
url_soup = bs(url_page_response.content,"html.parser") #star section

stocks_list = [] #storing the headings containing ltp

for heading in url_soup.find_all('strong'):
    text = heading.text
    ltp = "LTP"
    target = "Target"

    if ltp in text:
        split = text.split("|")
        stocks_list.append(split)
    elif target in text:
        split = text.split("|")
        stocks_list.append(split)


stocks_df = pd.DataFrame(stocks_list)
headers = ["Stock-Name","LTP","Stop-Loss","Target","Return"]
stocks_df.columns = headers

stocks_df[['Stock-Name','Buy-Sell']] = stocks_df['Stock-Name'].str.split(': ',expand=True)

stocks_df['LTP'] = stocks_df['LTP'].str.replace('LTP: Rs','')
stocks_df['LTP'] = stocks_df['LTP'].str.replace('CMP: Rs','')

stocks_df['Stop-Loss'] = stocks_df['Stop-Loss'].str.replace('Stop-Loss:','')
stocks_df['Stop-Loss'] = stocks_df['Stop-Loss'].str.replace('Rs','')

stocks_df['Target'] = stocks_df['Target'].str.replace('Target: Rs','')

stocks_df['Return'] = stocks_df['Return'].str.replace('Return: ','')

stocks_df['Return'] = stocks_df['Return'].str.replace('percent','')

print(stocks_df)

sl.write(
"""
# Hot Stocks of the day
"""
)

sl.table(stocks_df)
