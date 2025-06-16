import streamlit as st
from db_config import connect_to_db, DatabaseManager
from etl.extract import load_csv_files
from etl.transform import clean_and_prepare, prepare_for_db
from etl.load import save, get_table
from logger import setup_logger
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import trim_mean

logger = setup_logger()

st.set_page_config(page_title="Tennis Stats", layout="wide")

st.title("Tennis Stats")
st.markdown("Pipeline ETL + Anteprima dati su DB")

# Step 1 - Caricamento file CSV
file_paths = [
    "./data_csv/atp_matches_qual_chall_2022.csv"
]

with st.spinner("Caricamento del file..."):
    try:
        raw_df = load_csv_files(file_paths)
        st.success(f"File caricato. Totale righe: {len(raw_df)}")
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

if st.button("Mostra anteprima"):
    try:
        preview_df = get_table(engine).head(10)
        st.dataframe(preview_df)
    except Exception as e:
        st.error(f"Errore nel recupero della tabella: {e}")

# Step 5 - EDA
st.subheader("Analisi EDA")

# Dizionario per mappare le abbreviazioni ai loro significati (IN ORDINE LOGICO)
round_labels = {
    'Q1': 'Primo turno di qualificazione',
    'Q2': 'Secondo turno di qualificazione',
    'Q3': 'Terzo turno di qualificazione',
    'R64': 'Primo turno (64 giocatori)',
    'R32': 'Secondo turno (32 giocatori)',
    'R16': 'Ottavi di finale (16 giocatori)',
    'QF': 'Quarti di finale',
    'SF': 'Semifinali',
    'F': 'Finale'
}

# Ordinamento personalizzato per il grafico
round_order = list(round_labels.keys())

# Mappa di colori personalizzati
round_colors = {
    'Q1': '#1f77b4',   # Blu
    'Q2': '#ff7f0e',   # Arancione
    'Q3': '#2ca02c',   # Verde
    'R64': '#d62728',  # Rosso
    'R32': '#9467bd',  # Viola
    'R16': '#8c564b',  # Marrone
    'QF': '#e377c2',   # Rosa
    'SF': '#7f7f7f',   # Grigio
    'F': '#bcbd22'     # Giallo
}

fig, ax = plt.subplots(figsize=(12, 6))
sns.countplot(
    x='Rd',
    hue='Rd',
    data=final_df,
    order=round_order,
    palette=round_colors,
    ax=ax,
    legend=False
)

# Titoli e asse
ax.set_title('Distribuzione dei Turni di Gioco')
ax.set_xlabel('Turno')
ax.set_ylabel('Conteggio')

# Aggiunta della legenda personalizzata
handles = [plt.Line2D([0], [0], color=round_colors[abbr], lw=4, label=f'{abbr}: {desc}')
           for abbr, desc in round_labels.items()]
ax.legend(handles=handles, bbox_to_anchor=(1.05, 1), loc='upper left')

# Migliora il layout e mostra in Streamlit
fig.tight_layout()
st.pyplot(fig)


# Correlazione

# Selezione delle colonne indicate
selected_cols = [
    'DR', 'Ace_rate', 'DF_rate', '1stIn', 'w_1strate',
    'w_2strate', 'BPSvd', 'TPW', 'RPW', 'vA_rate', 'v1st_rate',
    'v2nd_rate', 'BPConv', 'TP','Time'
]

# Copia del dataset con solo le colonne selezionate
df_corr = final_df[selected_cols].copy()

# Calcolo della matrice di correlazione (ignora automaticamente i NaN)
corr_matrix = df_corr.corr()

# Creazione della figura e asse per la heatmap
fig, ax = plt.subplots(figsize=(18, 14))
sns.heatmap(
    corr_matrix,
    annot=True,
    fmt='.2f',
    cmap='coolwarm',
    square=True,
    linewidths=0.5,
    ax=ax
)
ax.set_title('Matrice di Correlazione delle Variabili Selezionate')
fig.tight_layout()

# Visualizzazione nel frontend Streamlit
st.subheader("Matrice di Correlazione")
st.pyplot(fig)


st.title("Boxplot Variabili e Media Trimmed")
st.markdown("Visualizzazione dei boxplot delle variabili numeriche. Clicca il bottone per rimuovere outlier con media trimmed.")

# -- Selezione variabili numeriche
numeric_cols = df_corr.select_dtypes(include=['float64', 'int64']).columns.tolist()

# -- Slider per percentuale trimmed
trim_prop = st.slider("Percentuale da rimuovere (media trimmed)", 0.0, 0.5, 0.1, step=0.05)

# -- Bottone per attivare la media trimmed
apply_trim = st.button("Applica media trimmed e aggiorna boxplot")

# -- Dati da visualizzare: originali o filtrati
if apply_trim:
    # Calcola media trimmed per ogni colonna
    trimmed_means = {col: trim_mean(df_corr[col].dropna(), proportiontocut=trim_prop) for col in numeric_cols}

    # Rimuovi outlier (valori troppo distanti dalla media trimmed)
    df_plot = df_corr.copy()
    for col in numeric_cols:
        col_data = df_plot[col].dropna()
        tm = trimmed_means[col]
        std = col_data.std()
        mask = (df_plot[col] > tm - 2 * std) & (df_plot[col] < tm + 2 * std)
        df_plot[col] = df_plot[col].where(mask)
    st.info("Media trimmed applicata. I grafici sono stati aggiornati.")
else:
    df_plot = df_corr.copy()

# -- Layout a griglia per boxplot
n_cols = 2
rows = (len(numeric_cols) + n_cols - 1) // n_cols
for i in range(rows):
    cols = st.columns(n_cols)
    for j in range(n_cols):
        idx = i * n_cols + j
        if idx < len(numeric_cols):
            colname = numeric_cols[idx]
            with cols[j]:
                fig, ax = plt.subplots(figsize=(5, 3))
                sns.boxplot(y=df_plot[colname], ax=ax)
                ax.set_title(f"Boxplot - {colname}")
                st.pyplot(fig)
