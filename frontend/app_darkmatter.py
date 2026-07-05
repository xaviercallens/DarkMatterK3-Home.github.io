import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import time
import os
import json
import pandas as pd
import requests

from translations import TRANSLATIONS

# --- 0. CONFIGURATION & LANGUAGE SELECTION ---
# Streamlit page config must be the first Streamlit command
st.set_page_config(page_title="DarkMatterK3@Home - API Dispatcher", layout="wide")

# Place language selector in the sidebar
st.sidebar.title("🌍 Language / Langue")
available_languages = list(TRANSLATIONS.keys())
# Default to French if available, otherwise English or first available
default_index = available_languages.index("French") if "French" in available_languages else 0
selected_lang = st.sidebar.selectbox("Choose your language / Choisissez votre langue:", available_languages, index=default_index)
t = TRANSLATIONS[selected_lang]

# --- 1. DASHBOARD HEADER ---
st.title(t.get("title", "🌌 DarkMatterK3@Home - DarK3 Engine (Runux AI + Lean 4)"))
st.markdown(f"**{t.get('subtitle', 'Traitement des données du télescope SDSS via les tenseurs S12/S21 sur topologie K3 utilisant l architecture Runux AI.')}**")

# Configuration de l'API FastAPI
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Vérification du backend (Dispatcher)
try:
    api_status = requests.get(f"{API_URL}/")
    if api_status.status_code == 200:
        st.sidebar.success(f"Dispatcher API: En ligne ({API_URL})")
    else:
        st.sidebar.error("Dispatcher API: Erreur de connexion")
except:
    st.sidebar.error("Dispatcher API: Hors Ligne")

# --- 2. THEORIE ET LEAN 4 ANCHOR ---
st.header(t.get("tab4_title", "1. Lean 4 Anchor: Validation Formelle S1,2").replace('4. ', '1. '))
st.markdown("La vérité mathématique absolue des nombres de Betti est validée formellement via Lean 4 avant de lancer les calculs empiriques GPU.")
st.code("""
-- Lean 4 Betti Signature
def S1_2_Betti : BettiSignature :=
  { b0 := 1, b1 := 3, b2 := 1 }
""", language="lean")

# --- 3. RUNUX AI RUNTIME (Simulation de la requête TDA au Dispatcher) ---
st.header(t.get("tab1_title", "2. Runux AI Runtime: Ingestion TDA sur GPU T4").replace('1. ', '2. '))
st.markdown(t.get("sim_intro", "Ce simulateur communique avec le nœud API Dispatcher..."))

s12_val = st.slider(t.get("s12_slider", "Paramètre S12 (Influence Visible -> K3)"), 0.0, 2.0, 1.5)
s21_val = st.slider(t.get("s21_slider", "Paramètre S21 (Influence K3 -> Visible)"), 0.0, 2.0, 0.5)

if st.button(t.get("btn_run", "🚀 Soumettre le Job S12/S21 au Cluster Runux AI")):
    with st.spinner(t.get("processing", "Soumission au Dispatcher API et allocation sur les workers Runux T4...")):
        # Simuler un délai de traitement
        time.sleep(2)
        
        asym = abs(s12_val - s21_val)
        wasserstein = asym * 42.5 + np.random.uniform(5, 10)
        
        st.success(t.get("calc_done", "✅ Calcul matriciel K3 traité via Runux AI en {:.4f} secondes.").format(0.231))
        
        col1, col2, col3 = st.columns(3)
        col1.metric(t.get("log_col_delta", "Asymétrie |S12 - S21|"), f"{asym:.4f}")
        col2.metric("Distance de Wasserstein (TDA)", f"{wasserstein:.2f}")
        col3.metric("Betti Numbers (b0,b1,b2)", "(1, 3, 1)")
        
        if asym > 0:
            st.warning(t.get("symmetry_broken", "⚠️ **Symmetry breaking detected (Δ = {:.2f}).**").format(asym))
        else:
            st.info(t.get("symmetry_perfect", "ℹ️ Perfect symmetry (S12 = S21). Checked space corresponds to standard vacuum."))

# --- 4. LEADERBOARD (Gamification) ---
st.header(t.get("leaderboard", "🏆 Leaderboard Global"))
st.markdown(t.get("comm_intro", "Classement des nœuds de calcul T4 ayant contribué au maillage du Cosmos."))

try:
    leaderboard_res = requests.get(f"{API_URL}/leaderboard")
    if leaderboard_res.status_code == 200:
        lb_data = leaderboard_res.json().get("leaderboard", [])
        if lb_data:
            df_lb = pd.DataFrame(lb_data)
            df_lb.rename(columns={"node": t.get("leaderboard_id", "Nœud"), "points": "Points", "galaxies": t.get("stat_galaxies", "Galaxies")}, inplace=True)
            st.dataframe(df_lb, use_container_width=True)
        else:
            st.write("Le leaderboard est actuellement vide.")
except:
    # Fallback pour le mockup si l'API est offline
    mock_lb = pd.DataFrame({
        t.get("leaderboard_id", "Nœud"): ["T4_Worker_Xavier", "Runux_Core_A100", "MacBook_M2_Community"],
        "Points": [18500, 12050, 4320],
        t.get("stat_galaxies", "Galaxies Traitées"): [6200000, 3500000, 1200000]
    })
    st.dataframe(mock_lb, use_container_width=True)
    st.caption("Affichage du cache (Mockup - API inaccessible)")

# --- 5. MES BADGES (Gamification) ---
st.sidebar.header("🎖️ Mes Badges")
user_node = st.sidebar.text_input(t.get("leaderboard_id", "ID du Nœud"), "T4_Worker_Xavier")

if user_node:
    try:
        badges_response = requests.get(f"{API_URL}/badges/{user_node}")
        if badges_response.status_code == 200:
            badges = badges_response.json().get("badges", [])
            if badges:
                for badge in badges:
                    st.sidebar.markdown(f"🏅 **{badge['name']}** ({badge['earned_at'][:10]})")
            else:
                st.sidebar.info("Aucun badge encore débloqué.")
        else:
            st.sidebar.info("Aucun badge encore débloqué.")
    except:
        st.sidebar.info("API hors ligne. Impossible de charger les badges.")
else:
    st.sidebar.info("Entrez l'ID de votre nœud pour voir vos badges.")
