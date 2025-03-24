from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, MetaData, Table
import pandas as pd

# Configurazione connessione database
DB_URL = "postgresql://username:password@localhost:5432/your_database"

# Connessione al database
def connect_to_db():
    engine = create_engine(DB_URL)
    return engine

# Creazione delle tabelle
def create_tables(engine):
    metadata = MetaData()

    ritiro_stats = Table(
        'ritiro_stats', metadata,
        Column('player_id', Integer, primary_key=True),
        Column('player_name', String),
        Column('total_matches', Integer),
        Column('losses_by_ret', Integer),
        Column('weighted_mean', Float),
        Column('harmonic_mean', Float),
        Column('geometric_mean', Float)
    )

    metadata.create_all(engine)
    print("Tabelle create con successo.")

# CRUD Operations
class DatabaseManager:
    def __init__(self, engine):
        self.engine = engine

    # Inserimento dati
    def insert_data(self, table_name, data_df):
        data_df.to_sql(table_name, self.engine, if_exists='replace', index=False, method='multi')
        print(f"Dati inseriti nella tabella '{table_name}' con successo.")

    # Lettura dati
    def read_data(self, table_name):
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, self.engine)
        return df

    # Aggiornamento dati
    def update_data(self, table_name, player_id, new_values):
        query = f"""
        UPDATE {table_name}
        SET losses_by_ret = {new_values['losses_by_ret']}
        WHERE player_id = {player_id}
        """
        with self.engine.connect() as conn:
            conn.execute(query)
        print(f"Dati aggiornati per player_id = {player_id}")

    # Eliminazione dati
    def delete_data(self, table_name, player_id):
        query = f"DELETE FROM {table_name} WHERE player_id = {player_id}"
        with self.engine.connect() as conn:
            conn.execute(query)
        print(f"Dati eliminati per player_id = {player_id}")

if __name__ == '__main__':
    engine = connect_to_db()
    create_tables(engine)

    # Esempio CRUD
    db_manager = DatabaseManager(engine)

    # Esempio di lettura dati
    data = db_manager.read_data('ritiro_stats')
    print(data)
