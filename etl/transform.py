import numpy as np
import pandas as pd
from logger import setup_logger
from functools import reduce
from stats.dominance_ratio import calculate_dominance_ratio
from stats.ace_rate import calculate_ace_rate
from stats.divide_season import get_season
from stats.double_f_rate import calculate_df_rate
from stats.serve_pr import calculate_serve_percentages
from stats.Break_point_opp_saved import calculate_break_point_opp_sa
from stats.total_point import calculate_total_point
from stats.return_point import calculate_return_point
from stats.calculate_return_point_v12st import calculate_advanced_stats
from stats.scomponi_score import extract_scores, calculate_winner_loser_score



logger = setup_logger()

def clean_and_prepare(df):
    try:
        #df.drop(['match_num'], axis=1, inplace=True)
        df['tourney_date'] = pd.to_datetime(df['tourney_date'], format='%Y%m%d')
        df['year'] = df['tourney_date'].dt.year

        eliminare = reduce(np.logical_or, [
            np.char.find(df['score'].values.astype(str), 'RET') >= 0,
            np.char.find(df['score'].values.astype(str), 'W/O') >= 0,
            np.char.find(df['score'].values.astype(str), 'DEF') >= 0,
            np.char.find(df['score'].values.astype(str), 'Ret') >= 0,
            np.char.find(df['score'].values.astype(str), 'Def.') >= 0
        ])

        df = df[~eliminare]

        columns_to_clean = [
            'w_ace', 'w_df', 'w_svpt', 'w_1stIn', 'w_1stWon', 'w_2ndWon', 'w_SvGms', 'w_bpSaved', 'w_bpFaced',
            'l_ace', 'l_df', 'l_svpt', 'l_1stIn', 'l_1stWon', 'l_2ndWon', 'l_SvGms', 'l_bpSaved', 'l_bpFaced',
            'match_num','winner_id', 'winner_entry','score', 'best_of'
        ]

        df = df.dropna(subset=columns_to_clean)

        # Applica la funzione per creare la nuova colonna tourney_season
        df['tourney_season'] = df['tourney_date'].apply(get_season)

        score_cols = ['score_1set_w', 'score_1set_l', 'score_tiebreak_1set_l', 
              'score_2set_w', 'score_2set_l', 'score_tiebreak_2set_l',
              'score_3set_w', 'score_3set_l', 'score_tiebreak_3set_l',
              'score_4set_w', 'score_4set_l', 'score_tiebreak_4set_l',
              'score_5set_w', 'score_5set_l', 'score_tiebreak_5set_l']

        df[score_cols] = np.array([extract_scores(s) for s in df['score']])

        df = calculate_winner_loser_score(df)

        df = calculate_dominance_ratio(df)
        df = calculate_ace_rate(df)
        df = calculate_serve_percentages(df)
        df = calculate_df_rate(df)
        df = calculate_break_point_opp_sa(df)
        df = calculate_total_point(df)
        df = calculate_advanced_stats(df)
        df = calculate_return_point(df)

        logger.info("Dati puliti e colonna 'year' aggiunta con successo.")
        return df
    except Exception as e:
        logger.error(f"Errore nella funzione clean_and_prepare: {e}")
        raise

def prepare_for_db(df):
    try:
        df_final = df[[ 
            'tourney_date', 'tourney_name', 'surface', 'round',
            'winner_rank', 'loser_rank', 'winner_name', 'loser_name', 'score', 
            'winner_score', 'loser_score',  'w_dominance_ratio', 'w_ace_rate', 'w_df_rate',
            '1stIn', 'w_1st_pct', 'w_2nd_pct', 'w_BPSvd',
            'w_TPW_pct', 'w_RPW', 'l_ace_rate', 'v1st_rate', 'v2nd_rate', 'l_BPSvd', 'TP', 'minutes'
            ]].copy()

        df_final.columns = [
            'Date', 'Tournament', 'Surface', 'Rd', 'wRk', 'vRk', 'w_name', 
            'vname' , 'score', 'w_score', 'vscore', 'DR', 'Ace_rate', 'DF_rate', '1stIn', 'w_1strate',
            'w_2strate', 'BPSvd', 'TPW', 'RPW', 'vA_rate', 'v1st_rate',
            'v2nd_rate', 'BPConv', 'TP','Time'
        ]

        # controllo colonne corrette

        logger.info("Dati trasformati per il DB con successo.")
        return df_final
    except KeyError as e:
        logger.error(f"Colonna mancante nella funzione prepare_for_db: {e}")
        raise
    except Exception as e:
        logger.error(f"Errore inaspettato nella funzione prepare_for_db: {e}")
        raise
