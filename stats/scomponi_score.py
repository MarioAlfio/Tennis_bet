import numpy as np

# Funzione per separare i set e gestire i tie-break
def extract_scores(score):
    try:
        sets = score.split()
        scores = []
        
        for s in sets:
            if '(' in s:  # Caso Tie-Break
                try:
                    w, tiebreak = s.split('(')
                    w, l = w.split('-')
                    scores.extend([int(w), int(l), int(tiebreak.strip(')'))])
                except ValueError:
                    scores.extend([np.nan, np.nan, np.nan])
            elif '-' in s:
                try:
                    w, l = s.split('-')
                    scores.extend([int(w), int(l), np.nan])  # No tie-break
                except ValueError:
                    scores.extend([np.nan, np.nan, np.nan])    
            else:
                scores.extend([np.nan, np.nan, np.nan])
            
        # Completamento con NaN se mancano dati
        while len(scores) < 15:
            scores.append(np.nan)
        
        return scores[:15]

    except Exception as e:
        print(f"Errore con il valore '{score}': {e}")
        return [np.nan] * 15  # Riempie i valori con NaN in caso di errore



# Funzione per calcolare i set vinti con NumPy
def calculate_winner_loser_score(df):
    # Verifica che le colonne necessarie siano presenti nel DataFrame
    required_columns = [
        'score_1set_w', 'score_2set_w', 'score_3set_w', 'score_4set_w', 'score_5set_w',
        'score_1set_l', 'score_2set_l', 'score_3set_l', 'score_4set_l', 'score_5set_l'
    ]
    
    # Controllo se le colonne richieste esistono nel DataFrame
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Mancano le seguenti colonne richieste: {missing_columns}")
    
    # Creazione della colonna 'winner_score'
    set_wins = np.sum(
        (df[['score_1set_w', 'score_2set_w', 'score_3set_w', 'score_4set_w', 'score_5set_w']].values >
         df[['score_1set_l', 'score_2set_l', 'score_3set_l', 'score_4set_l', 'score_5set_l']].values), 
        axis=1
    )

    set_loser = np.sum(
        (df[['score_1set_w', 'score_2set_w', 'score_3set_w', 'score_4set_w', 'score_5set_w']].values <
         df[['score_1set_l', 'score_2set_l', 'score_3set_l', 'score_4set_l', 'score_5set_l']].values), 
        axis=1
    )
    
    # Aggiungi la colonna 'winner_score' al DataFrame
    df['winner_score'] = set_wins
    df['loser_score'] = set_loser

    return df
