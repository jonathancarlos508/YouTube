import streamlit as st
import pandas as pd
from datetime import date
import base64

st.title("Jogos do Dia")

dia = st.date_input("Data de Análise", date.today())

@st.cache_data
def load_data_jogos(d):
    url = (
        "https://github.com/jonathancarlos508/YouTube/blob/main/"
        f"Jogos_do_Dia/FootyStats/Jogos_do_Dia_FootyStats_{d}.csv?raw=true"
    )
    return pd.read_csv(url)

df_jogos = load_data_jogos(dia)

st.dataframe(df_jogos)

# ---- DOWNLOAD COMO CSV -------------------------------------------------
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = (
        f'<a href="data:file/csv;base64,{b64}" '
        f'download="Jogos_{dia}.csv">Baixar CSV</a>'
    )
    return href

st.markdown(filedownload(df_jogos), unsafe_allow_html=True)
