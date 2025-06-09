import streamlit as st
import pandas as pd
import numpy as np

st.title("Web App Football Data")

st.sidebar.header("Leagues")
selected_league = st.sidebar.selectbox('League',['England','Germany','Italy','Spain','France'])

st.sidebar.header("Season")
select_season = st.sidebar.selectbox('Season',['2024/2025','2024/2023',2023/2022])
                                               
# WebScraping Football Data

def load_data(league,season):
  url = "https://www.football-data.co.uk/mmz4281/"+season+"/"+league+".csv"
  data = pd.read_csv(url)
  return data

df = loead_data(selected_league, selected_season)
