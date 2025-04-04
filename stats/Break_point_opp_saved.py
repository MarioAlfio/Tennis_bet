import numpy as np 
import pandas as pd

def calculate_break_point_opp_sa(df):

    # Calcola BPSvd (Break Point Opportunities Saved) per il vincitore
    df['w_BPSvd'] = (df['w_bpSaved'] / df['w_bpFaced']) * 100
    df['l_BPSvd'] = (df['l_bpSaved'] / df['l_bpFaced']) * 100

    for col in ['w_BPSvd', 'l_BPSvd']:
        df[col] = df[col].replace([np.inf, -np.inf], np.nan)
        # Arrotonda a 1 decimale e aggiungi simbolo %
        df[col] = df[col].apply(lambda x: f"{round(x, 1)}" if pd.notnull(x) else None)

    return df