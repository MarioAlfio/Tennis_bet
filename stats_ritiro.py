import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import hmean, gmean
from db_config import connect_to_db, DatabaseManager

# Funzione per il calcolo dei match disputati
def calculate_total_matches(calcolo_ritiro):
    all_players = np.r_[calcolo_ritiro['winner_id'].values, calcolo_ritiro['loser_id'].values]
    player_matches = pd.Series(all_players).value_counts().reset_index()
    player_matches.columns = ['player_id', 'total_matches']
    player_matches = player_matches[player_matches['total_matches'] >= 10]
    return player_matches

# Funzione per il calcolo dei match persi per ritiro
def calculate_losses_by_ret(calcolo_ritiro):
    loser_ret = calcolo_ritiro.loc[calcolo_ritiro['ritiro'].values, 'loser_id'].values
    df_loser_ret = pd.Series(loser_ret).value_counts().reset_index()
    df_loser_ret.columns = ['player_id', 'losses_by_ret']
    df_loser_ret = df_loser_ret[df_loser_ret['losses_by_ret'] >= 2]
    return df_loser_ret

# Funzione per il calcolo delle medie
def calculate_means(player_matches, df_loser_ret):
    merged_data = pd.merge(player_matches, df_loser_ret, on='player_id', how='left').fillna(0)
    merged_data['mean'] = (merged_data['losses_by_ret'] / merged_data['total_matches']).replace(np.inf, 0)
    return merged_data

def create_boxplot(data, title, xlabel):
    plt.figure(figsize=(10, 5))
    sns.boxplot(x=data)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.show()
