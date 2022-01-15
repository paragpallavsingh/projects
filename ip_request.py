'''
A few weeks ago #google has released the IP ranges for Googlebot allowing #SEO to more easily verify if a server request is really from Google or just someone impersonating it.
'''

import ipaddress
import requests
import pandas as pd
import base64
import streamlit as st
api = "https://developers.google.com/search/apis/ipranges/googlebot.json"

def getIPfromPrefix(ipPrefix):
	lst_ips = [str(ip) for ip in ipaddress. IPv4Network( ipPrefix)]
	return lst_ips
r = requests.get(api).json()

prefixLst = [resp['ipv4Prefix'] for resp in r["prefixes"] if 'ipv4Prefix' in resp]
df_pref_list = pd.DataFrame(prefixLst)

full_lst = [getIPfromPrefix(i) for i in prefixLst]
df_full_lst = pd.DataFrame(full_lst)

#Streamlit start design
st.set_page_config(page_title="List of IP")
st.title("***Full List of IP ranges for Googlebot***", anchor=None)

st.table(df_full_lst)
st.write('For more info, check this [post](https://www.linkedin.com/posts/activity-6888066374522949632-iGS6/) by Mirko Obkircher')
csv = df_full_lst.to_csv()
b64 = base64.b64encode(csv.encode()).decode()
st.markdown('### **⬇️ Download output CSV File **')
href = f"""<a href="data:file/csv;base64,{b64}">Download CSV File</a> (Right-click and save as "filename.csv". Don't left-click)"""
st.markdown(href, unsafe_allow_html=True)

