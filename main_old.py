import numpy as np
import pandas as pd
from stats.stats_ritiro import calculate_losses_by_ret, calculate_total_matches, calculate_means, create_boxplot
from stats.scomponi_score import extract_scores, calculate_winner_loser_score
from db_config import connect_to_db, DatabaseManager
import matplotlib.pyplot as plt
import seaborn as sns
from stats.dominance_ratio import calculate_dominance_ratio
from stats.ace_rate import calculate_ace_rate
from stats.double_f_rate import calculate_df_rate
from stats.serve_pr import calculate_serve_percentages

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

# split del campo stringa score

    #df.drop(['score'], axis=1, inplace=True)

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

    # Dizionario per mappare le abbreviazioni ai loro significati (IN ORDINE LOGICO)
    round_labels = {
        'Q1': 'Primo turno di qualificazione',
        'Q2': 'Secondo turno di qualificazione',
        'Q3': 'Terzo turno di qualificazione',
        'R64': 'Primo turno (64 giocatori)',
        'R32': 'Secondo turno (32 giocatori)',
        'R16': 'Ottavi di finale (16 giocatori)',
        'QF': 'Quarti di finale',
        'SF': 'Semifinali',
        'F': 'Finale'
    }

    # Ordinamento personalizzato per il grafico
    round_order = list(round_labels.keys())

    # Mappa di colori personalizzati
    round_colors = {
        'Q1': '#1f77b4',   # Blu
        'Q2': '#ff7f0e',   # Arancione
        'Q3': '#2ca02c',   # Verde
        'R64': '#d62728',  # Rosso
        'R32': '#9467bd',  # Viola
        'R16': '#8c564b',  # Marrone
        'QF': '#e377c2',   # Rosa
        'SF': '#7f7f7f',   # Grigio
        'F': '#bcbd22'     # Giallo
    }

    # Creazione del grafico con colori personalizzati
    plt.figure(figsize=(12, 6))
    sns.countplot(x='round', hue= 'round', data=df, order=round_order, palette=round_colors, legend=False)

    # Titoli e asse
    plt.title('Distribuzione dei Turni di Gioco')
    plt.xlabel('Turno')
    plt.ylabel('Conteggio')

    # Aggiunta della legenda
    handles = [plt.Line2D([0], [0], color=round_colors[abbr], lw=4, label=f'{abbr}: {desc}') 
                for abbr, desc in round_labels.items()]
    plt.legend(handles=handles, bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.show()

    # Definizioni dei livelli dei tornei
    tourney_labels = {
        'G': 'Grand Slam',
        'M': 'Masters 1000',
        'A': 'ATP 500/250',
        'C': 'Challenger'
    }

    tourney_order = list(tourney_labels.keys())
    tourney_colors = {
        'G': '#1f77b4',
        'M': '#ff7f0e',
        'A': '#2ca02c',
        'C': '#d62728'
    }

  
    plt.figure(figsize=(10, 5))
    sns.countplot(x='tourney_level', hue='tourney_level', data=df,
                order=tourney_order, palette=tourney_colors, legend=False)

    plt.title('Distribuzione dei Livelli dei Tornei')
    plt.xlabel('Livello del Torneo')
    plt.ylabel('Conteggio')

    # Legenda manuale
    handles = [plt.Line2D([0], [0], color=tourney_colors[abbr], lw=4, label=f'{abbr}: {desc}') 
            for abbr, desc in tourney_labels.items()]
    plt.legend(handles=handles, bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.show()

### TROVARE TUTTE MEDIE E STATS SU MATCH E DOPO EFFETTUARE DI NUOVO CORRELAZIONE 

    df = calculate_dominance_ratio(df)

    plt.figure(figsize=(8, 5))
    sns.boxplot(x=df['w_dominance_ratio'])
    plt.title("Boxplot del Dominance Ratio (Vincitore)")
    plt.xlabel("Dominance Ratio")
    plt.tight_layout()
    plt.show()

    sns.histplot(df['w_dominance_ratio'], bins=30, kde=True)
    plt.title("Distribuzione del Dominance Ratio (Vincitore)")
    plt.show()

    df = calculate_ace_rate(df)

    # Boxplot per visualizzare la distribuzione del tasso di ace
    plt.figure(figsize=(10, 5))
    sns.boxplot(x=df['w_ace_rate'])
    plt.title('Distribuzione del Tasso di Ace per i Vincitori')
    plt.xlabel('Tasso di Ace (%)')
    plt.tight_layout()
    plt.show()

    # Confronto tra il tasso di ace del vincitore e del perdente
    plt.figure(figsize=(10, 5))
    sns.histplot(df['w_ace_rate'], color='blue', label='Vincitore', kde=True, stat='density', linewidth=0)
    sns.histplot(df['l_ace_rate'], color='red', label='Perdente', kde=True, stat='density', linewidth=0)
    plt.title('Distribuzione del Tasso di Ace - Vincitore vs Perdente')
    plt.xlabel('Tasso di Ace (%)')
    plt.legend()
    plt.tight_layout()
    plt.show()


    df = calculate_df_rate(df)

    plt.figure(figsize=(10, 5))
    #sns.boxplot(x=df['w_df_rate'], color='blue', label='Vincitore')
    sns.boxplot(x=df['l_df_rate'], color='red', label='Perdente')
    plt.title('Distribuzione del Double Fault Rate (Vincitore vs Perdente)')
    plt.xlabel('Double Fault Rate (%)')
    plt.legend()
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 5))
    sns.histplot(df['w_df_rate'], color='blue', label='Vincitore', kde=True)
    sns.histplot(df['l_df_rate'], color='red', label='Perdente', kde=True)
    plt.title('Distribuzione del Double Fault Rate - Vincitore vs Perdente')
    plt.xlabel('Double Fault Rate (%)')
    plt.legend()
    plt.tight_layout()
    plt.show()

    df = calculate_serve_percentages(df)

    plt.figure(figsize=(10, 5))
    sns.boxplot(x=df['w_1st_pct'], color='blue', label='Vincitore 1st Serve %')
    sns.boxplot(x=df['w_2nd_pct'], color='green', label='Vincitore 2nd Serve %')
    sns.boxplot(x=df['l_1st_pct'], color='red', label='Perdente 1st Serve %')
    sns.boxplot(x=df['l_2nd_pct'], color='orange', label='Perdente 2nd Serve %')
    plt.title('Distribuzione delle Percentuali di Servizio (1st e 2nd Serve) - Vincitore vs Perdente')
    plt.xlabel('Percentuale di Punti Vinti (%)')
    plt.legend()
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 5))
    sns.histplot(df['w_1st_pct'], color='blue', label='Vincitore 1st Serve %', kde=True)
    sns.histplot(df['w_2nd_pct'], color='green', label='Vincitore 2nd Serve %', kde=True)
    sns.histplot(df['l_1st_pct'], color='red', label='Perdente 1st Serve %', kde=True)
    sns.histplot(df['l_2nd_pct'], color='orange', label='Perdente 2nd Serve %', kde=True)
    plt.title('Distribuzione delle Percentuali di Servizio (1st e 2nd Serve) - Vincitore vs Perdente')
    plt.xlabel('Percentuale di Punti Vinti (%)')
    plt.legend()
    plt.tight_layout()
    plt.show()

    




if __name__ == '__main__':
    main()