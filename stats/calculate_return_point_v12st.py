import numpy as np
import pandas as pd

def calculate_advanced_stats(df):
    
    # Percentuale di punti vinti in risposta alla 1a di servizio dell’avversario
    df['v1st_rate'] = ((df['l_1stIn'] - df['l_1stWon']) / df['l_1stIn']) * 100

    # Percentuale di punti vinti in risposta alla 2a di servizio dell’avversario
    second_serves = df['l_svpt'] - df['l_1stIn']
    points_won_on_2nd = second_serves - df['l_2ndWon']
    df['v2nd_rate'] = (points_won_on_2nd / second_serves) * 100

    
    for col in ['v1st_rate', 'v2nd_rate']:
        df[col] = df[col].replace([np.inf, -np.inf], np.nan)
        # Arrotonda a 1 decimale e aggiungi simbolo %
        df[col] = df[col].apply(lambda x: f"{round(x, 1)}" if pd.notnull(x) else None)

    return df
