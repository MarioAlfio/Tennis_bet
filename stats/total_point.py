import numpy as np
import pandas as pd

#def calculate_total_point(df):

    # Calcola TPW (Total Points Won) per il vincitore e il perdente
#    df['w_TPW'] = df['w_1stWon'] + df['w_2ndWon'] + (df['l_svpt'] - df['l_1stWon'] - df['l_2ndWon'])
#    df['l_TPW'] = df['l_1stWon'] + df['l_2ndWon'] + (df['w_svpt'] - df['w_1stWon'] - df['w_2ndWon'])
    #df['TP'] = df['w_TPW'] + df['l_TPW']
    
#    for col in ['w_TPW', 'l_TPW']:
#        df[col] = df[col].replace([np.inf, -np.inf], np.nan)
        # Arrotonda a 1 decimale e aggiungi simbolo %
#        df[col] = df[col].apply(lambda x: f"{round(x, 1)}" if pd.notnull(x) else None)

    #df['TP'] = df['w_TPW'] + df['l_TPW']

#   return(df)


def calculate_total_point(df):
    # TPW = tutti i punti vinti dal vincitore e dal perdente
    df['w_TPW'] = df['w_1stWon'] + df['w_2ndWon'] + (df['l_svpt'] - df['l_1stWon'] - df['l_2ndWon'])
    df['l_TPW'] = df['l_1stWon'] + df['l_2ndWon'] + (df['w_svpt'] - df['w_1stWon'] - df['w_2ndWon'])

    # Pulisci infiniti
    df['w_TPW'] = df['w_TPW'].replace([np.inf, -np.inf], np.nan)
    df['l_TPW'] = df['l_TPW'].replace([np.inf, -np.inf], np.nan)

    # Calcola il totale dei punti giocati e % vinta dal vincitore
    df['TP'] = df['w_TPW'] + df['l_TPW']
    df['w_TPW_pct'] = (df['w_TPW'] / df['TP']) * 100

    df['w_TPW_pct'] = df['w_TPW_pct'].round(1)

    return df
