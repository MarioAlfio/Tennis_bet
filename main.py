import streamlit as st
from db_config import connect_to_db, DatabaseManager
from etl.extract import load_csv_files
from etl.transform import clean_and_prepare, prepare_for_db
from etl.load import save, get_table
from logger import setup_logger

logger = setup_logger()

st.set_page_config(page_title="Tennis Stats", layout="wide")

st.title("Tennis Stats")
st.markdown("Pipeline ETL + Anteprima dati su DB")

# Step 1 - Caricamento file CSV
file_paths = [
    "./data_csv/atp_matches_qual_chall_2022.csv",
    "./data_csv/atp_matches_qual_chall_2023.csv",
    "./data_csv/atp_matches_qual_chall_2024.csv"
]

with st.spinner("Caricamento e unione dei file..."):
    try:
        raw_df = load_csv_files(file_paths)
        st.success(f"File caricati. Totale righe: {len(raw_df)}")
    except Exception as e:
        st.error(f"Errore nel caricamento dei file: {e}")
        st.stop()

# Step 2 - Pulizia e trasformazione
with st.spinner("Pulizia e trasformazione dati..."):
    try:
        cleaned_df = clean_and_prepare(raw_df)
        final_df = prepare_for_db(cleaned_df)
        st.success("Dati trasformati con successo.")
    except Exception as e:
        st.error(f"Errore nella trasformazione: {e}")
        st.stop()

# Step 3 - Connessione DB e salvataggio
engine = connect_to_db()

if st.button("🚀 Salva nel Database"):
    with st.spinner("Salvataggio in corso..."):
        try:
            save(engine, final_df)
            st.success("Dati salvati su DB per ogni anno.")
        except Exception as e:
            st.error(f"Errore nel salvataggio: {e}")

# Step 4 - Anteprima tabella dal DB
st.subheader("Anteprima dei dati salvati nel DB")

#selected_year = st.selectbox("Seleziona l'anno", [2022, 2023, 2024])
if st.button("Mostra anteprima"):
    try:
        preview_df = get_table(engine).head(10)
        st.dataframe(preview_df)
    except Exception as e:
        st.error(f"Errore nel recupero della tabella: {e}")
