import streamlit as st
import pandas as pd
from datetime import date
import base64 

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

def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a hred="data:file/csv;base64,{b64}" download="Base_Dados.csv">Download CSV File</a>
    return href

    st.markdown(filedownload(df), unsafe_allow_html=True)
