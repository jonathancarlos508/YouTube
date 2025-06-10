import streamlit as st
import pandas as pd
from datetime import date

st.title("Jogos do Dia")

dia = st.date_input("Data de Análise", date.today())

@st.cache_data  # opcional, mas acelera o app se você abrir a mesma data várias vezes
def load_data_jogos(d):
    url = (
        "https://github.com/jonathancarlos508/YouTube/blob/main/"
        f"Jogos_do_Dia/FootyStats/Jogos_do_Dia_FootyStats_{d}.csv?raw=true"
    )
    return pd.read_csv(url)

df_jogos = load_data_jogos(dia)

st.dataframe(df_jogos)
