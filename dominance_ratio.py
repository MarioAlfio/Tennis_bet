def calculate_dominance_ratio(df):
    import numpy as np

    # --- Vincitore ---
    df['w_sv_won'] = df['w_1stWon'] + df['w_2ndWon']
    df['w_sv_lost'] = df['w_svpt'] - df['w_sv_won']

    df['l_sv_won'] = df['l_1stWon'] + df['l_2ndWon']
    df['l_sv_lost'] = df['l_svpt'] - df['l_sv_won']

    df['w_return_pct'] = df['l_sv_lost'] / df['l_svpt']
    df['w_serve_lost_pct'] = df['w_sv_lost'] / df['w_svpt']
    df['w_dominance_ratio'] = df['w_return_pct'] / df['w_serve_lost_pct']
        

    # Gestione divisioni per zero e valori estremi
    df = df.replace({ 'w_dominance_ratio': {np.inf: np.nan, -np.inf: np.nan} })

    return df
