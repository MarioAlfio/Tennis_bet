from db_config import create_match_stats_table, DatabaseManager
from logger import setup_logger

logger = setup_logger()

def save(engine, df):
    db_manager = DatabaseManager(engine)

    try:
        table_name = "match_stats"
        create_match_stats_table(engine)
        logger.info(f"Salvataggio del DataFrame nella tabella '{table_name}'...")
        db_manager.insert_dataframe(df, table_name)
    except Exception as e:
        logger.error(f"Errore nel salvataggio dei dati: {e}")
        raise

def get_table(engine):
    try:
        logger.info(f"Tipo di engine ricevuto: {type(engine)}")
        db_manager = DatabaseManager(engine)
        return db_manager.read_table("match_stats")
    except Exception as e:
        logger.error(f"Errore nella lettura della tabella match_stats: {e}")
        raise

def update_row(engine, condition_dict, update_dict):
    try:
        table_name = "match_stats"
        db_manager = DatabaseManager(engine)
        db_manager.update_data(table_name, condition_dict, update_dict)
    except Exception as e:
        logger.error(f"Errore nell'aggiornamento del record in {table_name}: {e}")
        raise

def delete_row(engine, condition_dict):
    try:
        table_name = "match_stats"
        db_manager = DatabaseManager(engine)
        db_manager.delete_data(table_name, condition_dict)
    except Exception as e:
        logger.error(f"Errore nell'eliminazione del record da {table_name}: {e}")
        raise
