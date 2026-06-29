import streamlit as st
import pandas as pd
import requests
import plotly.express as px

#API da Copa 2026
url = "https://wcup2026.org/api/data.php?action=scorers"
dados = requests.get(url).json()

#Jogadores(Jogadores e times)
BASE_PATH_2026 = "Dados/Jogadores"
players_2026 = pd.read_csv(f"{BASE_PATH_2026}/df_players.csv")
teams_2026 = pd.read_csv(f"{BASE_PATH_2026}/df_teams.csv")
national_team_2026 = pd.read_csv(f"{BASE_PATH_2026}/df_national_team.csv")

#copa de 1930 a 2022
BASE_PATH = "Dados/Copas(1930-2022)"
tournaments = pd.read_csv(f"{BASE_PATH}/tournaments.csv")
matches = pd.read_csv(f"{BASE_PATH}/matches.csv")
goals = pd.read_csv(f"{BASE_PATH}/goals.csv")
teams = pd.read_csv(f"{BASE_PATH}/teams.csv")
players = pd.read_csv(f"{BASE_PATH}/players.csv")
