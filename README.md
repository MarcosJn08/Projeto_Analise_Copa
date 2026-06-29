# 🏆 Dashboard das Copas do Mundo

Dashboard interativo desenvolvido com **Streamlit** para análise histórica das Copas do Mundo (1930–2022) e analise em tempo real da **Copa do Mundo 2026**.

---

## 📋 Sobre o Projeto
Link no Streamlit:
https://geihnt38xdyhu9xgmqijlj.streamlit.app/


O projeto tem 3 fontes de Dados

- **Histórico das copa de 1930 a2022:** análise de torneios, partidas, gols e artilheiros de todas as edições da Copa do Mundo masculina.
- **Copa 2026:** dados ao vivo dos artilheiros via API pública e 
- **Dados dos Jogadores:** informações dos jogadores convocados (clubes, ligas e países).

## ✨ Funcionalidades

### Aba 1 — Copa (1930–2022)
- Filtro: Você pode filtrar a seleção a qual você quer ver os dados e as copas que você quer ver
- Métricas: total de copas, jogos, gols e seleções participantes
- Tabela de partidas com placar e data
- Gráfico de linha: média de gols por Copa ao longo dos anos
- Gráfico de barras: Top 10 artilheiros que mais fizeram gols
- Gráfico de barras: quantidade de jogos por edição da copa

### Aba 2 — Copa 2026
- Dados em tempo real com a API (`https://wcup2026.org/api/data.php?action=scorers`)
- Métricas: total de artilheiros, maior número de gols e clubes representados
- Filtro por ligas a qual os times dos jogadores convocados jogam
- Top 10 clubes com mais jogadores convocados
- Top 10 ligas com mais jogadores convocados
- Top 10 países-sede dos clubes
- Top 10 artilheiros da Copa 2026

---

## 🗂️ Estrutura do Projeto

```
Projeto_Analise_Copa/
│
├── app.py                          
├── requirements.txt                
│
└── Dados/
    ├── Jogadores/                  # Dados dos jogadores (Copa 2026)
    │   ├── df_players.csv          # Jogadores convocados
    │   ├── df_teams.csv            # Clubes
    │   └── df_national_team.csv    # Seleções nacionais
    │
    └── Copas(1930-2022)/           # Dados históricos das Copas
        ├── tournaments.csv         # Edições dos torneios
        ├── matches.csv             # Partidas
        ├── goals.csv               # Gols
        ├── players.csv             # Jogadores
        ├── teams.csv               # Seleções
        ├── squads.csv              # Elencos
        ├── bookings.csv            # Cartões
        ├── penalty_kicks.csv       # Pênaltis
        ├── substitutions.csv       # Substituições
        ├── group_standings.csv     # Classificação por grupos
        ├── award_winners.csv       # Premiados
        └── ... (demais tabelas)
```


## 🌐 API Utilizada

- **Endpoint:** `https://wcup2026.org/api/data.php?action=scorers`
- **Repositorio:** `https://github.com/salah23222/worldcup2026/tree/main`


## 📊 Fontes Dos arquivos CSV

- **Copa 2026 — Jogadores:** dados de jogadores e clubes obtidos no repositorio: `https://github.com/julyaW11/fifa-world-cup-2026-pre-tournament-analysis/tree/main`

- **Histórico 1930–2022:** Dados das Copas de 1930 a 2022 foram obtidas nesse repositório: `https://github.com/jfjelstul/worldcup/tree/master/data-csv`
