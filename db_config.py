from sqlalchemy import create_engine, Column, Integer, String, Float, Date, MetaData, Table, text
from sqlalchemy.orm import sessionmaker
import pandas as pd
from logger import setup_logger

logger = setup_logger()

DB_URL = "postgresql://mytennuser:mytennuser1@localhost:5432/tennis_db"

def connect_to_db():
    try:
        engine = create_engine(DB_URL)
        logger.info("Connessione al DB avvenuta con successo.")
        return engine
    except Exception as e:
        logger.error(f"Errore nella connessione al database: {e}")
        raise

def create_match_stats_table(engine):
    try:
        metadata = MetaData()
        table_name = "match_stats"

        match_stats = Table(
            table_name, metadata,
            Column('Date', Date),
            Column('Tournament', String),
            Column('Surface', String),
            Column('Rd', String),
            Column('wRk', Integer),
            Column('vRk', Integer),
            Column('w_name', String),
            Column('vname', String),
            Column('score', String),
            Column('w_score', Integer),
            Column('vscore', Integer),
            Column('DR', Float),
            Column('Ace_rate', Float),
            Column('DF_rate', Float),
            Column('1stIn', Float),
            Column('w_1strate', Float),
            Column('w_2strate', Float),
            Column('BPSvd', Float),
            Column('TPW', Float),
            Column('RPW', Float),
            Column('vA_rate', Float),
            Column('v1st_rate', Float),
            Column('v2nd_rate', Float),
            Column('BPConv', Float),
            Column('TP', Integer),
            Column('Time', Integer)
        )
        

        metadata.create_all(engine)
        logger.info(f"Tabella '{table_name}' creata con successo.")
    except Exception as e:
        logger.error(f"Errore nella creazione della tabella {table_name}: {e}")
        raise

class DatabaseManager:
    def __init__(self, engine):
        self.engine = engine
        self.Session = sessionmaker(bind=engine)

    def insert_dataframe(self, df, table_name):
        try:
            df.to_sql(table_name, self.engine, if_exists='append', index=False, method='multi')
            logger.info(f"Inseriti {len(df)} record nella tabella '{table_name}'.")
        except Exception as e:
            logger.error(f"Errore nell'inserimento dati in '{table_name}': {e}")
            raise

    def read_table(self, table_name):
        try:
            with self.engine.connect() as conn:
                query = text(f"SELECT * FROM {table_name}")
                df = pd.read_sql(query, conn)
            logger.info(f"Lettura completata dalla tabella '{table_name}'.")
            return df
        except Exception as e:
            logger.error(f"Errore nella lettura della tabella '{table_name}': {e}")
            raise

    def update_data(self, table_name, condition_dict, update_dict):
        try:
            set_clause = ", ".join([f"{k} = :{k}" for k in update_dict.keys()])
            where_clause = " AND ".join([f"{k} = :{k}" for k in condition_dict.keys()])

            sql = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
            params = {**update_dict, **condition_dict}

            with self.engine.connect() as conn:
                conn.execute(text(sql), params)
            logger.info(f"Aggiornato record nella tabella '{table_name}'.")
        except Exception as e:
            logger.error(f"Errore nell'update sulla tabella '{table_name}': {e}")
            raise

    def delete_data(self, table_name, condition_dict):
        try:
            where_clause = " AND ".join([f"{k} = :{k}" for k in condition_dict.keys()])
            sql = f"DELETE FROM {table_name} WHERE {where_clause}"

            with self.engine.connect() as conn:
                conn.execute(text(sql), condition_dict)
            logger.info(f"Eliminato record dalla tabella '{table_name}'.")
        except Exception as e:
            logger.error(f"Errore nella delete sulla tabella '{table_name}': {e}")
            raise
