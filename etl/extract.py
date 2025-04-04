import pandas as pd
from logger import setup_logger
import os

logger = setup_logger()

def load_csv_files(file_paths):
    dfs = []

    for fp in file_paths:
        try:
            if not os.path.exists(fp):
                logger.warning(f"File non trovato: {fp}")
                continue

            df = pd.read_csv(fp)
            logger.info(f"File caricato correttamente: {fp} ({len(df)} righe)")
            dfs.append(df)

        except pd.errors.ParserError as e:
            logger.error(f"Errore di parsing nel file {fp}: {e}")
        except Exception as e:
            logger.error(f"Errore imprevisto nel file {fp}: {e}")

    if not dfs:
        logger.error("Nessun file CSV caricato. Verifica i percorsi.")
        raise ValueError("Nessun file valido caricato.")

    try:
        df_final = pd.concat(dfs, axis=0, ignore_index=True)
        logger.info(f"Tutti i file concatenati con successo. Totale righe: {len(df_final)}")
        return df_final
    except Exception as e:
        logger.error(f"Errore nella concatenazione dei DataFrame: {e}")
        raise
