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

dados2026 = players_2026.merge(teams_2026[["club_id","competition_name","country_name"]],left_on="current_club_id",right_on="club_id",how="left"
)

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

with tab2:

    st.header("⚽ Copa do Mundo 2026")


    scorers = pd.DataFrame(dados_api["scorers"])


    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🏅 Artilheiros",
        len(scorers)
    )

    col2.metric(
        "⚽ Maior nº de gols",
        scorers["goals"].max()
    )

    col3.metric(
        "🏟️ Clubes",
        dados2026["current_club_name"].nunique()
    )

    st.divider()

    # Filtro
    liga = st.selectbox(
        "Liga",
        ["Todas"] + sorted(
            dados2026["competition_name"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    dados_filtrado = dados2026.copy()

    if liga != "Todas":
        dados_filtrado = dados_filtrado[
            dados_filtrado["competition_name"] == liga
        ]

    col1, col2 = st.columns(2)

    # Top 10 Clubes

    clubes = (
        dados_filtrado
        .groupby("current_club_name")
        .size()
        .reset_index(name="Jogadores")
        .sort_values("Jogadores", ascending=False)
        .head(10)
    )

    fig1 = px.bar(
        clubes,
        x="Jogadores",
        y="current_club_name",
        orientation="h",
        text="Jogadores",
        color="Jogadores",
        title="🏟️ Top 10 clubes com mais jogadores"
    )

    fig1.update_layout(
        height=450,
        yaxis=dict(categoryorder="total ascending"),
        showlegend=False,
        title_x=0.5
    )

    col1.plotly_chart(fig1, use_container_width=True)

    # Top 10 Ligas
    ligas = (
        dados_filtrado
        .groupby("competition_name")
        .size()
        .reset_index(name="Jogadores")
        .sort_values("Jogadores", ascending=False)
        .head(10)
    )

    fig2 = px.bar(
        ligas,
        x="competition_name",
        y="Jogadores",
        text="Jogadores",
        color="Jogadores",
        title="🏆 Top 10 ligas com mais jogadores"
    )

    fig2.update_layout(
        height=450,
        showlegend=False,
        title_x=0.5,
        xaxis_title="Liga",
        yaxis_title="Jogadores"
    )

    col2.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)


    # Top 10 Países
    paises = (
        dados_filtrado
        .groupby("country_name")
        .size()
        .reset_index(name="Jogadores")
        .sort_values("Jogadores", ascending=False)
        .head(10)
    )

    fig3 = px.bar(
        paises,
        x="Jogadores",
        y="country_name",
        orientation="h",
        text="Jogadores",
        color="Jogadores",
        title="🌍 Top 10 países dos clubes"
    )

    fig3.update_layout(
        height=450,
        yaxis=dict(categoryorder="total ascending"),
        showlegend=False,
        title_x=0.5
    )

    col3.plotly_chart(fig3, use_container_width=True)

    # Top 10 Países
    paises = (
        dados_filtrado
        .groupby("country_name")
        .size()
        .reset_index(name="Jogadores")
        .sort_values("Jogadores", ascending=False)
        .head(10)
    )

    fig3 = px.bar(
        paises,
        x="Jogadores",
        y="country_name",
        orientation="h",
        text="Jogadores",
        color="Jogadores",
        title="🌍 Top 10 países dos clubes"
    )

    fig3.update_layout(
        height=450,
        yaxis=dict(categoryorder="total ascending"),
        showlegend=False,
        title_x=0.5
    )

    col3.plotly_chart(fig3, use_container_width=True)

    # Top 10 Artilheiros
    fig4 = px.bar(
        scorers.head(10),
        x="goals",
        y="name",
        orientation="h",
        text="goals",
        color="goals",
        title="🥇 Top 10 artilheiros da Copa"
    )

    fig4.update_layout(
        height=450,
        yaxis=dict(categoryorder="total ascending"),
        showlegend=False,
        title_x=0.5
    )

    col4.plotly_chart(fig4, use_container_width=True)
