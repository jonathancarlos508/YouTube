import streamlit as st
import pandas as pd
import numpy as np
import datetime
from datetime import date

st.title("Jogos do Dia")

dia = st.date_input(
"Data de Análise",
  date.today())

def load_data_jogos():
  data_jogos = pd.read_csv("https://github.com/jonathancarlos508/YouTube/blob/main/Jogos_do_Dia/FootyStats/Jogos_do_Dia_FootyStats_"+str(dia)+".csv?raw=true")

return data_jogos

df_jogos = load_data_jogos()

st.dataframe(df_jogos)
