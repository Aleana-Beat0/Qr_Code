# example/st_app.py
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

url = "https://docs.google.com/spreadsheets/d/1v4fTbihZMWGP4xqKtYh_drO7KkVU4wcaty2gZ8GmkDY/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetsConnection)

data = conn.read(spreadsheet=url, usecols=[1])
st.dataframe(data)

column_1 = data.iloc[:, 0] 
with pd.option_context('display.max_rows', None):
        print(column_1)