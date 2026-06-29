import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(
    page_title="Dashboard das Copas",
    layout="wide"
)

st.title("🏆 Dashboard das Copas do Mundo")

#API Copa 2026
url = "https://wcup2026.org/api/data.php?action=scorers"
dados = requests.get(url).json()

#Dados Jogadores
BASE_PATH_2026 = "Dados/Jogadores"
players_2026 = pd.read_csv(f"{BASE_PATH_2026}/df_players.csv")
teams_2026 = pd.read_csv(f"{BASE_PATH_2026}/df_teams.csv")
national_team_2026 = pd.read_csv(f"{BASE_PATH_2026}/df_national_team.csv")

# DADOS COPAS (1930-2022)
BASE_PATH = "Dados/Copas(1930-2022)"
tournaments = pd.read_csv(f"{BASE_PATH}/tournaments.csv")
matches = pd.read_csv(f"{BASE_PATH}/matches.csv")
goals = pd.read_csv(f"{BASE_PATH}/goals.csv")
teams = pd.read_csv(f"{BASE_PATH}/teams.csv")
players = pd.read_csv(f"{BASE_PATH}/players.csv")

selecoes = sorted(teams["team_name"].unique())
anos = sorted(tournaments["year"].unique())

tab1, tab2 = st.tabs([
    "Copa (1930–2022)",
    "Copa 2026"
])

with tab1:

    st.header("Análise Histórica das Copas")


    st.sidebar.header("Filtros")

    selecoes = sorted(teams["team_name"].unique())

    selecao = st.sidebar.selectbox(
        "Seleção",
        ["Todas"] + selecoes
    )

    anos = sorted(tournaments["year"].unique())

    ano_inicio, ano_fim = st.sidebar.select_slider(
        "Período",
        options=anos,
        value=(anos[0], anos[-1])
    )

    tournaments_filtrado = tournaments[
        (tournaments["year"] >= ano_inicio) &
        (tournaments["year"] <= ano_fim)
    ]

    ids_torneios = tournaments_filtrado["tournament_id"]

    matches_filtrado = matches[
        matches["tournament_id"].isin(ids_torneios)
    ]

    if selecao != "Todas":

        matches_filtrado = matches_filtrado[
            (matches_filtrado["home_team_name"] == selecao) |
            (matches_filtrado["away_team_name"] == selecao)
        ]

    goals_filtrado = goals[
        goals["match_id"].isin(matches_filtrado["match_id"])
    ]



    total_copas = tournaments_filtrado["tournament_id"].nunique()
    total_jogos = matches_filtrado["match_id"].nunique()
    total_gols = len(goals_filtrado)
    total_selecoes = teams["team_name"].nunique()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🏆 Copas", total_copas)
    col2.metric("⚽ Jogos", total_jogos)
    col3.metric("🥅 Gols", total_gols)
    col4.metric("🌍 Seleções", total_selecoes)

    st.divider()

    st.subheader("Tabela de Partidas")

    tabela = matches_filtrado[["match_name", "score", "match_date",]]

    st.dataframe(tabela, use_container_width=True, hide_index=True)

with tab2:

    st.header("⚽ Copa do Mundo 2026")
