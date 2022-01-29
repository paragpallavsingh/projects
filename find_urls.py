from cgitb import text
from operator import le
# from classes import Page
import base64
import pandas as pd
import requests
import streamlit as st
from bs4 import BeautifulSoup
import requests

st.set_page_config(page_title="SEO Report of Website")
st.title("***SEO Review by Parag Pallav Singh***", anchor=None)

url_input = st.text_area("Enter URL to look. (ex. https://currentdomain.com/current-page)", height=20)
submit = st.button(label='Get the List')

if submit:

    #scraping
    page_source = requests.get(url_input).text
    soup = BeautifulSoup(page_source, 'html.parser')
    urls_list = [item.get('href') for item in soup.article.find_all('a')]
    text_list = [item.text for item in soup.article.find_all('a')]

    #dataframe
    df = pd.DataFrame(urls_list,text_list)

    #streamlit
    st.table(df)
    csv = df.to_csv()        
    b64 = base64.b64encode(csv.encode()).decode()
    st.markdown('### **⬇️ Download output CSV File **')
    href = f"""<a href="data:file/csv;base64,{b64}">Download CSV File</a> (Right-click and save as "filename.csv". Don't left-click)"""
    st.markdown(href, unsafe_allow_html=True)
