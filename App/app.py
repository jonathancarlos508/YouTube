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
  
  if selected_league == 'England':
    league = 'E0'
    if selected_league == 'Germany':
    league = 'D1'
    if selected_league == 'Italy':
    league = 'I1'
    if selected_league == 'Spain':
    league = 'SP1'
    if selected_league == 'France':
    league = 'F1'
    
    if selected_season == '2024/2025':
    season = '2425'
    if selected_season == '2023/2024':
    season = '2324'
    if selected_season == '2022/2023':
    season = '2223'
    
    url = "https://www.football-data.co.uk/mmz4281/"+season+"/"+league+".csv"
    data = pd.read_csv(url)
    return data

df = loead_data(selected_league, selected_season)

st.subheader("Dataframe: "+selected_league)
st.dataframe(df)
