"""
==============================================================================
GESTIONALE PERIZIE - Applicazione principale
==============================================================================
Autenticazione: credenziali hardcodate.
Per cambiarle, modifica i valori APP_USERNAME e APP_PASSWORD qui sotto.
"""

import streamlit as st
import pandas as pd
import uuid
import datetime
import io
import json
from supabase import create_client, Client

# ──────────────────────────────────────────────────────────────────────────────
# ❗ CREDENZIALI DI ACCESSO — modificale qui
# ──────────────────────────────────────────────────────────────────────────────
APP_USERNAME = "admin"
APP_PASSWORD = "password_perito_2026"
# ──────────────────────────────────────────────────────────────────────────────

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURAZIONE PAGINA
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Gestionale Perizie",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# CSS PERSONALIZZATO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* Font & base */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Background scuro principale */
.stApp { background-color: #0f1117; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1f2e 0%, #141824 100%);
    border-right: 1px solid #2d3748;
}

/* Login card */
.login-card {
    background: linear-gradient(135deg, #1a1f2e 0%, #1e2538 100%);
    border: 1px solid #2d3748;
    border-radius: 16px;
    padding: 2rem 2rem 1.5rem 2rem;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    max-width: 420px;
    margin: 0 auto 1.5rem auto;
}

/* Metric cards per i filtri stato */
.metric-btn {
    background: linear-gradient(135deg, #1e2538 0%, #252d42 100%);
    border: 1px solid #3d4f6e;
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s ease;
    margin-bottom: 0.5rem;
}
.metric-btn:hover { border-color: #5b7dd8; transform: translateY(-2px); }
.metric-btn .count { font-size: 2rem; font-weight: 700; color: #5b7dd8; }
.metric-btn .label { font-size: 0.85rem; color: #8a9bb5; margin-top: 0.2rem; }
.metric-btn.active { border-color: #5b7dd8; background: linear-gradient(135deg, #1f2d4f 0%, #253660 100%); }

/* Blocchi form */
.block-header {
    font-size: 1rem;
    font-weight: 600;
    color: #c8d3e8;
    padding: 0.6rem 1rem;
    background: linear-gradient(90deg, #1e2538, transparent);
    border-left: 3px solid #5b7dd8;
    border-radius: 4px;
    margin-bottom: 1rem;
    margin-top: 0.5rem;
}

/* Veicolo card */
.vehicle-card {
    background: #1a1f2e;
    border: 1px solid #2d3748;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
}
.vehicle-title {
    font-size: 0.9rem;
    font-weight: 600;
    color: #5b7dd8;
    margin-bottom: 0.8rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid #2d3748;
}

/* Status badge */
.badge-aperta   { background:#1a3a2a; color:#4ade80; border:1px solid #166534; padding:2px 10px; border-radius:20px; font-size:0.8rem; }
.badge-chiusura { background:#3a2d1a; color:#fb923c; border:1px solid #7c2d12; padding:2px 10px; border-radius:20px; font-size:0.8rem; }
.badge-chiusa   { background:#1a2a3a; color:#60a5fa; border:1px solid #1e3a5f; padding:2px 10px; border-radius:20px; font-size:0.8rem; }

/* Divider */
.section-divider { border: none; border-top: 1px solid #2d3748; margin: 1.5rem 0; }

/* Pulsante principale */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #3b5bdb 0%, #5b7dd8 100%) !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 0.6rem 2rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(91,125,216,0.4) !important;
}

/* Nasconde hamburger menu, bottone di deploy e footer */
#MainMenu { visibility: hidden; }
.stDeployButton { visibility: hidden; }
footer { visibility: hidden; }

/* Rende trasparente l'header e mantiene visibile il pulsante di riapertura barra laterale */
[data-testid="stHeader"] {
    background: transparent !important;
}

/* Navigazione sidebar in stile tab premium */
[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 8px;
}
[data-testid="stSidebar"] div[role="radiogroup"] label {
    background-color: transparent;
    border: 1px solid transparent;
    border-radius: 8px;
    padding: 0.6rem 0.8rem !important;
    transition: all 0.25s ease;
    cursor: pointer;
    margin: 0;
    width: 100%;
}
[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {
    display: none !important;
}
[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background-color: rgba(91, 125, 216, 0.08);
    border-color: rgba(91, 125, 216, 0.2);
}
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(135deg, #1f2d4f 0%, #253660 100%) !important;
    border-color: #5b7dd8 !important;
    box-shadow: 0 4px 15px rgba(91, 125, 216, 0.15);
}
[data-testid="stSidebar"] div[role="radiogroup"] label p,
[data-testid="stSidebar"] div[role="radiogroup"] label span {
    color: #8a9bb5 !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    transition: color 0.2s ease;
}
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p,
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) span {
    color: #ffffff !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HELPER: CONNESSIONE SUPABASE
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_resource(show_spinner=False)
def get_supabase_client() -> Client | None:
    """Crea e restituisce il client Supabase. Restituisce None se la connessione fallisce."""
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        return None


# ══════════════════════════════════════════════════════════════════════════════
# HELPER: GENERAZIONE NUMERO PROTOCOLLO
# ══════════════════════════════════════════════════════════════════════════════
def genera_numero_protocollo() -> str:
    """Genera un numero di protocollo nel formato PYYYYMMDD-XXXX."""
    today = datetime.date.today()
    suffix = str(uuid.uuid4())[:4].upper()
    return f"P{today.strftime('%Y%m%d')}-{suffix}"


# ══════════════════════════════════════════════════════════════════════════════
# HELPER: CARICAMENTO DATI DA SUPABASE
# ══════════════════════════════════════════════════════════════════════════════
def carica_pratiche(client: Client) -> pd.DataFrame:
    """Carica tutte le pratiche dalla tabella 'pratiche'."""
    try:
        response = client.table("pratiche").select("*").order("data_creazione_record", desc=True).execute()
        if response.data:
            return pd.DataFrame(response.data)
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Errore nel caricamento delle pratiche: {e}")
        return pd.DataFrame()


def carica_veicoli_per_pratica(client: Client, numero_protocollo: str) -> list:
    """Carica i veicoli/soggetti per una specifica pratica."""
    try:
        response = (
            client.table("soggetti_veicoli_coinvolti")
            .select("*")
            .eq("numero_protocollo", numero_protocollo)
            .execute()
        )
        return response.data or []
    except Exception as e:
        return []


# ══════════════════════════════════════════════════════════════════════════════
# HELPER: SALVATAGGIO SU SUPABASE (UPSERT)
# ══════════════════════════════════════════════════════════════════════════════
def salva_pratica(client: Client, dati_pratica: dict, dati_veicoli: list) -> tuple[bool, str]:
    """
    Esegue un UPSERT sulla tabella 'pratiche' e poi salva/aggiorna
    i veicoli nella tabella 'soggetti_veicoli_coinvolti'.
    Restituisce (successo: bool, messaggio: str).
    """
    numero_protocollo = dati_pratica.get("numero_protocollo", "")
    try:
        # ── UPSERT pratica principale ────────────────────────────────────────
        client.table("pratiche").upsert(dati_pratica, on_conflict="numero_protocollo").execute()

        # ── Elimina i veicoli precedenti e reinserisce ───────────────────────
        client.table("soggetti_veicoli_coinvolti").delete().eq(
            "numero_protocollo", numero_protocollo
        ).execute()
        for veicolo in dati_veicoli:
            veicolo["numero_protocollo"] = numero_protocollo
            client.table("soggetti_veicoli_coinvolti").insert(veicolo).execute()

        return True, f"✅ Pratica **{numero_protocollo}** salvata con successo!"
    except Exception as e:
        return False, f"❌ Errore durante il salvataggio: {e}"


# ══════════════════════════════════════════════════════════════════════════════
# HELPER IA: DUE OUTPUT SEPARATI CON GROQ
# ══════════════════════════════════════════════════════════════════════════════
def _groq_client():
    """Restituisce un client OpenAI puntato su Groq. Solleva eccezione se la chiave manca."""
    import openai
    api_key = st.secrets.get("GROQ_API_KEY", "")
    base_url = st.secrets.get("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
    if not api_key:
        raise ValueError("GROQ_API_KEY non configurata in secrets.toml")
    return openai.OpenAI(api_key=api_key, base_url=base_url)


def elabora_dinamica_ia(dati_anagrafica: dict, veicoli: list, dinamica_grezza: str) -> str:
    """
    Rielabora la dinamica sintetica grezza in un testo tecnico-peritale formale.
    Restituisce il testo formale (str).
    """
    client_groq = _groq_client()
    veicoli_str = "\n".join(
        f"  - {v.get('ruolo','')}: Targa {v.get('targa','N/D')}, "
        f"Modello {v.get('modello','N/D')}, Conducente {v.get('conducente','N/D')}"
        for v in veicoli
    )
    prompt = f"""Sei un perito assicurativo esperto. Riscrivi la seguente dinamica di sinistro in italiano tecnico e peritale formale, \
mantenendo tutti i fatti reali ma usando un linguaggio ufficiale adatto a una relazione peritale.

CONTESTO PRATICA:
- Assistito: {dati_anagrafica.get('cognome_assistito','')} {dati_anagrafica.get('nome_assistito','')}
- Compagnia: {dati_anagrafica.get('compagnia','')}
- Data sinistro: {dati_anagrafica.get('data_sinistro','')}
- Tipo: {dati_anagrafica.get('tipo_dinamica','').upper()}

VEICOLI COINVOLTI:
{veicoli_str}

DINAMICA GREZZA DA RIELABORARE:
{dinamica_grezza if dinamica_grezza else '[Non fornita]'}

Restituisci SOLO il testo rielaborato della dinamica, senza titoli, intestazioni o commenti aggiuntivi.
"""
    response = client_groq.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800,
        temperature=0.3,
    )
    print(f"--- CONSUMO GROQ [dinamica] --- Input: {response.usage.prompt_tokens} | Output: {response.usage.completion_tokens}")
    return response.choices[0].message.content.strip()


def elabora_richieste_ia(dati_anagrafica: dict, richieste_grezze: str) -> str:
    """
    Rielabora le richieste danni grezze in un'analisi tecnica formale.
    Restituisce il testo formale (str).
    """
    client_groq = _groq_client()
    prompt = f"""Sei un perito assicurativo esperto. Riscrivi le seguenti richieste danni in forma tecnica e formale, \
articolando ogni punto in modo chiaro e professionale, adatto a una relazione peritale ufficiale.

CONTESTO PRATICA:
- Assistito: {dati_anagrafica.get('cognome_assistito','')} {dati_anagrafica.get('nome_assistito','')}
- Compagnia: {dati_anagrafica.get('compagnia','')}
- Importo stimato: {dati_anagrafica.get('importo_stimato','N/D')} €

RICHIESTE GREZZE DA RIELABORARE:
{richieste_grezze if richieste_grezze else '[Nessuna richiesta inserita]'}

Restituisci SOLO il testo formale delle richieste, senza titoli, intestazioni o commenti aggiuntivi.
"""
    response = client_groq.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600,
        temperature=0.3,
    )
    print(f"--- CONSUMO GROQ [richieste] --- Input: {response.usage.prompt_tokens} | Output: {response.usage.completion_tokens}")
    return response.choices[0].message.content.strip()


# (mantenuta per compatibilità legacy — non più usata dal form principale)
def genera_relazione_ia(dati_anagrafica: dict, veicoli: list, dinamica: str, richieste: str = "") -> str:
    """
    Genera una relazione formale usando Groq (llama-3.1-8b-instant).
    Riceve anagrafica, veicoli, dinamica sintetica e richieste del perito.
    Fallback: relazione template compilata se Groq non è disponibile.
    """

    # ── Tentativo con Groq ───────────────────────────────────────────────────
    try:
        import openai
        groq_api_key = st.secrets.get("GROQ_API_KEY", "")
        groq_base_url = st.secrets.get("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
        if groq_api_key:
            client_groq = openai.OpenAI(
                api_key=groq_api_key,
                base_url=groq_base_url,
            )
            veicoli_str = "\n".join(
                [
                    f"  - {v.get('ruolo','')}: Targa {v.get('targa','N/D')}, "
                    f"Modello {v.get('modello','N/D')}, Conducente {v.get('conducente','N/D')}"
                    for v in veicoli
                ]
            )
            sezione_richieste = (
                f"\nRICHIESTE DEL PERITO:\n{richieste}\n"
                if richieste.strip() else ""
            )
            prompt = f"""Sei un perito assicurativo esperto. Redigi una relazione peritale formale e professionale basandoti ESCLUSIVAMENTE sui seguenti dati reali:

ANAGRAFICA:
- Protocollo: {dati_anagrafica.get('numero_protocollo','')}
- Assistito: {dati_anagrafica.get('cognome_assistito','')} {dati_anagrafica.get('nome_assistito','')}
- Codice Fiscale: {dati_anagrafica.get('codice_fiscale_assistito','')}
- Numero Sinistro: {dati_anagrafica.get('numero_sinistro','')}
- Compagnia: {dati_anagrafica.get('compagnia','')}
- Perito Assegnato: {dati_anagrafica.get('perito_assegnato','')}
- Liquidatore: {dati_anagrafica.get('liquidatore','')}
- Data sinistro: {dati_anagrafica.get('data_sinistro','')}
- Tipo dinamica: {dati_anagrafica.get('tipo_dinamica','').upper()}
- Riparatore: {dati_anagrafica.get('riparatore','')}
- Importo Stimato: {dati_anagrafica.get('importo_stimato','N/D')} €

VEICOLI COINVOLTI:
{veicoli_str}

DINAMICA SINTETICA:
{dinamica if dinamica else '[Non fornita]'}
{sezione_richieste}
Struttura la relazione con le seguenti sezioni in ordine:
1. INTESTAZIONE FORMALE (protocollo, data, compagnia, perito)
2. SOGGETTO ASSISTITO
3. VEICOLI COINVOLTI
4. DINAMICA DEL SINISTRO
5. ANALISI DELLE RICHIESTE (se presenti, rispondi punto per punto)
6. CONCLUSIONI PERITALI

Usa un linguaggio formale e tecnico. Non aggiungere informazioni non presenti nei dati.
"""
            response = client_groq.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
            )
            print(f"--- CONSUMO GROQ [relazione] --- Input: {response.usage.prompt_tokens} | Output: {response.usage.completion_tokens}")
            return response.choices[0].message.content
    except Exception:
        pass

    # ── Fallback: relazione modello ──────────────────────────────────────────
    oggi = datetime.date.today().strftime("%d/%m/%Y")
    ass = f"{dati_anagrafica.get('cognome_assistito','---')} {dati_anagrafica.get('nome_assistito','---')}"
    proto = dati_anagrafica.get("numero_protocollo", "---")
    comp = dati_anagrafica.get("compagnia", "---")
    data_sin = dati_anagrafica.get("data_sinistro", "---")
    tipo_din = dati_anagrafica.get("tipo_dinamica", "---").upper()
    riparatore = dati_anagrafica.get("riparatore", "---")

    veicoli_text = ""
    for v in veicoli:
        ruolo = v.get("ruolo", "N/D")
        targa = v.get("targa", "N/D")
        modello = v.get("modello", "N/D")
        conducente = v.get("conducente", "N/D")
        proprietario = v.get("proprietario", "N/D")
        veicoli_text += (
            f"\n  [{ruolo.upper()}] Targa: {targa} | Modello: {modello} "
            f"| Conducente: {conducente} | Proprietario: {proprietario}"
        )

    relazione = f"""RELAZIONE PERITALE
══════════════════════════════════════════════════════
Numero Protocollo : {proto}
Data Redazione    : {oggi}
Compagnia         : {comp}
Tipo Pratica      : {tipo_din}
══════════════════════════════════════════════════════

SOGGETTO ASSISTITO
──────────────────
Nominativo   : {ass}
Data Sinistro: {data_sin}
Riparatore   : {riparatore}

VEICOLI COINVOLTI
─────────────────{veicoli_text}

DINAMICA DEL SINISTRO
─────────────────────
{dinamica if dinamica else '[Nessuna dinamica inserita]'}

CONCLUSIONI PERITALI
────────────────────
A seguito di accurato esame della documentazione prodotta e delle circostanze 
esposte, il sottoscritto perito dichiara di aver preso visione del sinistro 
avvenuto in data {data_sin}, coinvolgente i veicoli sopra elencati.

La dinamica ricostruita risulta coerente con i danni rilevati e con le 
dichiarazioni rese dai soggetti coinvolti. Si rimanda alla relazione tecnica 
di stima per i dettagli relativi ai danni materiali accertati.

Il perito
_________________________
Data: {oggi}
══════════════════════════════════════════════════════
(Relazione generata automaticamente — revisionare prima dell'uso)
"""
    return relazione


# ══════════════════════════════════════════════════════════════════════════════
# SCHERMATA DI LOGIN
# ══════════════════════════════════════════════════════════════════════════════
def render_login():
    """Mostra la schermata di login centrata. Aggiorna session_state se login ok."""
    st.markdown("<br><br>", unsafe_allow_html=True)

    col_left, col_center, col_right = st.columns([1, 1.2, 1])
    with col_center:
        st.markdown(
            """
            <div class="login-card">
                <div style="text-align:center; margin-bottom:0;">
                    <span style="font-size:3rem;">🛡️</span>
                    <h2 style="color:#c8d3e8; margin:0.5rem 0 0.2rem; font-weight:700;">
                        Gestionale Perizie
                    </h2>
                    <p style="color:#6b7a99; font-size:0.9rem; margin:0;">
                        Inserisci le credenziali per accedere
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("form_login", clear_on_submit=False):
            username = st.text_input("👤 Username", placeholder="username")
            password = st.text_input("🔑 Password", type="password", placeholder="••••••••••")
            submitted = st.form_submit_button("Accedi →", use_container_width=True, type="primary")

            if submitted:
                if username == APP_USERNAME and password == APP_PASSWORD:
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = username
                    st.rerun()
                else:
                    st.error("Credenziali non valide. Riprova.")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1: DASHBOARD & RICERCA
# ══════════════════════════════════════════════════════════════════════════════
def render_dashboard(client: Client):
    st.markdown("## 📊 Dashboard & Ricerca")
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # ── Caricamento dati ─────────────────────────────────────────────────────
    with st.spinner("Caricamento pratiche..."):
        df_all = carica_pratiche(client)

    if df_all.empty:
        st.info("Nessuna pratica trovata nel database. Inizia creando una nuova pratica dalla scheda **➕ Nuova Pratica**.")

        # Mostra comunque area chat IA
        _render_chat_ia(pd.DataFrame())
        return

    # ── Metriche / Filtri rapidi ──────────────────────────────────────────────
    totale   = len(df_all)
    aperte   = len(df_all[df_all.get("stato_pratica", pd.Series(dtype=str)).str.lower() == "aperta"])   if "stato_pratica" in df_all.columns else 0
    chiusura = len(df_all[df_all.get("stato_pratica", pd.Series(dtype=str)).str.lower() == "in chiusura"]) if "stato_pratica" in df_all.columns else 0
    chiuse   = len(df_all[df_all.get("stato_pratica", pd.Series(dtype=str)).str.lower() == "chiusa"])   if "stato_pratica" in df_all.columns else 0

    # Stato del filtro attivo
    if "filtro_stato" not in st.session_state:
        st.session_state["filtro_stato"] = "Tutte"

    col1, col2, col3, col4 = st.columns(4)
    stati_filtro = ["Tutte", "Aperte", "In Chiusura", "Chiuse"]
    conteggi     = [totale, aperte, chiusura, chiuse]
    icone        = ["📁", "🟢", "🟠", "🔵"]
    cols         = [col1, col2, col3, col4]

    for col, etichetta, conteggio, icona in zip(cols, stati_filtro, conteggi, icone):
        with col:
            attivo = "active" if st.session_state["filtro_stato"] == etichetta else ""
            st.markdown(
                f"""<div class="metric-btn {attivo}" onclick="">
                    <div class="count">{conteggio}</div>
                    <div class="label">{icona} {etichetta}</div>
                </div>""",
                unsafe_allow_html=True,
            )
            if st.button(f"Filtra: {etichetta}", key=f"btn_filtro_{etichetta}", use_container_width=True):
                st.session_state["filtro_stato"] = etichetta
                st.rerun()

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # ── Applicazione filtro stato ─────────────────────────────────────────────
    df_filtrato = df_all.copy()
    if st.session_state["filtro_stato"] == "Aperte" and "stato_pratica" in df_filtrato.columns:
        df_filtrato = df_filtrato[df_filtrato["stato_pratica"].str.lower() == "aperta"]
    elif st.session_state["filtro_stato"] == "In Chiusura" and "stato_pratica" in df_filtrato.columns:
        df_filtrato = df_filtrato[df_filtrato["stato_pratica"].str.lower() == "in chiusura"]
    elif st.session_state["filtro_stato"] == "Chiuse" and "stato_pratica" in df_filtrato.columns:
        df_filtrato = df_filtrato[df_filtrato["stato_pratica"].str.lower() == "chiusa"]

    # ── Barra di ricerca globale ──────────────────────────────────────────────
    st.markdown("### 🔍 Ricerca")
    ricerca = st.text_input(
        "Cerca in tutti i campi",
        placeholder="es. Rossi  |  AB123CD  |  P20260528-...  |  Generali  |  rca  |  Aperta  ...",
        label_visibility="collapsed",
    )

    if ricerca:
        mask = pd.Series([False] * len(df_filtrato), index=df_filtrato.index)
        campi_ricerca = [
            "numero_protocollo", "cognome_assistito", "nome_assistito",
            "codice_fiscale_assistito", "compagnia", "numero_sinistro",
            "tipo_dinamica", "stato_pratica", "riparatore",
            "perito_assegnato", "liquidatore", "note_generali",
            "data_sinistro",
        ]
        for campo in campi_ricerca:
            if campo in df_filtrato.columns:
                mask |= df_filtrato[campo].astype(str).str.contains(ricerca, case=False, na=False)
        df_filtrato = df_filtrato[mask]

    st.markdown(f"**{len(df_filtrato)} pratica/e trovata/e**")

    # ── Tabella risultati ─────────────────────────────────────────────────────
    if not df_filtrato.empty:
        # Colonne visibili e ordine
        colonne_display = [
            c for c in [
                "numero_protocollo", "cognome_assistito", "nome_assistito",
                "compagnia", "data_sinistro", "tipo_dinamica", "stato_pratica",
                "riparatore",
            ] if c in df_filtrato.columns
        ]
        df_display = df_filtrato[colonne_display].copy()

        # Rinomina colonne per leggibilità
        rename_map = {
            "numero_protocollo": "Protocollo",
            "cognome_assistito": "Cognome",
            "nome_assistito": "Nome",
            "compagnia": "Compagnia",
            "data_sinistro": "Data Sinistro",
            "tipo_dinamica": "Tipo",
            "stato_pratica": "Stato",
            "riparatore": "Riparatore",
        }
        df_display.rename(columns=rename_map, inplace=True)

        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True,
            height=min(400, 60 + 35 * len(df_display)),
        )

        # ── Seleziona pratica per modifica ────────────────────────────────────
        st.markdown("### ✏️ Seleziona una Pratica per Modificarla")
        protocolli = df_filtrato["numero_protocollo"].tolist() if "numero_protocollo" in df_filtrato.columns else []

        if protocolli:
            col_sel, col_btn = st.columns([3, 1])
            with col_sel:
                pratica_sel = st.selectbox(
                    "Numero Protocollo",
                    options=["— Seleziona —"] + protocolli,
                    label_visibility="collapsed",
                )
            with col_btn:
                if st.button("📝 Apri per Modifica", type="primary", use_container_width=True):
                    if pratica_sel != "— Seleziona —":
                        riga = df_all[df_all["numero_protocollo"] == pratica_sel].iloc[0].to_dict()
                        veicoli = carica_veicoli_per_pratica(client, pratica_sel)
                        st.session_state["pratica_in_modifica"] = riga
                        st.session_state["veicoli_in_modifica"] = veicoli
                        st.session_state["active_tab"] = "➕ Nuova Pratica / Modifica"
                        st.rerun()
                    else:
                        st.warning("Seleziona una pratica dall'elenco.")
    else:
        st.info("Nessun risultato per i criteri selezionati.")

    # ── Chat IA di Ricerca ────────────────────────────────────────────────────
    _render_chat_ia(df_filtrato)


def _render_chat_ia(df: pd.DataFrame):
    """Render dell'area Chat IA di Ricerca in fondo alla dashboard."""
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    with st.expander("🤖 Chat IA di Ricerca (Text-to-SQL)", expanded=False):
        st.caption("Fai domande sui tuoi dati in linguaggio naturale. Questa funzione usa l'IA per interrogare il database.")
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []

        # Mostra storico chat
        for msg in st.session_state["chat_history"]:
            role_icon = "👤" if msg["role"] == "user" else "🤖"
            st.markdown(f"**{role_icon}:** {msg['content']}")

        domanda = st.text_input("La tua domanda...", key="chat_input", placeholder="es. Quante pratiche aperte ho questo mese?")
        col_invia, col_reset = st.columns([1, 4])
        with col_invia:
            if st.button("Invia", key="btn_chat_send"):
                if domanda and not df.empty:
                    # ── Risposta IA semplice basata su dati in memoria ─────────
                    risposta = _risposta_chat_ia(domanda, df)
                    st.session_state["chat_history"].append({"role": "user", "content": domanda})
                    st.session_state["chat_history"].append({"role": "assistant", "content": risposta})
                    st.rerun()
                elif df.empty:
                    st.warning("Nessun dato disponibile per rispondere.")
        with col_reset:
            if st.button("🗑️ Cancella storico", key="btn_chat_reset"):
                st.session_state["chat_history"] = []
                st.rerun()


def _risposta_chat_ia(domanda: str, df: pd.DataFrame) -> str:
    """
    Risponde alla domanda dell'utente usando Groq LLM con i dati del DataFrame
    come contesto. Fallback a messaggio di errore se Groq non è disponibile.
    """
    try:
        import openai

        groq_api_key = st.secrets.get("GROQ_API_KEY", "")
        groq_base_url = st.secrets.get("GROQ_BASE_URL", "https://api.groq.com/openai/v1")

        if not groq_api_key:
            return "⚠️ Chiave API Groq non configurata. Aggiungila in `.streamlit/secrets.toml`."

        # Serializza il DataFrame in CSV compatto (max 200 righe per non sforare i token)
        df_context = df.head(200).to_csv(index=False)

        system_prompt = f"""Sei un assistente database preciso per un gestionale di perizie assicurative.
Rispondi SOLO basandoti sui dati reali forniti qui sotto — non inventare informazioni.
Se la risposta non è ricavabile dai dati, dillo chiaramente.
Rispondi sempre in italiano, in modo conciso e diretto.

DATI CORRENTI (formato CSV, {len(df)} righe totali, mostrate le prime {min(len(df), 200)}):
{df_context}"""

        client_groq = openai.OpenAI(
            api_key=groq_api_key,
            base_url=groq_base_url,
        )

        response = client_groq.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": domanda},
            ],
            max_tokens=512,
            temperature=0.2,
        )
        print(f"--- CONSUMO GROQ [chat] --- Input: {response.usage.prompt_tokens} | Output: {response.usage.completion_tokens}")
        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Errore nella chiamata a Groq: {e}"


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2: NUOVA PRATICA / MODIFICA
# ══════════════════════════════════════════════════════════════════════════════
def render_form_pratica(client: Client):
    """Rendering del form di inserimento/modifica pratica."""

    # ── Contatore versione form (pattern reset affidabile) ──────────────────
    # Ogni widget ha la sua key suffissata con il numero di versione.
    # Incrementando il contatore, tutti i widget vengono ricreati da zero.
    if "form_ver" not in st.session_state:
        st.session_state["form_ver"] = 0
    ver = st.session_state["form_ver"]

    in_modifica = "pratica_in_modifica" in st.session_state and st.session_state["pratica_in_modifica"]
    dati = st.session_state.get("pratica_in_modifica", {}) or {}
    veicoli_esistenti = st.session_state.get("veicoli_in_modifica", []) or []

    # ── Inizializzazione session_state BLOCCO C ──
    if f"input_dinamica_{ver}" not in st.session_state:
        st.session_state[f"input_dinamica_{ver}"] = dati.get("dinamica_sintetica", "")
    if f"input_richieste_{ver}" not in st.session_state:
        st.session_state[f"input_richieste_{ver}"] = dati.get("richieste", "")
    if f"output_dinamica_{ver}" not in st.session_state:
        st.session_state[f"output_dinamica_{ver}"] = dati.get("dinamica_sintetica", "")
    if f"output_richieste_{ver}" not in st.session_state:
        st.session_state[f"output_richieste_{ver}"] = dati.get("richieste", "")
    # Alias senza versione per compatibilità con il resto del codice
    _k_in_din  = f"input_dinamica_{ver}"
    _k_in_req  = f"input_richieste_{ver}"
    _k_out_din = f"output_dinamica_{ver}"
    _k_out_req = f"output_richieste_{ver}"

    if in_modifica:
        st.markdown(f"## ✏️ Modifica Pratica — `{dati.get('numero_protocollo','')}`")
        col_back, _ = st.columns([1, 5])
        with col_back:
            if st.button("← Torna alla Dashboard", key="btn_back"):
                del st.session_state["pratica_in_modifica"]
                st.session_state.pop("veicoli_in_modifica", None)
                st.session_state["active_tab"] = "📊 Dashboard & Ricerca"
                st.rerun()
    else:
        st.markdown("## ➕ Nuova Pratica")

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # ══ BLOCCO A — ANAGRAFICA ════════════════════════════════════════════════
    st.markdown('<div class="block-header">📋 BLOCCO A — Anagrafica</div>', unsafe_allow_html=True)

    # Numero protocollo (generato o recuperato)
    numero_protocollo = dati.get("numero_protocollo") or genera_numero_protocollo()
    st.text_input("Numero Protocollo", value=numero_protocollo, disabled=True, key=f"field_protocollo_{ver}")

    # ── Riga 1: Dati identificativi assistito ─────────────────────────────────
    colA1, colA2, colA3 = st.columns(3)
    with colA1:
        cognome = st.text_input("Cognome Assistito *", value=dati.get("cognome_assistito", ""), key=f"field_cognome_{ver}")
    with colA2:
        nome = st.text_input("Nome Assistito", value=dati.get("nome_assistito", ""), key=f"field_nome_{ver}")
    with colA3:
        codice_fiscale = st.text_input("Codice Fiscale Assistito", value=dati.get("codice_fiscale_assistito", ""), key=f"field_cf_{ver}")

    # ── Riga 2: Compagnia, sinistro, data ────────────────────────────────────
    colB1, colB2, colB3 = st.columns(3)
    with colB1:
        compagnia = st.text_input("Compagnia Assicurativa", value=dati.get("compagnia", ""), key=f"field_compagnia_{ver}")
    with colB2:
        numero_sinistro = st.text_input("Numero Sinistro", value=dati.get("numero_sinistro", ""), key=f"field_numero_sinistro_{ver}")
    with colB3:
        data_sinistro_val = None
        if dati.get("data_sinistro"):
            try:
                data_sinistro_val = datetime.date.fromisoformat(str(dati["data_sinistro"]))
            except Exception:
                data_sinistro_val = None
        data_sinistro = st.date_input("Data Sinistro", value=data_sinistro_val, key=f"field_data_sinistro_{ver}")

    # ── Riga 3: Tipo dinamica, riparatore, stato ─────────────────────────────
    colC1, colC2, colC3 = st.columns(3)
    with colC1:
        tipo_dinamica = st.selectbox(
            "Tipo Dinamica",
            options=["cai", "60gg", "rca", "biologico"],
            index=["cai", "60gg", "rca", "biologico"].index(dati["tipo_dinamica"])
                   if dati.get("tipo_dinamica") in ["cai", "60gg", "rca", "biologico"] else 0,
            key=f"field_tipo_dinamica_{ver}",
        )
    with colC2:
        riparatore = st.text_input("Riparatore", value=dati.get("riparatore", ""), key=f"field_riparatore_{ver}")
    with colC3:
        stato_pratica = st.selectbox(
            "Stato Pratica",
            options=["Aperta", "In Chiusura", "Chiusa"],
            index=["Aperta", "In Chiusura", "Chiusa"].index(dati["stato_pratica"])
                   if dati.get("stato_pratica") in ["Aperta", "In Chiusura", "Chiusa"] else 0,
            key=f"field_stato_{ver}",
        )

    # ── Riga 4: Perito, liquidatore, importo stimato ─────────────────────────
    colD1, colD2, colD3 = st.columns(3)
    with colD1:
        perito_assegnato = st.text_input("Perito Assegnato", value=dati.get("perito_assegnato", ""), key=f"field_perito_{ver}")
    with colD2:
        liquidatore = st.text_input("Liquidatore", value=dati.get("liquidatore", ""), key=f"field_liquidatore_{ver}")
    with colD3:
        importo_raw = dati.get("importo_stimato", None)
        try:
            importo_default = float(importo_raw) if importo_raw not in (None, "") else 0.0
        except (ValueError, TypeError):
            importo_default = 0.0
        importo_stimato = st.number_input(
            "Importo Stimato (€)",
            min_value=0.0,
            value=importo_default,
            step=100.0,
            format="%.2f",
            key=f"field_importo_{ver}",
        )

    # ── Riga 5: Note generali ─────────────────────────────────────────────────
    note_generali = st.text_area("Note Generali", value=dati.get("note_generali", ""), height=80, key=f"field_note_{ver}")

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # ══ BLOCCO B — VEICOLI COINVOLTI ════════════════════════════════════════
    st.markdown('<div class="block-header">🚗 BLOCCO B — Veicoli Coinvolti</div>', unsafe_allow_html=True)

    num_veicoli_default = max(1, len(veicoli_esistenti)) if veicoli_esistenti else 1
    num_veicoli = st.number_input(
        "Numero veicoli coinvolti",
        min_value=1,
        max_value=10,
        value=num_veicoli_default,
        step=1,
        key=f"field_num_veicoli_{ver}",
    )

    dati_veicoli = []
    for i in range(int(num_veicoli)):
        ruolo = "Assistito" if i == 0 else f"Controparte {i}"
        v_esistente = veicoli_esistenti[i] if i < len(veicoli_esistenti) else {}

        st.markdown(
            f'<div class="vehicle-card"><div class="vehicle-title">🚘 Veicolo {i+1} — {ruolo}</div></div>',
            unsafe_allow_html=True,
        )
        with st.container():
            colV1, colV2 = st.columns(2)
            with colV1:
                targa = st.text_input(
                    f"Targa *", value=v_esistente.get("targa", ""), key=f"v_targa_{i}_{ver}"
                )
                conducente = st.text_input(
                    f"Conducente", value=v_esistente.get("conducente", ""), key=f"v_conducente_{i}_{ver}"
                )
            with colV2:
                modello = st.text_input(
                    f"Modello Auto", value=v_esistente.get("modello", ""), key=f"v_modello_{i}_{ver}"
                )
                proprietario = st.text_input(
                    f"Proprietario", value=v_esistente.get("proprietario", ""), key=f"v_proprietario_{i}_{ver}"
                )
        dati_veicoli.append(
            {
                "ruolo": ruolo,
                "targa": targa,
                "modello": modello,
                "conducente": conducente,
                "proprietario": proprietario,
            }
        )

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # ══ BLOCCO C — DINAMICA, RICHIESTE E TRASFORMAZIONE IA ══════════════════
    st.markdown('<div class="block-header">📝 BLOCCO C — Dinamica e Richieste</div>', unsafe_allow_html=True)

    # ─ CAMPO 1: Appunti grezzi dinamica (INPUT) ─────────────────────────────────
    st.text_area(
        "1. Dinamica Sintetica (Appunti Grezzi) *",
        key=_k_in_din,
        height=100,
        placeholder="Scrivi qui la dinamica in modo grezzo. L'IA la rielaborerà in forma ufficiale.",
    )

    # ─ CAMPO 2: Appunti grezzi richieste (INPUT) ───────────────────────────────
    st.text_area(
        "2. Richieste Danni (Appunti Grezzi)",
        key=_k_in_req,
        height=100,
        placeholder="Elenca le richieste in modo grezzo. L'IA le formalizzerà in linguaggio tecnico.",
    )

    # ─ PULSANTE IA ─────────────────────────────────────────────────────────────
    if st.button("🤖 Elabora e Trasforma con IA", key="btn_genera_ia"):
        dati_anag = {
            "numero_protocollo": numero_protocollo,
            "cognome_assistito": cognome,
            "nome_assistito": nome,
            "codice_fiscale_assistito": codice_fiscale,
            "numero_sinistro": numero_sinistro,
            "compagnia": compagnia,
            "perito_assegnato": perito_assegnato,
            "liquidatore": liquidatore,
            "data_sinistro": str(data_sinistro) if data_sinistro else "",
            "tipo_dinamica": tipo_dinamica,
            "riparatore": riparatore,
            "importo_stimato": importo_stimato,
        }
        errori_ia = []
        # Output 1: Dinamica formale — legge da _k_in_din
        try:
            with st.spinner("Rielaborazione dinamica in corso..."):
                dinamica_formale = elabora_dinamica_ia(
                    dati_anag, dati_veicoli,
                    st.session_state[_k_in_din]
                )
            st.session_state[_k_out_din] = dinamica_formale
        except Exception as e:
            errori_ia.append(f"Dinamica: {e}")
        # Output 2: Richieste formali — legge da _k_in_req
        try:
            with st.spinner("Formalizzazione richieste in corso..."):
                richieste_formali = elabora_richieste_ia(
                    dati_anag,
                    st.session_state[_k_in_req]
                )
            st.session_state[_k_out_req] = richieste_formali
        except Exception as e:
            errori_ia.append(f"Richieste: {e}")

        if errori_ia:
            for err in errori_ia:
                st.error(f"❌ Errore IA — {err}")
        else:
            st.success("✅ Testi elaborati dall'IA. Controlla e modifica prima di salvare.")
        st.rerun()

    # ─ CAMPO 3: Dinamica ufficiale (OUTPUT, modificabile) ──────────────────────
    st.text_area(
        "3. Dinamica Peritale Ufficiale (Modificabile) *",
        key=_k_out_din,
        height=150,
        placeholder="Qui apparirà la dinamica rielaborata dall'IA. Puoi modificarla prima di salvare.",
    )

    # ─ CAMPO 4: Richieste ufficiali (OUTPUT, modificabile) ─────────────────────
    st.text_area(
        "4. Analisi Richieste Ufficiale (Modificabile)",
        key=_k_out_req,
        height=150,
        placeholder="Qui apparirà l'analisi formalizzata delle richieste. Puoi modificarla prima di salvare.",
    )

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # ══ SALVATAGGIO ══════════════════════════════════════════════════════════
    # Totalmente indipendente dall'IA: funziona sempre, anche senza IA.
    col_save, col_clear = st.columns([2, 1])
    with col_save:
        if st.button("💾 Salva Pratica", type="primary", use_container_width=True, key="btn_salva"):
            errori = []
            if not cognome.strip():
                errori.append("Il campo **Cognome Assistito** è obbligatorio.")
            if any(not v["targa"].strip() for v in dati_veicoli):
                errori.append("La **Targa** è obbligatoria per ogni veicolo.")
            # Usa _k_out_din se compilato, altrimenti fallback su _k_in_din
            din_da_salvare = (st.session_state.get(_k_out_din) or "").strip() \
                             or (st.session_state.get(_k_in_din) or "").strip()
            if not din_da_salvare:
                errori.append("La **Dinamica Sintetica** è obbligatoria.")

            if errori:
                for e in errori:
                    st.error(e)
            else:
                # Fallback intelligente: output se presente, altrimenti input
                req_da_salvare = (st.session_state.get(_k_out_req) or "").strip() \
                                 or (st.session_state.get(_k_in_req) or "").strip()
                pratica_payload = {
                    "numero_protocollo": numero_protocollo,
                    "cognome_assistito": cognome.strip(),
                    "nome_assistito": nome.strip(),
                    "codice_fiscale_assistito": codice_fiscale.strip(),
                    "numero_sinistro": numero_sinistro.strip(),
                    "compagnia": compagnia.strip(),
                    "perito_assegnato": perito_assegnato.strip(),
                    "liquidatore": liquidatore.strip(),
                    "data_sinistro": str(data_sinistro) if data_sinistro else None,
                    "tipo_dinamica": tipo_dinamica,
                    "riparatore": riparatore.strip(),
                    "importo_stimato": importo_stimato if importo_stimato > 0 else None,
                    "note_generali": note_generali.strip(),
                    "stato_pratica": stato_pratica,
                    "dinamica_sintetica": din_da_salvare,   # Box 3 > Box 1
                    "richieste": req_da_salvare,            # Box 4 > Box 2
                }
                try:
                    with st.spinner("Salvataggio in corso..."):
                        ok, messaggio = salva_pratica(client, pratica_payload, dati_veicoli)
                    if ok:
                        st.success(messaggio)
                        if not in_modifica:
                            # Avanza la versione per svuotare il form dopo il salvataggio
                            st.session_state["form_ver"] = st.session_state.get("form_ver", 0) + 1
                            st.session_state.pop("pratica_in_modifica", None)
                            st.session_state.pop("veicoli_in_modifica", None)
                            st.rerun()
                    else:
                        st.error(messaggio)
                except Exception as e:
                    st.error(f"❌ Errore imprevisto durante il salvataggio: {e}")

    with col_clear:
        if st.button("🗑️ Svuota Form", use_container_width=True, key="btn_clear"):
            # Incrementa il contatore di versione: tutti i widget ricevono
            # nuove key e vengono ricreati da zero con i valori di default (vuoti).
            st.session_state["form_ver"] = st.session_state.get("form_ver", 0) + 1
            st.session_state.pop("pratica_in_modifica", None)
            st.session_state.pop("veicoli_in_modifica", None)
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3: SISTEMA & BACKUP
# ══════════════════════════════════════════════════════════════════════════════
def render_sistema(client: Client):
    st.markdown("## ⚙️ Sistema & Backup")
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # ── Stato connessioni ─────────────────────────────────────────────────────
    st.markdown("### 🔌 Stato Connessioni")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Supabase**")
        if client:
            try:
                client.table("pratiche").select("numero_protocollo").limit(1).execute()
                st.success("✅ Connesso a Supabase")
                st.caption(f"URL: `{st.secrets.get('SUPABASE_URL','N/D')[:40]}...`")
            except Exception as e:
                st.error(f"❌ Errore Supabase: {e}")
        else:
            st.error("❌ Client Supabase non inizializzato")

    with col2:
        st.markdown("**Groq IA**")
        groq_key = st.secrets.get("GROQ_API_KEY", "")
        groq_url = st.secrets.get("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
        if groq_key:
            st.success("✅ Chiave Groq presente")
            st.caption(f"Endpoint: `{groq_url}`")
        else:
            st.warning("⚠️ Chiave Groq assente — le funzioni IA non saranno disponibili")

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # ── Backup ───────────────────────────────────────────────────────────────
    st.markdown("### 💾 Backup & Export")

    col_btn, col_info = st.columns([1, 2])
    with col_btn:
        if st.button("📥 Genera Backup CSV", type="primary", use_container_width=True, key="btn_backup"):
            if client:
                with st.spinner("Recupero dati per il backup..."):
                    try:
                        resp_pratiche = client.table("pratiche").select("*").execute()
                        resp_veicoli  = client.table("soggetti_veicoli_coinvolti").select("*").execute()

                        df_pratiche = pd.DataFrame(resp_pratiche.data or [])
                        df_veicoli  = pd.DataFrame(resp_veicoli.data or [])

                        # Crea file zip in memoria con entrambi i CSV
                        import zipfile
                        buf = io.BytesIO()
                        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
                            zf.writestr("pratiche.csv", df_pratiche.to_csv(index=False))
                            zf.writestr("veicoli.csv",  df_veicoli.to_csv(index=False))
                        buf.seek(0)

                        nome_file = f"backup_perizie_{datetime.date.today().strftime('%Y%m%d')}.zip"
                        st.session_state["backup_data"] = buf.getvalue()
                        st.session_state["backup_nome"] = nome_file
                        st.session_state["backup_info"] = {
                            "pratiche": len(df_pratiche),
                            "veicoli": len(df_veicoli),
                        }
                        st.success(f"Backup generato: **{len(df_pratiche)}** pratiche, **{len(df_veicoli)}** veicoli.")
                    except Exception as e:
                        st.error(f"Errore durante il backup: {e}")
            else:
                st.error("Impossibile connettersi a Supabase.")

    with col_info:
        st.markdown(
            """
            Il backup genera un archivio `.zip` contenente:
            - `pratiche.csv` — tutte le pratiche
            - `veicoli.csv` — tutti i soggetti/veicoli

            Puoi poi salvarlo manualmente su Google Drive o su un bucket cloud.
            """
        )

    # Bottone download (appare solo dopo la generazione)
    if "backup_data" in st.session_state:
        st.download_button(
            label=f"⬇️ Scarica {st.session_state['backup_nome']}",
            data=st.session_state["backup_data"],
            file_name=st.session_state["backup_nome"],
            mime="application/zip",
            use_container_width=False,
            key="btn_download_backup",
        )

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # ── Info versione ─────────────────────────────────────────────────────────
    st.markdown("### ℹ️ Informazioni Sistema")
    st.markdown(f"""
    | Campo | Valore |
    |---|---|
    | Versione App | `1.0.0` |
    | Data Deploy | `{datetime.date.today()}` |
    | Utente attivo | `{st.session_state.get('username','N/D')}` |
    | Streamlit | `{st.__version__}` |
    """)


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
def render_sidebar() -> str:
    """Renderizza la sidebar e restituisce la tab selezionata."""
    with st.sidebar:
        st.markdown(
            f"""
            <div style="text-align:center; padding:1.5rem 0 1rem;">
                <span style="font-size:2.5rem;">🛡️</span>
                <h3 style="color:#c8d3e8; margin:0.5rem 0 0.2rem; font-weight:700;">Perizie Pro</h3>
                <p style="color:#6b7a99; font-size:0.85rem; margin:0;">
                    👤 {st.session_state.get('username','').capitalize()}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<hr style='border-color:#2d3748; margin:0 0 1rem;'>", unsafe_allow_html=True)

        tabs = ["📊 Dashboard & Ricerca", "➕ Nuova Pratica / Modifica", "⚙️ Sistema & Backup"]
        default_idx = tabs.index(st.session_state.get("active_tab", tabs[0]))
        tab_selezionata = st.radio(
            "Navigazione",
            tabs,
            index=default_idx,
            label_visibility="collapsed",
            key="nav_radio",
        )

        # Sincronizza active_tab con radio
        st.session_state["active_tab"] = tab_selezionata

        st.markdown("<hr style='border-color:#2d3748; margin:1rem 0;'>", unsafe_allow_html=True)

        # Logout
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True, key="btn_logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    return tab_selezionata


# ══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT PRINCIPALE
# ══════════════════════════════════════════════════════════════════════════════
def main():
    # Inizializzazione session_state
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "active_tab" not in st.session_state:
        st.session_state["active_tab"] = "📊 Dashboard & Ricerca"

    # ── Schermata di Login ────────────────────────────────────────────────────
    if not st.session_state["logged_in"]:
        render_login()
        return

    # ── Applicazione principale ───────────────────────────────────────────────
    client = get_supabase_client()
    if not client:
        st.error(
            "⚠️ Impossibile connettersi a Supabase. "
            "Verifica i valori in `.streamlit/secrets.toml`."
        )
        return

    tab_attiva = render_sidebar()

    if tab_attiva == "📊 Dashboard & Ricerca":
        render_dashboard(client)
    elif tab_attiva == "➕ Nuova Pratica / Modifica":
        render_form_pratica(client)
    elif tab_attiva == "⚙️ Sistema & Backup":
        render_sistema(client)


if __name__ == "__main__":
    main()
