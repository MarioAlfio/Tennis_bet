import numpy as np
import pandas as pd

def calculate_serve_percentages(df):
    
    # Calcolare la percentuale per il vincitore
    df['1stIn'] = (df['w_1stIn'] / df['w_svpt'])*100
    df['w_1st_pct'] = (df['w_1stWon'] / df['w_1stIn']) * 100
    df['w_2nd_pct'] = (df['w_2ndWon'] / (df['w_svpt'] - df['w_1stIn'])) * 100

    # Calcolare la percentuale per il perdente
    df['l_1st_pct'] = (df['l_1stWon'] / df['l_1stIn']) * 100
    df['l_2nd_pct'] = (df['l_2ndWon'] / (df['l_svpt'] - df['l_1stIn'])) * 100

    for col in ['1stIn', 'w_1st_pct', 'w_2nd_pct', 'l_1st_pct', 'l_2nd_pct']:
        df[col] = df[col].replace([np.inf, -np.inf], np.nan)
        # Arrotonda a 1 decimale e aggiungi simbolo %
        df[col] = df[col].apply(lambda x: f"{round(x, 1)}" if pd.notnull(x) else None)
    
    return df
