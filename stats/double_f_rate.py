import numpy as np
import pandas as pd

def calculate_df_rate(df):
    
    # Calcolo del Double Fault Rate (DF%) per il vincitore
    df['w_df_rate'] = (df['w_df'] / df['w_svpt']) * 100

    df['l_df_rate'] = (df['l_df'] / df['l_svpt']) * 100
    
    for col in ['w_df_rate', 'l_df_rate']:
        df[col] = df[col].replace([np.inf, -np.inf], np.nan)
        # Arrotonda a 1 decimale e aggiungi simbolo %
        df[col] = df[col].apply(lambda x: f"{round(x, 1)}" if pd.notnull(x) else None)

    return df
