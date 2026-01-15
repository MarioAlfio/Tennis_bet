# Tennis Stats

Applicazione Streamlit per l'analisi statistica di partite ATP, con pipeline ETL completa e dashboard EDA interattiva.

## Architettura

```
tennis-stats/
├── main.py              # App Streamlit (frontend + orchestrazione)
├── db_config.py         # Configurazione PostgreSQL + CRUD
├── logger.py            # Logging centralizzato
├── etl/
│   ├── extract.py       # Caricamento CSV
│   ├── transform.py     # Pulizia + calcolo statistiche
│   └── load.py          # Salvataggio su DB
├── stats/               # Funzioni statistiche (DR, ace rate, ecc.)
└── data_csv/            # File sorgente ATP
```

## Pipeline ETL

| Fase | Modulo | Operazioni |
|------|--------|------------|
| **Extract** | `extract.py` | Carica CSV ATP, valida esistenza e contenuto |
| **Transform** | `transform.py` | Rimuove ritiri (RET/W.O.), calcola 15+ metriche statistiche |
| **Load** | `load.py` | Crea tabella `match_stats`, inserisce dati in PostgreSQL |

## Statistiche Calcolate

- **DR** (Dominance Ratio) — rapporto punti vinti/persi
- **Ace Rate** — percentuale ace su punti servizio
- **DF Rate** — percentuale doppi falli
- **1stIn** — percentuale prima di servizio in campo
- **w_1strate / w_2strate** — punti vinti con prima/seconda
- **BPSvd** — break point salvati
- **TPW / RPW** — total/return points won
- **BPConv** — break point convertiti

## EDA Interattiva

L'app include tre visualizzazioni:

1. **Distribuzione turni** — countplot dei round (Q1 → Finale)
2. **Matrice di correlazione** — heatmap delle metriche numeriche
3. **Boxplot con trimmed mean** — rimozione outlier interattiva

## Requisiti

```
streamlit
pandas
numpy
sqlalchemy
psycopg2-binary
matplotlib
seaborn
scipy
```

## Setup Database

```sql
CREATE DATABASE tennis_db;
CREATE USER mytennuser WITH PASSWORD 'mytennuser1';
GRANT ALL PRIVILEGES ON DATABASE tennis_db TO mytennuser;
```

Modifica `DB_URL` in `db_config.py` se necessario.

## Utilizzo

```bash
# Installa dipendenze
pip install -r requirements.txt

# Avvia l'app
streamlit run main.py
```

1. L'app carica automaticamente il CSV all'avvio
2. Clicca **"Salva nel Database"** per persistere i dati
3. Esplora le visualizzazioni EDA nella sezione inferiore
