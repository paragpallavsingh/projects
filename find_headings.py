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
    h1_list = [item.text for item in soup.body.find_all('h1')]
    h2_list = [item.text for item in soup.body.find_all('h2')]
    h3_list = [item.text for item in soup.body.find_all('h3')]
    h4_list = [item.text for item in soup.body.find_all('h4')]
    h5_list = [item.text for item in soup.body.find_all('h5')]
    h6_list = [item.text for item in soup.body.find_all('h6')]
    
    

    #dataframe
    df = pd.DataFrame({'h1':pd.Series(h1_list),
                        'h2':pd.Series(h2_list),
                        'h3':pd.Series(h3_list),
                        'h4':pd.Series(h4_list),
                        'h5':pd.Series(h5_list),
                        'h6':pd.Series(h6_list)
                        })

    #streamlit
    st.write(
        "All the headings in the page🏹: "+url_input
    )
    st.table(df.transpose())
    csv = df.to_csv()        
    b64 = base64.b64encode(csv.encode()).decode()
    st.markdown('### **⬇️ Download output CSV File **')
    href = f"""<a href="data:file/csv;base64,{b64}">Download CSV File</a> (Right-click and save as "filename.csv". Don't left-click)"""
    st.markdown(href, unsafe_allow_html=True)
