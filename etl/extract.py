import pandas as pd
from logger import setup_logger
import os

logger = setup_logger()

def load_csv_files(file_paths):
    if not file_paths or len(file_paths) != 1:
        raise ValueError("Devi specificare esattamente un file CSV da caricare.")

    fp = file_paths[0]

    try:
        if not os.path.exists(fp):
            logger.error(f"File non trovato: {fp}")
            raise FileNotFoundError(f"File non trovato: {fp}")

        df = pd.read_csv(fp)

        if df.empty:
            logger.warning(f"Il file è vuoto: {fp}")
            raise ValueError(f"Il file {fp} è vuoto.")

        logger.info(f"File caricato correttamente: {fp} ({len(df)} righe)")
        return df

    except pd.errors.ParserError as e:
        logger.error(f"Errore di parsing nel file {fp}: {e}")
        raise

    except Exception as e:
        logger.error(f"Errore imprevisto nel file {fp}: {e}")
        raise
