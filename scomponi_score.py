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

