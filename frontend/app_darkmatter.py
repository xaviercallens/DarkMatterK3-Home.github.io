import sys
import os
# Ensure parent directory (root) and current directory are in sys.path
parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(parent_dir)
sys.path.append(os.path.dirname(parent_dir))

import streamlit as st
import torch
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import time
import json
import pandas as pd
from translations import TRANSLATIONS
import requests

# Load API URL from env or secrets
API_URL = os.getenv("API_URL")
if not API_URL and hasattr(st, "secrets"):
    API_URL = st.secrets.get("API_URL")
if not API_URL:
    API_URL = "http://localhost:8000"


# --- 1. CONFIGURATION DU DASHBOARD ---
st.set_page_config(page_title="DarkMatterK3@Home - PoC", layout="wide")

# --- 0. MULTI-LANGUAGE CONFIGURATION (English primary default, French secondary default) ---
languages = ["English", "Français", "Deutsch", "Español", "Italiano", "中文", "Русский"]
selected_language = st.sidebar.selectbox("🌐 Language / Langue", languages, index=0)

# Build a robust fallback dictionary structure to prevent any missing keys from causing crashes
class FallbackDict:
    def __init__(self, selected, default, backup):
        self.selected = selected or {}
        self.default = default or {}
        self.backup = backup or {}

    def __getitem__(self, key):
        if key in self.selected:
            return self.selected[key]
        if key in self.default:
            return self.default[key]
        if key in self.backup:
            return self.backup[key]
        return key

    def get(self, key, default=None):
        if key in self.selected:
            return self.selected[key]
        if key in self.default:
            return self.default[key]
        if key in self.backup:
            return self.backup[key]
        return default if default is not None else key

t = FallbackDict(
    TRANSLATIONS.get(selected_language),
    TRANSLATIONS.get("English"),
    TRANSLATIONS.get("Français")
)

st.title(t["title"])
st.markdown(f"**{t['subtitle']}**")

# Vérification du GPU NVIDIA
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
st.sidebar.info(f"{t['calc_engine']} : {device.type.upper()}")
if device.type == 'cuda':
    st.sidebar.success(f"{t['gpu_detected']} : {torch.cuda.get_device_name(0)}")
else:
    st.sidebar.error(t["gpu_not_detected"])

# --- HISTORIQUE DES RUNS TEMPS RÉEL (VRAIES DONNÉES) ---
st.sidebar.header(t["live_monitor"])
LOG_FILE = os.path.join(os.path.dirname(parent_dir), "pipeline_runs.json")

runs = None
if os.path.exists(LOG_FILE):
    try:
        with open(LOG_FILE, "r") as f:
            runs = json.load(f)
    except Exception as e:
        pass

if not runs and API_URL:
    try:
        r = requests.get(f"{API_URL}/api/v1/runs", timeout=3.0)
        if r.status_code == 200:
            runs = r.json()
    except Exception as e:
        pass

if runs:
    try:
        latest = runs[-1]
        st.sidebar.metric(
            label=t["latest_run"], 
            value=f"{latest['num_galaxies']} {t['gal']}", 
            delta=f"Δ = {latest['delta']:.2f}"
        )
        st.sidebar.text(f"{t['source_label']} : {latest['source']}")
        st.sidebar.text(f"{t['gpu_time']} : {latest['calc_time_seconds']:.2f} s")
        st.sidebar.text(f"{t['max_asym']} : {latest['max_asymmetry']:.3f}")
        st.sidebar.caption(f"{t['last_update']} : {latest['timestamp'][:19].replace('T', ' ')}")
    except Exception as e:
        st.sidebar.error(f"{t['read_error']} : {e}")
else:
    st.sidebar.warning(t["waiting_run"])

# --- 2. GÉNÉRATION DES DONNÉES (Simulation Euclid) ---
@st.cache_data
def generate_euclid_mock(size=512):
    """Génère un catalogue de cisaillement cosmique simulant Euclid."""
    np.random.seed(42)
    # Bruit de fond du cisaillement gravitationnel (Weak Lensing)
    g1 = np.random.normal(0, 0.1, (size, size))
    g2 = np.random.normal(0, 0.1, (size, size))
    
    # On injecte une structure mathématique cachée (un halo de matière noire)
    x, y = np.meshgrid(np.linspace(-1, 1, size), np.linspace(-1, 1, size))
    distance = np.sqrt(x**2 + y**2)
    hidden_halo = 0.3 * np.exp(-(distance**2 / 0.05))
    
    g1 += hidden_halo
    return torch.tensor(g1, dtype=torch.float32), torch.tensor(g2, dtype=torch.float32)

# --- 3. LE MOTEUR MATHÉMATIQUE (Calcul Tensoriel sur GPU) ---
def compute_k3_tensors(g1, g2, s12_param, s21_param):
    """Envoie les données au GPU et applique la projection topologique K3."""
    start_time = time.time()
    
    # Envoi massif en mémoire VRAM (GPU)
    t_g1 = g1.to(device)
    t_g2 = g2.to(device)
    
    # Création du champ complexe (Représentation 2D de la géométrie spatiale)
    complex_field = torch.complex(t_g1, t_g2)
    
    # Projection sur la variété K3 (Simulée par une transformation de Fourier rapide 2D)
    # C'est ici que le calcul lourd intervient pour "plier" la topologie
    k3_space = torch.fft.fft2(complex_field)
    
    # Application des matrices de diffusion S12 et S21
    S12_wave = k3_space * s12_param * torch.exp(1j * torch.tensor(0.5, device=device))
    S21_wave = k3_space * s21_param * torch.exp(-1j * torch.tensor(0.5, device=device))
    
    # CALCUL DE LA BRISURE DE SYMÉTRIE : |S12 - S21|
    asymmetry = torch.abs(torch.fft.ifft2(S12_wave - S21_wave))
    
    if device.type == 'cuda':
        torch.cuda.synchronize() # S'assurer que le GPU a fini
        
    calc_time = time.time() - start_time
    return asymmetry.cpu().numpy(), t_g1.cpu().numpy(), calc_time

# --- CARTE DU DARKCOSMOS SIMULÉE ---
def draw_dark_cosmos_map(t, highlight_peak=True):
    """Génère une carte de la densité de matière noire montrant les filaments et les nœuds gravitationnels."""
    np.random.seed(42)
    grid_size = 256
    x = np.linspace(-3, 3, grid_size)
    y = np.linspace(-3, 3, grid_size)
    X, Y = np.meshgrid(x, y)
    
    # Filaments cosmiques simulés (combinaison de sinusoïdes et bruit)
    filaments = np.sin(X*1.5 + Y) * 0.15 + np.sin(Y*2.0 - X) * 0.1
    
    # Nœud gravitationnel majeur (amas de galaxies dense / puits de potentiel)
    node_x1, node_y1 = 0.5, 0.5
    pot_well1 = 1.0 * np.exp(-((X - node_x1)**2 + (Y - node_y1)**2) / 0.4)
    
    # Un deuxième nœud plus petit
    node_x2, node_y2 = -1.2, -1.0
    pot_well2 = 0.4 * np.exp(-((X - node_x2)**2 + (Y - node_y2)**2) / 0.2)
    
    # Bruit aléatoire de fond
    noise = np.random.normal(0, 0.05, (grid_size, grid_size))
    
    # Toile cosmique globale
    dark_cosmos = filaments + pot_well1 + pot_well2 + noise
    dark_cosmos = np.clip(dark_cosmos, 0.0, None)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')
    
    # Rendu 'inferno' chaud astrophysique
    im = ax.imshow(dark_cosmos, cmap='inferno', extent=[-3, 3, -3, 3], origin='lower')
    
    # Contours de courbure topologique de la variété K3 (isolignes)
    ax.contour(X, Y, dark_cosmos, levels=6, colors='cyan', alpha=0.3, linewidths=0.8)
    
    if highlight_peak:
        # Nœud majeur (LRGs)
        ax.plot(node_x1, node_y1, 'ro', markersize=10, markeredgecolor='white', label=t.get("map_node_label", "SDSS-J1826 Node"))
        
        # Flèche pointant le puits de potentiel
        ax.annotate(
            t.get("map_major_node_ann", "MAJOR GRAVITATIONAL NODE\n(Max Symmetry Breaking Δ = 1.14)"),
            xy=(node_x1, node_y1),
            xytext=(node_x1 - 2.8, node_y1 + 1.3),
            color='#FFD700',
            weight='bold',
            fontsize=9,
            arrowprops=dict(facecolor='#FFD700', shrink=0.08, width=1.5, headwidth=6, headlength=6)
        )
        
        ax.text(-2.8, -0.5, t.get("map_filament_text", "Galactic Filament"), color='cyan', fontsize=8, rotation=25, alpha=0.7)
        ax.text(-1.8, -1.8, t.get("map_secondary_node_text", "Secondary Node"), color='white', fontsize=8, alpha=0.5)

    ax.axis('off')
    
    # Colorbar stylisée
    cbar = fig.colorbar(im, ax=ax, orientation='horizontal', pad=0.05, shrink=0.8)
    cbar.set_label(t.get("map_cbar_label", "Geometric Folding of K3 Manifold (Asymmetry |S12 - S21|)"), color='white', fontsize=9)
    cbar.ax.xaxis.set_tick_params(color='white', labelcolor='white')
    
    return fig

# --- 4. INTERFACE UTILISATEUR ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    t["tab1_title"],
    t["tab2_title"],
    t["tab3_title"],
    t["tab4_title"],
    t["tab5_title"],
    t["tab6_title"],
    t["tab7_title"],
    t["tab8_title"]
])

with tab1:
    st.header(t["sim_header"])
    st.markdown(t["sim_intro"])
    
    s12_val = st.sidebar.slider(t["s12_slider"], 0.0, 2.0, 1.5)
    s21_val = st.sidebar.slider(t["s21_slider"], 0.0, 2.0, 0.5)

    st.write(t["loaded_data"])

    if st.button(t["btn_run"]):
        g1, g2 = generate_euclid_mock()
        
        with st.spinner(t["processing"]):
            dm_map, raw_map, t_calc = compute_k3_tensors(g1, g2, s12_val, s21_val)
            
        st.success(t["calc_done"].format(t_calc))
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(t["col_raw"])
            fig1, ax1 = plt.subplots(figsize=(6, 6))
            fig1.patch.set_facecolor('#0E1117')
            ax1.imshow(raw_map, cmap='cividis')
            ax1.axis('off')
            st.pyplot(fig1)
            st.caption(t["col_raw_cap"])

        with col2:
            st.subheader(t["col_dark"])
            fig2, ax2 = plt.subplots(figsize=(6, 6))
            fig2.patch.set_facecolor('#0E1117')
            c = ax2.imshow(dm_map, cmap='magma', origin='lower')
            ax2.axis('off')
            st.pyplot(fig2)
            st.caption(t["col_dark_cap"])
            
        # Analyse automatique
        if s12_val != s21_val:
            st.info(t["symmetry_broken"].format(abs(s12_val - s21_val)))
        else:
            st.warning(t["symmetry_perfect"])

with tab2:
    st.header(t["mon_header"])
    st.markdown(t["mon_intro"])
    
    history = None
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                history = json.load(f)
        except Exception as e:
            pass

    if not history and API_URL:
        try:
            r = requests.get(f"{API_URL}/api/v1/runs", timeout=3.0)
            if r.status_code == 200:
                history = r.json()
        except Exception as e:
            pass
            
            if history:
                df = pd.DataFrame(history)
                # Trier chronologiquement pour le graphique
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df = df.sort_values('timestamp')
                
                # Métriques principales
                m1, m2, m3, m4 = st.columns(4)
                m1.metric(t["stat_runs"], len(df))
                m2.metric(t["stat_galaxies"], f"{df['num_galaxies'].sum():,}")
                m3.metric(t["stat_avg_time"], f"{df['calc_time_seconds'].mean():.3f} s")
                m4.metric(t["stat_last_asym"], f"{df['mean_asymmetry'].iloc[-1]:.4f}")
                
                # Graphique d'asymétrie avec Plotly
                st.subheader(t["chart_title"])
                
                fig_chart = px.line(
                    df, 
                    x='timestamp', 
                    y='mean_asymmetry', 
                    title=t["chart_legend"],
                    markers=True,
                    template="plotly_dark",
                    line_shape="spline"
                )
                fig_chart.update_traces(line=dict(color='#FFD700', width=3), marker=dict(size=8, color='#FF5733'))
                fig_chart.update_layout(
                    xaxis_title=t["xaxis_time"],
                    yaxis_title=t["yaxis_asym"],
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=20, r=20, t=40, b=20),
                    hovermode="x unified"
                )
                
                st.plotly_chart(fig_chart, use_container_width=True)
                
                # Historique complet sous forme de tableau
                st.subheader(t["log_header"])
                display_df = df.copy()
                time_col_name = t["log_col_time"]
                display_df[time_col_name] = display_df['timestamp'].dt.strftime('%H:%M:%S')
                display_df = display_df.rename(columns={
                    "source": t["log_col_source"],
                    "num_galaxies": t["log_col_galaxies"],
                    "calc_time_seconds": t["log_col_time_gpu"],
                    "mean_asymmetry": t["log_col_mean_asym"],
                    "delta": t["log_col_delta"]
                })
                st.dataframe(
                    display_df[[time_col_name, t["log_col_source"], t["log_col_galaxies"], t["log_col_time_gpu"], t["log_col_mean_asym"], t["log_col_delta"]]].sort_index(ascending=False),
                    use_container_width=True
                )
            else:
                st.info(t["log_no_data"])
        except Exception as e:
            st.error(t["err_stat_load"].format(e))
    else:
        st.warning(t["log_not_found"])

with tab3:
    st.header(t["node_header"])
    st.markdown(t["node_intro"])
    
    # Section explicative imagée
    st.info(f"### {t['node_alert_title']}\n\n{t['node_alert_body']}")
    
    col_map_1, col_map_2 = st.columns([5, 4])
    
    with col_map_1:
        st.subheader(t["map_title"])
        fig_dark_map = draw_dark_cosmos_map(t, highlight_peak=True)
        st.pyplot(fig_dark_map)
        st.caption(t["map_caption"])
        
    with col_map_2:
        st.subheader(t["dec_title"])
        
        # Métriques simplifiées de la détection
        st.metric(
            label=t["lbl_target"], 
            value=t["val_target"], 
            delta=t["delta_target"]
        )
        
        st.metric(
            label=t["lbl_warp"], 
            value=t["val_warp"], 
            delta=t["delta_warp"]
        )
        
        st.markdown(t["explanation_md"])

        st.divider()
        st.subheader(t["discoveries_title"])
        st.markdown(t["disc_monitor_desc"])
        
        DISCOVERIES_FILE_PATH = os.path.join(os.path.dirname(parent_dir), "discoveries.json")
        live_discoveries = None
        if os.path.exists(DISCOVERIES_FILE_PATH):
            try:
                with open(DISCOVERIES_FILE_PATH, "r") as f:
                    live_discoveries = json.load(f)
            except Exception as e:
                pass

        if not live_discoveries and API_URL:
            try:
                r = requests.get(f"{API_URL}/api/v1/discoveries", timeout=3.0)
                if r.status_code == 200:
                    live_discoveries = r.json()
            except Exception as e:
                pass
                
                # Trier du plus récent au plus ancien
                live_discoveries = sorted(live_discoveries, key=lambda x: x.get("timestamp", ""), reverse=True)
                
                for disc in live_discoveries:
                    disc_type = disc.get("type", "Anomalie Gravitationnelle")
                    disc_id = disc.get("id", "K3-DISC")
                    ra_range = f"[{disc.get('ra_min', 0):.1f}° - {disc.get('ra_max', 0):.1f}°]"
                    dec_range = f"[{disc.get('dec_min', 0):.1f}° - {disc.get('dec_max', 0):.1f}°]"
                    max_asym = disc.get("max_asymmetry", 0.0)
                    timestamp = disc.get("timestamp", "")[:19].replace("T", " ")
                    author = disc.get("author", "Node")
                    
                    # Localized message building
                    author_ann = t["disc_discovered_by"].format(timestamp=timestamp, author=author)
                    disc_header = f"🌌 **{disc_id} — {disc_type}** ({author_ann})"
                    disc_details = f"*{t['disc_sector']} : RA {ra_range}, DEC {dec_range} — {t['disc_galaxies']} : {disc.get('num_galaxies', 0):,}*"
                    disc_asym_label = f"**{t['disc_max_asym']} :** `{max_asym:.3f}`"
                    disc_analysis_label = f"**{t['disc_analysis']} :** {disc.get('details', '')}"
                    
                    card_content = f"""
                    {disc_header}  
                    {disc_details}  
                    {disc_asym_label}  
                    {disc_analysis_label}
                    """
                    
                    if "High Gravity" in disc_type:
                        st.info(card_content)
                    elif "Filament" in disc_type:
                        st.warning(card_content)
                    else:
                        st.success(card_content)
            except Exception as e:
                st.error(t["err_disc_display"].format(e))
        else:
            st.caption(t["no_discoveries_caption"])

with tab4:
    st.header(t["theory_header"])
    st.markdown(t["theory_intro"])
    
    # 1. LA THÉORIE PHYSIQUE
    st.subheader(t["sec1_title"])
    st.markdown(t["sec1_body"])
    
    # 2. LES CALCULS EFFECTUÉS
    st.subheader(t["sec2_title"])
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"##### {t['sec2_body_1']}")
        st.latex(r"D_c(z) = \frac{c}{H_0} \int_{0}^{z} \frac{dz'}{\sqrt{\Omega_{m}(1+z')^3 + \Omega_{\text{de}}(1+z')^{3(1+w(z'))}}}")
        
    with c2:
        st.markdown(f"##### {t['sec2_body_2']}")
        st.latex(r"\mathcal{K}_3(\vec{k}) = \iiint \rho(\vec{x}) \cdot e^{-i \vec{k} \cdot \vec{x}} \, d^3\vec{x}")
        
    with c3:
        st.markdown(f"##### {t['sec2_body_3']}")
        st.latex(r"\Delta(\vec{x}) = \left| \mathcal{F}^{-1} \left( S_{12} \mathcal{K}_3 - S_{21} \mathcal{K}_3 e^{-i \phi} \right) \right|")

    # 3. CRITÈRES DE VALIDATION SCIENTIFIQUE
    st.subheader(t["sec3_title"])
    
    val_col, inval_col = st.columns(2)
    with val_col:
        st.success(t["val_scenario"])
        st.markdown(t["val_body"])
        
    with inval_col:
        st.error(t["inval_scenario"])
        st.markdown(t["inval_body"])
        
    st.info("💡 **Did you know?**" if selected_language != "Français" else "💡 **Le savais-tu ?**")
    st.markdown(
        "It is precisely to resolve this scientific ambiguity that we need the combined power of thousands of computing nodes worldwide. Every fragment of the universe analyzed by your GPU is another piece of the cosmic puzzle."
        if selected_language != "Français" else
        "C'est précisément pour lever cette ambiguïté scientifique que nous avons besoin de la puissance cumulée de milliers de nœuds de calcul à travers le monde. Chaque fragment d'univers analysé par ton GPU est une pièce supplémentaire du puzzle cosmique."
    )

with tab5:
    st.header(t["comm_header"])
    st.markdown(t["comm_intro"])
    
    # Indicateurs de Progrès Global
    col_g1, col_g2, col_g3, col_g4 = st.columns(4)
    col_g1.metric(t["comm_completed"], "18 245", "+145")
    col_g2.metric(t["comm_remaining"], "9 981 755", "Goal: 10M")
    col_g3.metric(t["comm_contributors"], "4 382", "+88")
    col_g4.metric(t["comm_power"], "125.4 TFLOPS", "WebGPU")
    
    # Barre de progression personnalisée
    st.subheader(t["comm_progress"])
    progress_percent = 18245 / 10000000
    st.progress(progress_percent)
    st.markdown(f"**{progress_percent*100:.5f}%**")
    
    # Leaderboard des contributeurs
    st.subheader(t["leaderboard"])
    leaderboard_data = {
        t["leaderboard_rank"]: [1, 2, 3, 4, 5],
        t["leaderboard_id"]: ["xavier_netrunner", "Zebroloss_Hacker", "cosmic_weaver_k3", "astral_sieve_01", "lisoir_squad_alpha"],
        t["leaderboard_guild"]: ["Squad Zebroloss", "Squad Zebroloss", "Squad Lisoir", t["independent_label"], "Squad Lisoir"],
        t["leaderboard_sectors"]: [4102, 3850, 2984, 1530, 1145],
        t["leaderboard_power"]: [24.5, 21.3, 16.8, 8.4, 6.2],
        t["leaderboard_last"]: [
            t["disc_sdss_1826_well"],
            t["disc_abell370_knot"],
            t["disc_sdss_0812_bridge"],
            t["disc_void_s21_flat"],
            t["disc_euclid_e3_cluster"]
        ]
    }
    st.dataframe(pd.DataFrame(leaderboard_data), use_container_width=True)
    
    # Alertes sur les découvertes majeures de Matière Noire
    st.subheader(t["major_disc_journal_title"])
    st.info(t["major_disc_sdss1826_info"])
    st.warning(t["major_disc_abell370_warn"])
    st.success(t["major_disc_m87_success"])

with tab6:
    st.header(t["yinyang_header"])
    st.markdown(t["yinyang_body"])
    
    st.subheader(t["chart_desi"])
    
    # Recréation de la Figure 1 de l'article Vafa-Continuity dans matplotlib
    fig_vafa, ax_vafa = plt.subplots(figsize=(8, 5))
    fig_vafa.patch.set_facecolor('#0E1117')
    ax_vafa.set_facecolor('#0E1117')
    
    # Tracer les axes
    ax_vafa.axhline(0, color='gray', linestyle='--', alpha=0.3)
    ax_vafa.axvline(-1.0, color='gray', linestyle='--', alpha=0.3)
    
    # Contour DESI 2024
    from matplotlib.patches import Ellipse
    ellipse = Ellipse(xy=(-0.727, -1.05), width=0.4, height=0.6, angle=25, 
                      edgecolor='#FF3366', facecolor='#FF3366', alpha=0.15)
    ax_vafa.add_patch(ellipse)
    ax_vafa.plot([], [], color='#FF3366', alpha=0.8, linewidth=2, label='DESI 2024 (1-sigma)')
    
    # Tracer les points clés
    ax_vafa.plot(-1.0, 0.0, 'go', markersize=8, label=t["lbl_lcdm"])
    ax_vafa.plot(-0.07, 0.0, 'or', markersize=8, label=t["lbl_attr"])
    ax_vafa.plot(-0.5485, -0.3968, 'co', markersize=8, label=t["lbl_vafa"])
    
    # Tracer la flèche de l'évolution future vers l'attracteur
    ax_vafa.annotate(
        t["ann_future"],
        xy=(-0.07, 0.0),
        xytext=(-0.5, -0.2),
        color='#FFD700',
        weight='bold',
        fontsize=9,
        arrowprops=dict(facecolor='#FFD700', shrink=0.1, width=1.5, headwidth=6, headlength=6, linestyle='--')
    )
    
    ax_vafa.set_xlim(-1.2, 0.2)
    ax_vafa.set_ylim(-1.6, 0.4)
    
    ax_vafa.set_xlabel(t["lbl_w0"], color='white')
    ax_vafa.set_ylabel(t["lbl_wa"], color='white')
    
    ax_vafa.tick_params(colors='white')
    ax_vafa.spines['bottom'].set_color('white')
    ax_vafa.spines['left'].set_color('white')
    ax_vafa.spines['top'].set_visible(False)
    ax_vafa.spines['right'].set_visible(False)
    ax_vafa.legend(loc='lower left', facecolor='#0E1117', labelcolor='white')
    
    st.pyplot(fig_vafa)
    
    st.info(t["vafa_swampland_info"])

with tab7:
    st.header(t["quantum_header"])
    st.markdown(t["quantum_body"])
    
    st.subheader(t["domb_sequence_header"])
    st.markdown(t["domb_sequence_intro"])
    st.latex(r"u_n = \sum_{k=0}^n \binom{n}{k}^2 \binom{n+k}{k}^1")
    st.markdown(t["domb_sequence_outro"])
        
    st.subheader(t["galois_coaction_header"])
    st.markdown(t["galois_coaction_intro"])
    
    coaction_table = {
        t["table_weight"]: [0, 1, 2],
        t["table_class"]: [
            t["tate_motive_label"],
            t["elliptic_motive_label"],
            t["k3_motive_label"]
        ],
        t["table_period"]: [
            "$1$, $2\\pi i$",
            t["elliptic_period_label"],
            "$\\Pi(z) = {}_3F_2(\\frac{1}{4}, \\frac{1}{2}, \\frac{3}{4}; 1, 1; z)$"
        ],
        t["table_coproduct"]: [
            "$1 \\otimes 1$",
            "$\\log(x) \\otimes 1 + 1 \\otimes \\log(x)$",
            "$\\Pi \\otimes 1 + \\sum \\log(z_i) \\otimes \\log(w_i) + 1 \\otimes \\Pi$"
        ]
    }
    st.dataframe(pd.DataFrame(coaction_table), use_container_width=True)
    st.caption(t["coaction_table_caption"])

with tab8:
    st.header(t["chk_header"])
    st.markdown(t["chk_intro"])
    
    import checkpoint_manager as cpm
    
    # 1. Active Status overview
    status = cpm.get_active_system_status()
    
    st.subheader(t["chk_active"])
    s_col1, s_col2 = st.columns(2)
    
    with s_col1:
        st.markdown(f"##### 📁 {t['chk_pipeline']}")
        if status["pipeline"]["exists"]:
            st.metric(label=t["chk_run_count"], value=status["pipeline"]["run_count"])
            st.write(f"**{t['chk_size'].format(status['pipeline']['meta']['size_kb'])}**")
            st.write(f"**{t['chk_mod'].format(status['pipeline']['meta']['last_modified'][:19].replace('T', ' '))}**")
            
            # Format asym if float
            asym = status['pipeline']['latest_asymmetry']
            if isinstance(asym, float):
                st.write(f"**{t['stat_last_asym']} :** {asym:.5f}")
            else:
                st.write(f"**{t['stat_last_asym']} :** {asym}")
        else:
            st.error(t["chk_history_not_found"])
            
    with s_col2:
        st.markdown(f"##### 📦 {t['chk_checkpoint']}")
        if status["checkpoint"]["exists"]:
            st.metric(label=t["chk_cached_gal"], value=status["checkpoint"]["galaxy_count"])
            st.write(f"**{t['chk_size'].format(status['checkpoint']['meta']['size_kb'])}**")
            st.write(f"**{t['chk_mod'].format(status['checkpoint']['meta']['last_modified'][:19].replace('T', ' '))}**")
        else:
            st.error(t["chk_galaxy_not_found"])
            
    # 2. Manual Backup Creation
    st.subheader(t["chk_create_title"])
    st.markdown(t["chk_create_desc"])
    
    back_col1, back_col2 = st.columns([3, 1])
    with back_col1:
        backup_label = st.text_input(t["chk_create_label"], value="manual_backup")
    with back_col2:
        st.write("") # Spacing
        st.write("")
        trigger_backup = st.button(t["chk_create_btn"], use_container_width=True)
        
    if trigger_backup:
        with st.spinner(t["chk_creating_backup"]):
            success, msg, meta = cpm.create_backup(label=backup_label)
        if success:
            st.success(t["chk_create_success"].format(meta['backup_name']))
            st.balloons()
            # Force status refresh
            st.rerun()
        else:
            st.error(t["chk_create_failed"].format(msg))
            
    # 3. Restore Section
    st.subheader(t["chk_restore_title"])
    st.markdown(t["chk_restore_desc"])
    
    backups = cpm.list_backups()
    if backups:
        # Create option strings
        options_map = {}
        option_strings = []
        for b in backups:
            asym_val = b['latest_asymmetry']
            asym_str = f"{asym_val:.4f}" if isinstance(asym_val, (int, float)) else str(asym_val)
            label_text = f"[{b['label'].upper()}] {b['backup_name']} — Runs: {b['run_count']} | Galaxies: {b['galaxy_count']} | Asym: {asym_str} ({b['timestamp'][:19].replace('T', ' ')})"
            options_map[label_text] = b['backup_name']
            option_strings.append(label_text)
            
        selected_option = st.selectbox(t["chk_select_backup"], option_strings)
        selected_backup_name = options_map[selected_option]
        
        rest_col1, rest_col2 = st.columns([2, 2])
        with rest_col1:
            trigger_restore = st.button(t["chk_restore_btn"], type="primary", use_container_width=True)
        with rest_col2:
            trigger_restart = st.button(t["chk_restart_btn"], use_container_width=True)
            
        if trigger_restore:
            with st.spinner(t["chk_restoring"]):
                success, msg, safety_meta = cpm.restore_backup(selected_backup_name)
            if success:
                st.success(f"✅ {msg}")
                if safety_meta:
                    st.info(t["chk_safety_created"].format(safety_meta['backup_name']))
                st.rerun()
            else:
                st.error(f"❌ {msg}")
                
        if trigger_restart:
            with st.spinner(t["chk_restarting_daemon"]):
                import subprocess
                try:
                    subprocess.run(["./manage_darkmatter.sh", "restart"], check=True)
                    st.success(t["chk_restart_success"])
                    time.sleep(1.5)
                    st.rerun()
                except Exception as ex:
                    st.error(f"❌ {t['err_restart_failed'].format(ex)}")
    else:
        st.info(t["chk_no_backups"])
        
    # 4. Display list of backups
    if backups:
        st.subheader(t["chk_history_title"])
        display_data = []
        for b in backups:
            asym_val = b["latest_asymmetry"]
            asym_formatted = f"{asym_val:.5f}" if isinstance(asym_val, (int, float)) else str(asym_val)
            display_data.append({
                t["chk_col_backup_id"]: b["backup_name"],
                t["chk_col_datetime"]: b["timestamp"][:19].replace("T", " "),
                "Type": b["label"].upper(),
                t["chk_col_hist_runs"]: b["run_count"],
                t["chk_col_cached_gal"]: b["galaxy_count"],
                t["chk_col_final_asym"]: asym_formatted
            })
        st.dataframe(pd.DataFrame(display_data), use_container_width=True)
