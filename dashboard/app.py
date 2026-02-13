import streamlit as st
import pandas as pd
import requests
import os
from google.cloud import bigquery
from config import PROJECT_ID, BACKEND_URL, BIGQUERY_DATASET, BIGQUERY_TABLE

# --- CONFIGURAZIONE CREDENZIALI ---
if os.path.exists("keys.json"):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "keys.json"
bq_client = bigquery.Client()

st.set_page_config(page_title="Data Platform MVP", layout="wide")
st.title("📊 Data Analysis Hub")

# Sidebar con info di configurazione
with st.sidebar:
    st.subheader("⚙️ Configurazione")
    st.info(f"**Project ID:**\n{PROJECT_ID}")
    st.info(f"**Backend URL:**\n{BACKEND_URL}")
    
    # Debug opzionale
    if st.checkbox("🔍 Mostra dettagli ambiente"):
        st.code(f"""
K_SERVICE: {os.getenv('K_SERVICE', 'N/A')}
GOOGLE_CLOUD_PROJECT: {os.getenv('GOOGLE_CLOUD_PROJECT', 'N/A')}
        """)

tab1, tab2 = st.tabs(["🚀 Ingestione API", "🔍 SQL Workspace"])

with tab1:
    st.header("Invia Dati al Backend")
    up = st.file_uploader("Carica CSV", type="csv")
    if up and st.button("Avvia Processo Custom"):
        df = pd.read_csv(up)
        st.info(f"📊 Dataset caricato: {len(df)} righe, {len(df.columns)} colonne")
        with st.spinner("Il backend sta elaborando..."):
            try:
                res = requests.post(
                    f"{BACKEND_URL}/analyze", 
                    json={"data": df.to_dict(orient="records")},
                    timeout=30
                )
                res.raise_for_status()
                st.success("✅ Analisi completata!")
                st.json(res.json())
            except requests.exceptions.ConnectionError:
                st.error(f"❌ Impossibile connettersi al backend")
                st.warning(f"Verifica che BACKEND_URL sia configurato correttamente: `{BACKEND_URL}`")
            except requests.exceptions.Timeout:
                st.error("⏱️ Il backend ha impiegato troppo tempo a rispondere")
            except requests.exceptions.HTTPError as e:
                st.error(f"❌ Errore HTTP {e.response.status_code}: {e.response.text}")
            except Exception as e:
                st.error(f"❌ Errore generico: {e}")

with tab2:
    st.header("Query Diretta BigQuery")
    query = st.text_area(
        "SQL Editor", 
        f"SELECT * FROM `{PROJECT_ID}.{BIGQUERY_DATASET}.{BIGQUERY_TABLE}` LIMIT 10",
        height=150
    )
    if st.button("Esegui SQL"):
        try:
            with st.spinner("⏳ Esecuzione query..."):
                df_res = bq_client.query(query).to_dataframe()
                st.success(f"✅ Query completata: {len(df_res)} righe")
                st.dataframe(df_res, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Errore BigQuery: {e}")