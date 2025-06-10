import streamlit as st
import panddas as pd
import numpy as np
import datetime
from datetime import date

st.title("Jogos do Dia")

dia = st.date_input(
"Data de Análise",
  date.today())
