import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(
    page_title="Dashboard das Copas",
    layout="wide"
)

st.title("🏆 Dashboard das Copas do Mundo")


# API Copa 2026
url = "https://wcup2026.org/api/data.php?action=scorers"
dados_api = requests.get(url).json()

# Dados Jogadores
BASE_PATH_2026 = "Dados/Jogadores"

players_2026 = pd.read_csv(f"{BASE_PATH_2026}/df_players.csv")
teams_2026 = pd.read_csv(f"{BASE_PATH_2026}/df_teams.csv")
national_team_2026 = pd.read_csv(f"{BASE_PATH_2026}/df_national_team.csv")

# Dados Copa 1930 - 2022
BASE_PATH = "Dados/Copas(1930-2022)"

tournaments = pd.read_csv(f"{BASE_PATH}/tournaments.csv")
matches = pd.read_csv(f"{BASE_PATH}/matches.csv")
goals = pd.read_csv(f"{BASE_PATH}/goals.csv")
teams = pd.read_csv(f"{BASE_PATH}/teams.csv")
players = pd.read_csv(f"{BASE_PATH}/players.csv")

players = players[players["female"] == False]

tab1, tab2 = st.tabs([
    "Copa (1930–2022)",
    "Copa 2026"
])

with tab1:

    st.header("Análise Histórica das Copas")

    st.sidebar.header("Filtros")

    selecoes = sorted(teams["team_name"].unique())
    anos = sorted(tournaments["year"].unique())

    selecao = st.sidebar.selectbox(
        "Seleção",
        ["Todas"] + selecoes
    )

    ano_inicio, ano_fim = st.sidebar.select_slider("Período",options=anos,value=(anos[0], anos[-1]))

    # Filtros
    tournaments_filtrado = tournaments[(tournaments["year"] >= ano_inicio) &(tournaments["year"] <= ano_fim)]

    ids_torneios = tournaments_filtrado["tournament_id"]

    matches_filtrado = matches[matches["tournament_id"].isin(ids_torneios)]

    if selecao != "Todas":
        matches_filtrado = matches_filtrado[(matches_filtrado["home_team_name"] == selecao) |(matches_filtrado["away_team_name"] == selecao)]

    goals_filtrado = goals[goals["match_id"].isin(matches_filtrado["match_id"])]

    # Métricas
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

    tabela = matches_filtrado[["match_name", "score", "match_date"]]

    st.dataframe(tabela,use_container_width=True,hide_index=True)

    # Calculos
    gols_por_copa = (goals_filtrado.groupby("tournament_id").size().reset_index(name="total_gols"))

    jogos_por_copa = (matches_filtrado.groupby("tournament_id").size().reset_index(name="total_jogos"))

    media_gols = pd.merge(gols_por_copa,jogos_por_copa,on="tournament_id")
    media_gols["media_gols"] = (media_gols["total_gols"] /media_gols["total_jogos"])
    media_gols = media_gols.merge(tournaments[["tournament_id", "year"]],on="tournament_id")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.line(
            media_gols,
            x="year",
            y="media_gols",
            markers=True,
            title="📈 Média de gols por Copa"
        )

        fig.update_layout(
            title_x=0.5,
            xaxis_title="Ano",
            yaxis_title="Média"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:
        artilheiros = (
            goals_filtrado
            .groupby("player_id")
            .size()
            .reset_index(name="gols")
        )

        artilheiros = artilheiros.merge(
            players,
            on="player_id"
        )

        artilheiros["player_name"] = (
            artilheiros["given_name"].fillna("") +
            " " +
            artilheiros["family_name"].fillna("")
        ).str.strip()

        top10 = (
            artilheiros
            .sort_values(
                "gols",
                ascending=False
            )
            .head(10)
        )

        fig = px.bar(
            top10,
            x="gols",
            y="player_name",
            orientation="h",
            text="gols",
            title="🥇 Top 10 Artilheiros"
        )

        fig.update_layout(
            title_x=0.5,
            xaxis_title="Gols",
            yaxis_title="",
            yaxis=dict(
                categoryorder="total ascending"
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    col3, col4 = st.columns(2)

    with col3:
        jogos_copa = (
            matches_filtrado
            .groupby("tournament_id")
            .size()
            .reset_index(name="Quantidade de Jogos")
        )

        jogos_copa = jogos_copa.merge(
            tournaments[
                ["tournament_id", "year"]
            ],
            on="tournament_id"
        )

        fig = px.bar(
            jogos_copa,
            x="year",
            y="Quantidade de Jogos",
            text="Quantidade de Jogos",
            title="📊 Quantidade de Jogos por Copa"
        )

        fig.update_layout(
            title_x=0.5,
            xaxis_title="Ano",
            yaxis_title="Jogos"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col4:
        st.info("Sem nada")