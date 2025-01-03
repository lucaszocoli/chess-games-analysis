import pandas as pd
import chess.pgn
import os
import matplotlib.pyplot as plt

eco_codes_df = pd.read_csv("data/csv/eco_codes.csv")

matches_data = []

pgn_folder = "data/pgn"
pgn_files = os.listdir(pgn_folder)

for file in pgn_files:
    file_path = f"{pgn_folder}/{file}"
    with open(file_path) as pgn_file:
        while True:
            game = chess.pgn.read_game(pgn_file)

            if game is None:
                break

            headers = game.headers
            matches_data.append({
                "Event": headers.get("Event", "Desconhecido"),
                "Site": headers.get("Site", "Desconhecido"),
                "Date": headers.get("Date", "Desconhecido"),
                "Round": headers.get("Round", "Desconhecido"),
                "WhitePlayer": headers.get("White", "Desconhecido"),
                "BlackPlayer": headers.get("Black", "Desconhecido"),
                "Result": headers.get("Result", "Desconhecido"),
                "WhitePlayerElo": headers.get("WhiteElo", "Desconhecido"),
                "BlackPlayerElo": headers.get("BlackElo", "Desconhecido"),
                "ECO": headers.get("ECO", "Desconhecido"),
            })

matches_df = pd.DataFrame(matches_data)

matches_df = matches_df.merge(eco_codes_df, left_on="ECO", right_on="eco", how="left")
matches_df = matches_df.drop(columns=["eco", "eco_example", "eco_type", "eco_group"])
matches_df = matches_df.rename(columns={"eco_name": "Opening Name"})

result_counts = matches_df.groupby(['Opening Name', 'Result']).size().unstack(fill_value=0)

top_white_wins = result_counts['1-0'].nlargest(5)
top_black_wins = result_counts['0-1'].nlargest(5)
top_draws = result_counts['1/2-1/2'].nlargest(5)

fig, ax = plt.subplots(figsize=(10, 6))
top_white_wins.plot(kind='barh', color='skyblue', ax=ax)
ax.set_title('Top 5 Aberturas com Mais Vitórias de Brancas')
ax.set_xlabel('Número de Vitórias')
ax.set_ylabel('Abertura')
ax.bar_label(ax.containers[0])
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
top_black_wins.plot(kind='barh', color='lightcoral', ax=ax)
ax.set_title('Top 5 Aberturas com Mais Vitórias de Pretas')
ax.set_xlabel('Número de Vitórias')
ax.set_ylabel('Abertura')
ax.bar_label(ax.containers[0])
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
top_draws.plot(kind='barh', color='lightgreen', ax=ax)
ax.set_title('Top 5 Aberturas com Mais Empates')
ax.set_xlabel('Número de Empates')
ax.set_ylabel('Abertura')
ax.bar_label(ax.containers[0])
plt.show()
