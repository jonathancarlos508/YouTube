import streamlit as st
import pandas as pd

st.title("Web App Football Data")

# Sidebar – seleção de liga e temporada
st.sidebar.header("Leagues")
selected_league = st.sidebar.selectbox(
    "League",
    ["England", "Germany", "Italy", "Spain", "France"],
)

st.sidebar.header("Season")
selected_season = st.sidebar.selectbox(
    "Season",
    ["2024/2025", "2023/2024", "2022/2023"],
)


@st.cache_data  # armazena em cache o resultado para acelerar a aplicação
def load_data(selected_league: str, selected_season: str) -> pd.DataFrame:
    """Faz o download do CSV da football‑data.co.uk para a liga e temporada escolhidas."""

    league_codes = {
        "England": "E0",
        "Germany": "D1",
        "Italy": "I1",
        "Spain": "SP1",
        "France": "F1",
    }

    season_codes = {
        "2024/2025": "2425",
        "2023/2024": "2324",
        "2022/2023": "2223",
    }

    league = league_codes.get(selected_league)
    season = season_codes.get(selected_season)

    if league is None or season is None:
        st.error("Liga ou temporada desconhecida. Verifique as seleções.")
        return pd.DataFrame()

    url = f"https://www.football-data.co.uk/mmz4281/{season}/{league}.csv"
    data = pd.read_csv(url)
    return data


# Carrega os dados com base nas escolhas do usuário
try:
    df = load_data(selected_league, selected_season)
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    df = pd.DataFrame()

# Mostra o DataFrame na tela
st.subheader(f"Dataframe: {selected_league} ({selected_season})")
if not df.empty:
    st.dataframe(df)
else:
    st.info("Nenhum dado para exibir.")


