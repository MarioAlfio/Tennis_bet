import numpy as np
import pandas as pd
from stats_ritiro import calculate_losses_by_ret, calculate_total_matches, calculate_means, create_boxplot
from scomponi_score import extract_scores, calculate_winner_loser_score
from db_config import connect_to_db, DatabaseManager
import matplotlib.pyplot as plt
import seaborn as sns

# Funzione principale
def main():
    data = pd.read_csv("./data_csv/atp_matches_qual_chall_2022.csv", sep=",")
    data_2 = pd.read_csv("./data_csv/atp_matches_qual_chall_2023.csv", sep=",")
    data_3 = pd.read_csv("./data_csv/atp_matches_qual_chall_2024.csv", sep=",")

    # Concatenate DataFrames vertically
    df = pd.concat([data, data_2, data_3], axis=0, ignore_index=True)

    df.drop(['match_num'], axis=1, inplace=True)

    df['tourney_date'] = pd.to_datetime(df['tourney_date'], format='%Y%m%d')

    # TROVARE STAGIONI SARA

# Analisi dei Ritiri per ogni giocatore
    df['ritiro'] = np.logical_or(
    np.char.find(df['score'].values.astype(str), 'RET') >= 0,
    np.char.find(df['score'].values.astype(str), 'W/O') >= 0
    )

    calcolo_ritiro = df[['winner_id', 'winner_name', 'loser_id', 'loser_name',
                         'score', 'ritiro', 'best_of', 'round', 'minutes']].copy()

    # Calcolo match totali e ritiri
    player_matches = calculate_total_matches(calcolo_ritiro)
    df_loser_ret = calculate_losses_by_ret(calcolo_ritiro)

    # Calcolo delle medie
    merged_data = calculate_means(player_matches, df_loser_ret)

    merged_data.describe()

    # Creazione dei grafici
    create_boxplot(merged_data['total_matches'], 
               "Distribuzione Totale Match Disputati", "Totale Match")
    
    create_boxplot(df_loser_ret['losses_by_ret'], 
               "Distribuzione dei Match Persi per Ritiro", "Match Persi per Ritiro")
    
    plt.figure(figsize=(12, 6))
    sns.scatterplot(x='total_matches', y='mean', data=merged_data, alpha=0.7)
    for i, row in merged_data.iterrows():
        plt.text(row['total_matches'], row['weighted_mean'])
    plt.title("Scatter Plot - Distribuzione Media Ponderata (Ritiri/Match Totali)")
    plt.xlabel("Totale Match")
    plt.ylabel("Media Ponderata")
    plt.grid(True)
    plt.show()

    # Salvataggio nel database - AGGIUNGERE TRY EXCEPT
    engine = connect_to_db()
    db_manager = DatabaseManager(engine)
    db_manager.insert_data('ritiro_stats', merged_data)

    print("Dati elaborati e salvati con successo nel database PostgreSQL.")

# split del campo stringa score

    df.drop(['score'], axis=1, inplace=True)

    score_cols = ['score_1set_w', 'score_1set_l', 'score_tiebreak_1set_l', 
              'score_2set_w', 'score_2set_l', 'score_tiebreak_2set_l',
              'score_3set_w', 'score_3set_l', 'score_tiebreak_3set_l',
              'score_4set_w', 'score_4set_l', 'score_tiebreak_4set_l',
              'score_5set_w', 'score_5set_l', 'score_tiebreak_5set_l']

    df[score_cols] = np.array([extract_scores(s) for s in df['score']])

    df = calculate_winner_loser_score(df)

###  SALVATAGGIO DB DEL DATASET COMPLETO

## Analisi EDA dataset

    plt.figure(figsize=(10, 5))
    sns.countplot(x='surface', data=df)
    plt.title('Distribuzione delle Superfici di Gioco')
    plt.show()

if __name__ == '__main__':
    main()