import numpy as np
import pandas as pd

def calculate_return_point(df):
    df['w_sv_won'] = df['w_1stWon'] + df['w_2ndWon']
    df['w_sv_lost'] = df['w_svpt'] - df['w_sv_won']

    df['l_sv_won'] = df['l_1stWon'] + df['l_2ndWon']
    df['l_sv_lost'] = df['l_svpt'] - df['l_sv_won']

    df['w_RPW'] = (df['l_sv_lost'] / df['l_svpt']) * 100
    df['l_RPW'] = (df['w_sv_lost'] / df['w_svpt']) * 100

    for col in ['w_RPW', 'l_RPW']:
        df[col] = df[col].replace([np.inf, -np.inf], np.nan)
        # Arrotonda a 1 decimale e aggiungi simbolo %
        df[col] = df[col].apply(lambda x: f"{round(x, 1)}" if pd.notnull(x) else None)

    return df