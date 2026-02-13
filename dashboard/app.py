import streamlit as st
import pandas as pd
import requests
import os
from google.cloud import bigquery

# --- FALLBACK LOGIC ---
PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "project-id-placeholder")
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8080")

if os.path.exists("keys.json"):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "keys.json"
bq_client = bigquery.Client()

st.set_page_config(page_title="Data Platform MVP", layout="wide")
st.title("📊 Data Analysis Hub")

st.sidebar.info(f"Backend URL: {BACKEND_URL}")

tab1, tab2 = st.tabs(["🚀 Ingestione API", "🔍 SQL Workspace"])

with tab1:
    st.header("Invia Dati al Backend")
    up = st.file_uploader("Carica CSV", type="csv")
    if up and st.button("Avvia Processo Custom"):
        df = pd.read_csv(up)
        with st.spinner("Il backend sta elaborando..."):
            try:
                res = requests.post(f"{BACKEND_URL}/analyze", json={"data": df.to_dict(orient="records")})
                st.success("Analisi completata!")
                st.json(res.json())
            except Exception as e:
                st.error(f"Errore di connessione: {e}")

with tab2:
    st.header("Query Diretta BigQuery")
    query = st.text_area("SQL Editor", f"SELECT * FROM `{PROJECT_ID}.mvp_dataset.processed_table` LIMIT 10")
    if st.button("Esegui SQL"):
        try:
            df_res = bq_client.query(query).to_dataframe()
            st.dataframe(df_res, use_container_width=True)
        except Exception as e:
            st.error(f"Errore BigQuery: {e}")