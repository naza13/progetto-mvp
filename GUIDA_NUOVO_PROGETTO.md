# 📘 Guida Completa: Creare un Nuovo Progetto dal Template MVP

## 🎯 Panoramica

Questa guida ti mostra come creare un nuovo progetto del master partendo dal template `progetto-mvp`.

**Tempo stimato:** 10-15 minuti per progetto

---

## 📋 Pre-requisiti

- [ ] Hai `progetto-mvp` funzionante e testato
- [ ] Account GitHub
- [ ] Account Google Cloud con progetto attivo
- [ ] `gcloud` CLI installato e configurato
- [ ] Git installato

---

## 🚀 Step-by-Step: Creare Nuovo Progetto

### STEP 1: Crea Copia Locale del Template

**Obiettivo:** Copiare il progetto base e prepararlo per il nuovo progetto.

**📝 Valori da definire:**
- `<NOME-PROGETTO>`: Il nome del tuo nuovo progetto (es: `sentiment-analysis`, `customer-churn`, `image-classifier`)
- `<TUA-DIRECTORY>`: Dove tieni i tuoi progetti sul PC (es: `~/Documenti`, `~/Desktop/progetti`, `C:/Users/tuonome/progetti`)

**Comandi:**

```bash
# 1. Vai nella tua directory di lavoro
cd <TUA-DIRECTORY>
# Esempio: cd ~/Documenti

# 2. Copia TUTTA la cartella progetto-mvp con un nuovo nome
cp -r progetto-mvp progetto-<NOME-PROGETTO>
# Esempio: cp -r progetto-mvp progetto-sentiment-analysis

# 3. Entra nella nuova cartella
cd progetto-<NOME-PROGETTO>
# Esempio: cd progetto-sentiment-analysis

# 4. Rimuovi il collegamento Git al progetto originale
rm -rf .git

# 5. Inizializza un nuovo repository Git (da zero)
git init
```

**✅ Risultato:**
Hai ora una copia fresca del template, scollegata dall'originale:
```
<TUA-DIRECTORY>/
├── progetto-mvp/                    ← Originale (non toccare più!)
└── progetto-<NOME-PROGETTO>/        ← Nuova copia per nuovo progetto
```

---

### STEP 2: Modifica config.py

**Obiettivo:** Configurare i nomi specifici del nuovo progetto.

**📝 Valori da definire:**
- `<NOME-PROGETTO>`: Il nome scelto nello STEP 1 (es: `sentiment-analysis`)
- `<NOME-DATASET>`: Nome per il dataset BigQuery (es: `sentiment_dataset`)

**File da modificare:** `config.py`

**Trova le righe 88-97 e sostituisci i valori:**

```python
# ========================================
# CONFIGURAZIONE PROGETTO
# ========================================

# Nome del servizio backend su Cloud Run
BACKEND_SERVICE_NAME = "backend-<NOME-PROGETTO>"
# Esempio: "backend-sentiment-analysis"

# Nome del servizio dashboard su Cloud Run  
DASHBOARD_SERVICE_NAME = "dashboard-<NOME-PROGETTO>"
# Esempio: "dashboard-sentiment-analysis"

# Nome del dataset BigQuery
BIGQUERY_DATASET = "<NOME-DATASET>"
# Esempio: "sentiment_dataset"

# Nome della tabella BigQuery per i dati processati
BIGQUERY_TABLE = "processed_table"
# ← Questo puoi lasciarlo così o cambiarlo
```

**💡 Convenzione nomi suggerita:**
- Backend: `backend-<nome-progetto>`
- Dashboard: `dashboard-<nome-progetto>`
- Dataset: `<nome-progetto>_dataset`

**Esempi concreti:**

| Progetto | BACKEND_SERVICE_NAME | DASHBOARD_SERVICE_NAME | BIGQUERY_DATASET |
|----------|---------------------|------------------------|------------------|
| Sentiment Analysis | `backend-sentiment-analysis` | `dashboard-sentiment-analysis` | `sentiment_dataset` |
| Customer Churn | `backend-customer-churn` | `dashboard-customer-churn` | `churn_dataset` |
| Image Classifier | `backend-image-classifier` | `dashboard-image-classifier` | `images_dataset` |

---

### STEP 3: Modifica cloudbuild.yaml

**Obiettivo:** Dire a Cloud Build come chiamare i servizi quando li deploya.

**File da modificare:** `cloudbuild.yaml`

**📝 Usa gli STESSI nomi che hai messo in config.py!**

---

**Modifica 1 - Riga 22:** Nome del servizio backend

**Trova:**
```yaml
- 'backend-mvp'  
```

**Sostituisci con:**
```yaml
- 'backend-<NOME-PROGETTO>'
```
**Esempio:** `- 'backend-sentiment-analysis'`

---

**Modifica 2 - Riga 48:** Nome del servizio dashboard

**Trova:**
```yaml
- 'dashboard-mvp'
```

**Sostituisci con:**
```yaml
- 'dashboard-<NOME-PROGETTO>'
```
**Esempio:** `- 'dashboard-sentiment-analysis'`

---

**Modifica 3 - Riga 53:** Backend URL

**Trova:**
```yaml
- '--set-env-vars=BACKEND_URL=https://backend-mvp-392180154441.europe-west1.run.app'
```

⚠️ **IMPORTANTE:** NON modificare ancora questo! 

Lascialo così per ora. Lo aggiornerai **DOPO il primo deploy** nello STEP 8, quando avrai l'URL vero del tuo nuovo backend.

---

**✅ Riepilogo modifiche:**
- Riga 22: Nome backend → `backend-<NOME-PROGETTO>`
- Riga 48: Nome dashboard → `dashboard-<NOME-PROGETTO>`  
- Riga 53: Lascia com'è per ora (lo cambi dopo)

---

### STEP 4: Commit Locale

```bash
git add .
git commit -m "Initial setup for sentiment-analysis project"
```

---

### STEP 5: Crea Repository GitHub

**Obiettivo:** Creare un posto dove salvare il codice online.

**📝 Valori da definire:**
- `<TUO-USERNAME>`: Il tuo username GitHub (es: `naza13`)
- `<NOME-PROGETTO>`: Il nome del progetto (es: `sentiment-analysis`)

---

**Opzione A - Via Web (più facile):**

1. Vai su **https://github.com**
2. Clicca sul bottone **"New"** (o **"+"** in alto a destra → **"New repository"**)
3. Compila:
   - **Repository name:** `progetto-<NOME-PROGETTO>`
   - **Description:** `Progetto master: <descrizione breve>`
   - **Visibilità:** Pubblico o Privato (scegli tu)
   - ⚠️ **NON** spuntare "Initialize this repository with a README"
4. Clicca **"Create repository"**

**Esempio compilazione:**
```
Repository name: progetto-sentiment-analysis
Description: Progetto master: Sentiment Analysis su Twitter
Visibility: Public
```

---

**Opzione B - Via GitHub CLI (se installato):**

```bash
gh repo create progetto-<NOME-PROGETTO> --public --source=. --remote=origin
```

**Esempio:**
```bash
gh repo create progetto-sentiment-analysis --public --source=. --remote=origin
```

---

### STEP 6: Push del Codice su GitHub

**Obiettivo:** Caricare il codice dal tuo PC a GitHub.

**📝 Valori da usare:**
- `<TUO-USERNAME>`: Il tuo username GitHub
- `<NOME-PROGETTO>`: Il nome del progetto

---

**Se hai usato Opzione A (creazione via web):**

```bash
# 1. Collega il repository remoto
git remote add origin https://github.com/<TUO-USERNAME>/progetto-<NOME-PROGETTO>.git

# 2. Rinomina il branch in 'main' (se necessario)
git branch -M main

# 3. Carica il codice su GitHub
git push -u origin main
```

**Esempio concreto:**
```bash
git remote add origin https://github.com/naza13/progetto-sentiment-analysis.git
git branch -M main
git push -u origin main
```

---

**Se hai usato Opzione B (GitHub CLI):**

Non serve fare nulla! Il codice è già stato caricato automaticamente.

---

**✅ Verifica:**
Vai su `https://github.com/<TUO-USERNAME>/progetto-<NOME-PROGETTO>` e dovresti vedere tutti i file!

---

### STEP 7: Configura Cloud Build Trigger

**Obiettivo:** Dire a Google Cloud di fare il deploy automatico quando fai `git push`.

**📝 Valori da usare:**
- `<NOME-PROGETTO>`: Il nome del progetto
- `<NOME-REPO-GITHUB>`: Il nome del repository GitHub (es: `progetto-sentiment-analysis`)

---

**Procedura dettagliata:**

1. **Vai su Google Cloud Console:**
   - Apri: https://console.cloud.google.com

2. **Apri Cloud Build:**
   - Clicca sul menu ☰ (in alto a sinistra)
   - Scorri e trova **"Cloud Build"**
   - Clicca su **"Trigger"** (o "Attivatori")

3. **Crea nuovo trigger:**
   - Clicca sul bottone blu **"CREA TRIGGER"** in alto

4. **Compila i campi:**

   | Campo | Valore da inserire | Esempio |
   |-------|-------------------|---------|
   | **Nome** | `deploy-<NOME-PROGETTO>` | `deploy-sentiment-analysis` |
   | **Descrizione** | `Auto-deploy per <NOME-PROGETTO>` | `Auto-deploy per sentiment analysis` |
   | **Evento** | Lascia "Push a un branch" | - |
   | **Sorgente** | Clicca **"CONNETTI NUOVO REPOSITORY"** | - |

5. **Connetti il repository GitHub:**
   - Nella finestra che si apre:
     - Seleziona **"GitHub (Cloud Build GitHub App)"**
     - Clicca **"CONTINUA"**
   - Se richiesto, **autenticati con GitHub**
   - Seleziona il repository **`progetto-<NOME-PROGETTO>`**
   - Spunta la casella per confermare
   - Clicca **"CONNETTI"**
   - Nella schermata successiva, clicca **"CREA TRIGGER"**

6. **Torna alla configurazione del trigger** (si riapre automaticamente):

   | Campo | Valore | Note |
   |-------|--------|------|
   | **Branch** | `^main$` | Triggera solo su push a main |
   | **Tipo** | Cloud Build configuration file (yaml or json) | - |
   | **Località** | Repository | Non "In linea"! |
   | **Percorso file configurazione** | `/cloudbuild.yaml` | Automatico quando selezioni "Repository" |

7. **Salva:**
   - Scorri in basso
   - Clicca il bottone blu **"CREA"**

---

**✅ Verifica:**
Nella pagina "Trigger" dovresti vedere il tuo nuovo trigger `deploy-<NOME-PROGETTO>` nella lista!

---

### STEP 8: Prima Build e Deploy

1. **Fai un push per triggerare la build:**
   ```bash
   git commit --allow-empty -m "Trigger first build"
   git push
   ```

2. **Monitora la build:**
   - Vai su **Cloud Build → Cronologia**
   - Clicca sulla build in corso
   - Aspetta che completi (~5-10 minuti per la prima volta)

3. **Quando la build è SUCCESS:**
   - Vai su **Cloud Run**
   - Trova il servizio `backend-sentiment-analysis`
   - Copia l'URL (tipo: `https://backend-sentiment-analysis-xyz.europe-west1.run.app`)

4. **Aggiorna cloudbuild.yaml con l'URL del backend:**
   
   Apri `cloudbuild.yaml`, trova riga 53:
   ```yaml
   - '--set-env-vars=BACKEND_URL=https://backend-mvp-392180154441.europe-west1.run.app'
   ```
   
   Sostituisci con il tuo URL:
   ```yaml
   - '--set-env-vars=BACKEND_URL=https://backend-sentiment-analysis-xyz.europe-west1.run.app'
   ```

5. **Committa e pusha:**
   ```bash
   git add cloudbuild.yaml
   git commit -m "Update backend URL"
   git push
   ```

6. **Aspetta la seconda build** (sarà più veloce, ~2-3 minuti)

---

### STEP 9: Test del Nuovo Progetto

1. **Apri il Dashboard:**
   - Vai su **Cloud Run**
   - Clicca su `dashboard-sentiment-analysis`
   - Clicca sull'**URL** in alto

2. **Verifica Sidebar:**
   - **Project ID:** Deve mostrare il tuo project-id GCP
   - **Backend URL:** Deve mostrare l'URL del backend-sentiment-analysis

3. **Test Upload CSV:**
   - Vai al tab **"🚀 Ingestione API"**
   - Carica un CSV di test
   - Clicca **"Avvia Processo Custom"**
   - Dovresti vedere: ✅ Analisi completata!

4. **Verifica BigQuery:**
   - Vai su **BigQuery**
   - Nel pannello di sinistra, espandi il tuo progetto
   - Dovresti vedere il dataset `sentiment_dataset` creato automaticamente
   - Espandilo → vedrai la tabella `processed_table` con i dati

---

## ✅ Checklist Finale

Verifica che tutto sia configurato correttamente:

- [ ] Repository GitHub creato e codice pushato
- [ ] Cloud Build trigger configurato
- [ ] Prima build completata con successo
- [ ] Backend deployato e URL copiato
- [ ] cloudbuild.yaml aggiornato con backend URL
- [ ] Seconda build completata con successo
- [ ] Dashboard accessibile via browser
- [ ] Sidebar mostra configurazione corretta
- [ ] Upload CSV funziona
- [ ] Dataset BigQuery creato automaticamente
- [ ] Query SQL nel dashboard funzionano

---

## 🔄 Workflow Quotidiano

Una volta configurato tutto, il workflow diventa semplicissimo:

```bash
# 1. Fai modifiche al codice
vim dashboard/app.py

# 2. Testa in locale (opzionale)
streamlit run dashboard/app.py

# 3. Committa
git add .
git commit -m "Add new feature X"

# 4. Pusha
git push

# 5. Cloud Build fa tutto automaticamente!
# - Builda i container
# - Li pusha su Container Registry
# - Li deploya su Cloud Run
```

Dopo 2-3 minuti, le tue modifiche sono live! 🚀

---

## 🆘 Troubleshooting

### Errore: "Build failed - config.py not found"

**Causa:** Il file config.py non è stato committato

**Soluzione:**
```bash
git add config.py
git commit -m "Add config.py"
git push
```

---

### Errore: "Impossibile connettersi al backend"

**Causa:** BACKEND_URL nel cloudbuild.yaml non è corretto

**Soluzione:**
1. Verifica l'URL del backend su Cloud Run
2. Aggiorna cloudbuild.yaml riga 53
3. Committa e pusha

---

### Errore: "Dataset not found" anche con auto-create

**Causa:** Permessi BigQuery mancanti

**Soluzione:**
1. Vai su **IAM e amministrazione**
2. Trova il service account di Cloud Run (tipo `xxx@xxx.iam.gserviceaccount.com`)
3. Aggiungi ruolo: **BigQuery Admin**

---

### Build lentissima (>10 minuti)

**Causa:** Prima build senza cache

**Soluzione:** È normale! Le build successive saranno molto più veloci (2-4 minuti)

---

## 📊 Riepilogo File da Modificare per Ogni Progetto

| File | Cosa Modificare | Quando |
|------|----------------|--------|
| `config.py` | Nomi servizi e dataset (righe 88-97) | All'inizio |
| `cloudbuild.yaml` | Nomi deploy (righe 22, 48, 53) | All'inizio + dopo primo deploy |
| Codice progetto | Aggiungi le tue feature! | Durante sviluppo |

**Tutto il resto rimane uguale!** ✅

---

## 🎓 Best Practices

### Naming Convention
- **Servizi:** `backend-<progetto>`, `dashboard-<progetto>`
- **Dataset:** `<progetto>_dataset`
- **Repository:** `progetto-<nome-descrittivo>`

### Git Workflow
- Branch `main` sempre stabile e deployabile
- Feature branch per sviluppo: `feature/nuova-funzionalita`
- Merge su main solo quando testato

### Documentazione
- Aggiungi un `README.md` specifico per ogni progetto
- Documenta l'obiettivo del progetto del master
- Includi esempi di utilizzo

### Costi
- Monitora i costi su **Cloud Console → Fatturazione**
- Cloud Run: Free tier 2M richieste/mese
- BigQuery: Free tier 1TB query/mese
- Elimina progetti non usati per risparmiare

---

## 📚 Progetti Suggeriti per il Master

Ecco alcuni esempi di come potresti usare questo template:

### 1. Sentiment Analysis
- Dataset: Tweet/recensioni
- BigQuery: Analisi sentiment per categoria
- Dashboard: Visualizza distribuzione sentiment

### 2. Customer Churn Prediction
- Dataset: Dati clienti + comportamento
- Backend: API predizione churn
- Dashboard: Visualizza rischio churn per segmento

### 3. Image Classification
- Dataset: Immagini + label
- Backend: Inference API con modello CNN
- Dashboard: Upload immagini e vedi predizioni

### 4. Time Series Forecasting
- Dataset: Dati storici (vendite, meteo, etc)
- BigQuery: Aggregazioni temporali
- Dashboard: Grafici interattivi + predizioni

### 5. Recommendation System
- Dataset: User-item interactions
- Backend: API raccomandazioni
- Dashboard: Esplora raccomandazioni per utente

### 6. NLP Text Classification
- Dataset: Testi + categorie
- Backend: API classificazione
- Dashboard: Input testo → categoria predetta

---

## 🎉 Conclusione

Hai ora un template solido e riutilizzabile per tutti i tuoi progetti del master!

**Vantaggi:**
✅ Setup rapido (10-15 minuti per progetto)
✅ Infrastruttura già configurata (Cloud Run, BigQuery, Firestore)
✅ Deploy automatico ad ogni push
✅ Scalabile e production-ready
✅ Zero maintenance del template base

**Per ogni nuovo progetto:**
1. Clona il template
2. Modifica 2 file (config.py + cloudbuild.yaml)
3. Configura trigger Cloud Build
4. Inizia a sviluppare le tue feature specifiche!

Buon lavoro con i tuoi progetti! 🚀

---

## 📞 Riferimenti Utili

- **Google Cloud Run Docs:** https://cloud.google.com/run/docs
- **BigQuery Docs:** https://cloud.google.com/bigquery/docs
- **Streamlit Docs:** https://docs.streamlit.io
- **FastAPI Docs:** https://fastapi.tiangolo.com

---

**Versione Guida:** 1.0  
**Ultimo Aggiornamento:** Febbraio 2025  
**Autore:** Setup per progetto-mvp-master
