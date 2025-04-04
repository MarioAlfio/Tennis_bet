import numpy as np

def calculate_ace_rate(df):
    
    # Calcola il tasso di ace per il vincitore
    df['w_ace_rate'] = (df['w_ace'] / df['w_svpt']) * 100

    # Calcola il tasso di ace per il perdente
    df['l_ace_rate'] = (df['l_ace'] / df['l_svpt']) * 100

    df = df.replace({ 'w_ace_rate': {np.inf: np.nan, -np.inf: np.nan} })
    df = df.replace({ 'l_ace_rate': {np.inf: np.nan, -np.inf: np.nan} })

    return df
