"""
config.py - Configurazione centralizzata per backend e dashboard
Gestisce auto-rilevamento GCP e fallback per sviluppo locale
"""
import os
import requests
from typing import Optional


class Config:
    """Classe di configurazione con caricamento lazy"""
    
    _project_id: Optional[str] = None
    _backend_url: Optional[str] = None
    
    @classmethod
    def get_project_id(cls) -> str:
        """
        Rileva automaticamente il Project ID GCP.
        Ordine di priorità:
        1. Variabile d'ambiente GCP_PROJECT_ID
        2. Variabili standard GCP (GOOGLE_CLOUD_PROJECT, etc)
        3. Metadata server GCP
        4. Fallback locale
        """
        if cls._project_id:
            return cls._project_id
        
        # 1. Variabile esplicita
        if project_id := os.getenv("GCP_PROJECT_ID"):
            cls._project_id = project_id
            return project_id
        
        # 2. Variabili standard GCP
        for var in ["GOOGLE_CLOUD_PROJECT", "GCP_PROJECT", "GCLOUD_PROJECT"]:
            if project_id := os.getenv(var):
                cls._project_id = project_id
                return project_id
        
        # 3. Metadata server (solo su GCP)
        try:
            metadata_url = "http://metadata.google.internal/computeMetadata/v1/project/project-id"
            headers = {"Metadata-Flavor": "Google"}
            response = requests.get(metadata_url, headers=headers, timeout=2)
            if response.status_code == 200:
                cls._project_id = response.text
                return response.text
        except:
            pass
        
        # 4. Fallback locale
        cls._project_id = "local-development-project"
        return cls._project_id
    
    @classmethod
    def get_backend_url(cls) -> str:
        """
        Rileva automaticamente l'URL del backend.
        Ordine di priorità:
        1. Variabile d'ambiente BACKEND_URL
        2. Fallback localhost per sviluppo
        """
        if cls._backend_url:
            return cls._backend_url
        
        # 1. Variabile esplicita (questo è il metodo raccomandato)
        if backend_url := os.getenv("BACKEND_URL"):
            cls._backend_url = backend_url
            return backend_url
        
        # 2. Fallback localhost per sviluppo locale
        cls._backend_url = "http://localhost:8080"
        return cls._backend_url
    
    @classmethod
    def get_port(cls) -> int:
        """Porta per il server (usato dal backend)"""
        return int(os.getenv("PORT", 8080))
    
    @classmethod
    def is_production(cls) -> bool:
        """Verifica se siamo in ambiente di produzione"""
        return os.getenv("K_SERVICE") is not None or os.getenv("GAE_ENV") is not None


# ========================================
# CONFIGURAZIONE PROGETTO
# ========================================
# Modifica questi valori per ogni nuovo progetto

# Nome del servizio backend su Cloud Run
BACKEND_SERVICE_NAME = "backend-mvp"

# Nome del servizio dashboard su Cloud Run  
DASHBOARD_SERVICE_NAME = "dashboard-mvp"

# Nome del dataset BigQuery
BIGQUERY_DATASET = "test_auto_create"

# Nome della tabella BigQuery per i dati processati
BIGQUERY_TABLE = "processed_table"

# ========================================
# VARIABILI AUTO-RILEVATE (non modificare)
# ========================================
PROJECT_ID = Config.get_project_id()
BACKEND_URL = Config.get_backend_url()
PORT = Config.get_port()
IS_PRODUCTION = Config.is_production()


if __name__ == "__main__":
    # Script di debug per verificare la configurazione
    print("=" * 50)
    print("CONFIGURAZIONE RILEVATA")
    print("=" * 50)
    print(f"Project ID: {PROJECT_ID}")
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Port: {PORT}")
    print(f"Ambiente: {'PRODUZIONE' if IS_PRODUCTION else 'LOCALE'}")
    print("=" * 50)
    print("\nCONFIGURAZIONE PROGETTO:")
    print(f"Backend Service: {BACKEND_SERVICE_NAME}")
    print(f"Dashboard Service: {DASHBOARD_SERVICE_NAME}")
    print(f"BigQuery Dataset: {BIGQUERY_DATASET}")
    print(f"BigQuery Table: {BIGQUERY_TABLE}")
    print("=" * 50)
    print("\nVariabili d'ambiente GCP:")
    for var in ["K_SERVICE", "GOOGLE_CLOUD_PROJECT", "GCP_PROJECT", "BACKEND_URL"]:
        print(f"  {var}: {os.getenv(var, 'NON IMPOSTATA')}")