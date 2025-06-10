import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, timedelta
from scipy.stats import poisson

st.set_page_config(page_title="Under 2.5 Dashboard", layout="wide")

st.title("🔻 Probabilidades de Under 2.5 Gols — Dashboard Interativo")

# ---------------------------------------------------------------------
# 1. Carrega dados históricos
# ---------------------------------------------------------------------
HIST_CSV = "/mnt/data/2025-06-10T02-10_export.csv"  # já enviado via ChatGPT
hist_df = pd.read_csv(HIST_CSV)

# Mantém apenas colunas necessárias
hist_df = hist_df[["HomeTeam", "AwayTeam", "FTHG", "FTAG"]].copy()

# ---------------------------------------------------------------------
# 2. Calcula forças de ataque/defesa (método de Dixon‑Coles simplificado)
# ---------------------------------------------------------------------
league_avg_home_goals = hist_df["FTHG"].mean()
league_avg_away_goals = hist_df["FTAG"].mean()

team_stats = (
    hist_df.groupby("HomeTeam")["FTHG"].mean()
    .to_frame("avg_home_scored")
    .join(hist_df.groupby("HomeTeam")["FTAG"].mean().rename("avg_home_conceded"))
)
team_stats = team_stats.join(
    hist_df.groupby("AwayTeam")["FTAG"].mean().rename("avg_away_scored")
)
team_stats = team_stats.join(
    hist_df.groupby("AwayTeam")["FTHG"].mean().rename("avg_away_conceded")
)

# ---------------------------------------------------------------------
# 3. Função para estimar gols esperados e prob. de Under 2.5
# ---------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def under_probability(home: str, away: str, max_goals: int = 5) -> float:
    """Retorna P(total_goals <= 2.5) via Poisson independente."""
    h_attack = team_stats.loc[home, "avg_home_scored"] / league_avg_home_goals
    a_attack = team_stats.loc[away, "avg_away_scored"] / league_avg_away_goals

    h_def = team_stats.loc[home, "avg_home_conceded"] / league_avg_away_goals
    a_def = team_stats.loc[away, "avg_away_conceded"] / league_avg_home_goals

    exp_h = h_attack * a_def * league_avg_home_goals
    exp_a = a_attack * h_def * league_avg_away_goals

    probs = 0.0
    for hg in range(max_goals + 1):
        for ag in range(max_goals + 1):
            if hg + ag <= 2:
                probs += poisson.pmf(hg, exp_h) * poisson.pmf(ag, exp_a)
    return probs

# ---------------------------------------------------------------------
# 4. Carregar/fetch de próximos jogos
# ---------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def fetch_fixtures() -> pd.DataFrame:
    """Exemplo de fetch de fixtures.
    Substitua por API real. Aqui carregamos um CSV de exemplo ou criamos dummy."""
    try:
        fixtures = pd.read_csv("fixtures.csv")  # precisa ter colunas: Date, HomeTeam, AwayTeam
    except FileNotFoundError:
        today = date.today()
        # Dummy fixtures para demonstração
        fixtures = pd.DataFrame(
            {
                "Date": [today + timedelta(days=i) for i in range(1, 8)],
                "HomeTeam": ["Everton", "Arsenal", "Brighton", "Man City", "Tottenham", "Chelsea", "Liverpool"],
                "AwayTeam": ["West Ham", "Wolves", "Southampton", "Leicester", "Brentford", "Newcastle", "Fulham"],
            }
        )
    return fixtures

fixtures_df = fetch_fixtures()

# ---------------------------------------------------------------------
# 5. Calcular probabilidade de Under 2.5 para cada jogo futuro
# ---------------------------------------------------------------------
probs = []
for _, row in fixtures_df.iterrows():
    ht, at = row["HomeTeam"], row["AwayTeam"]
    if ht in team_stats.index and at in team_stats.index:
        prob = under_probability(ht, at)
    else:
        prob = np.nan  # times não presentes no histórico
    probs.append(prob)

fixtures_df["ProbUnder2.5"] = probs
fixtures_df = fixtures_df.dropna(subset=["ProbUnder2.5"]).sort_values("ProbUnder2.5", ascending=False)

st.subheader("📅 Próximos Jogos com Maior Probabilidade de Under 2.5 Gols")
st.dataframe(
    fixtures_df.assign(ProbUnder2.5=lambda x: (x["ProbUnder2.5"] * 100).round(1)).rename(
        columns={"ProbUnder2.5": "Under 2.5 %"}
    )
)

# ---------------------------------------------------------------------
# 6. Estratégia Automatizada (exibição)
# ---------------------------------------------------------------------
st.markdown("""
### 🤖 Estratégia Automatizada
- **Filtro:** Apostar em Under 2.5 quando ProbUnder2.5 ≥ 60%.
- **Gestão de Banca:** Apostar 1‑2% da banca por aposta.
- **Revisão Diária:** Atualizar fixture e recomputar probabilidades.
""")

# ---------------------------------------------------------------------
# 7. Download dos dados
# ---------------------------------------------------------------------
csv_under = fixtures_df.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Baixar lista de Under 2.5 em CSV",
    data=csv_under,
    file_name="under25_fixtures.csv",
    mime="text/csv",
)
