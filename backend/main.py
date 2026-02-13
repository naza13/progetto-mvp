import os
import pandas as pd
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
from google.cloud import bigquery
import firebase_admin
from firebase_admin import credentials, firestore
from config import PROJECT_ID, PORT, BIGQUERY_DATASET, BIGQUERY_TABLE

app = FastAPI(title="MVP Data & CRUD API")

if not firebase_admin._apps:
    if os.path.exists("keys.json"):
        cred = credentials.Certificate("keys.json")
        firebase_admin.initialize_app(cred)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "keys.json"
    else:
        firebase_admin.initialize_app()

db_fs = firestore.client()
bq_client = bigquery.Client()

# --- MODELLI DATI (Pydantic) ---
class Item(BaseModel):
    title: str
    description: Optional[str] = None
    category: str

class DataPayload(BaseModel):
    data: List[Dict[str, Any]]

# --- 1. OPERAZIONE: GET (Read) ---
@app.get("/items")
async def get_all_items():
    """Recupera tutti i documenti dalla collezione 'items' di Firestore."""
    try:
        docs = db_fs.collection("items").stream()
        return [{"id": doc.id, **doc.to_dict()} for doc in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/items/{item_id}")
async def get_item(item_id: str):
    """Recupera un singolo documento per ID."""
    doc_ref = db_fs.collection("items").document(item_id)
    doc = doc_ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Elemento non trovato")
    return {"id": doc.id, **doc.to_dict()}

# --- 2. OPERAZIONE: POST (Create) ---
@app.post("/items")
async def create_item(item: Item):
    """Crea un nuovo documento in Firestore."""
    try:
        # .add() genera un ID automatico da Google
        new_doc = db_fs.collection("items").add({
            **item.dict(),
            "created_at": datetime.utcnow()
        })
        return {"id": new_doc[1].id, "status": "created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- 3. OPERAZIONE: PUT (Update) ---
@app.put("/items/{item_id}")
async def update_item(item_id: str, item: Item):
    """Aggiorna un documento esistente."""
    doc_ref = db_fs.collection("items").document(item_id)
    if not doc_ref.get().exists:
        raise HTTPException(status_code=404, detail="ID non trovato")
    
    doc_ref.update({**item.dict(), "updated_at": datetime.utcnow()})
    return {"status": "updated"}

# --- 4. OPERAZIONE: DELETE (Delete) ---
@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    """Elimina un documento."""
    doc_ref = db_fs.collection("items").document(item_id)
    if not doc_ref.get().exists:
        raise HTTPException(status_code=404, detail="ID non trovato")
    
    doc_ref.delete()
    return {"status": "deleted"}

# --- 5. OPERAZIONE SPECIALE: DATA ANALYSIS (Ingestione BQ) ---@app.post("/analyze")
async def analyze_and_store(payload: DataPayload):
    """Processa dati massivi e li salva su BigQuery."""
    try:
        df = pd.DataFrame(payload.data)
        if df.empty:
            raise HTTPException(400, "Dataset vuoto")
        
        # Crea il dataset se non esiste
        dataset_id = f"{PROJECT_ID}.{BIGQUERY_DATASET}"
        try:
            bq_client.get_dataset(dataset_id)
        except Exception:
            # Dataset non esiste, crealo
            dataset = bigquery.Dataset(dataset_id)
            dataset.location = "EU"  # Cambia se usi altra region
            bq_client.create_dataset(dataset, exists_ok=True)
        
        # Salvataggio su BigQuery
        table_id = f"{PROJECT_ID}.{BIGQUERY_DATASET}.{BIGQUERY_TABLE}"
        job = bq_client.load_table_from_dataframe(df, table_id)
        job.result()
        
        return {"status": "success", "rows": len(df)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)