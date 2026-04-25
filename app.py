import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import base64

st.set_page_config(
    page_title="Titanic · Análisis de Supervivencia y Rentabilidad",
    page_icon="🚢",
    layout="wide"
)

# ─────────────────────────────────────────────
# ESTILOS GLOBALES — tema marítimo, alto contraste
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Source+Sans+3:wght@300;400;600&display=swap');

/* ── Fondo ── */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(160deg, #0c1e38 0%, #0f2848 40%, #122f54 100%);
    background-attachment: fixed;
}
[data-testid="stHeader"] { background: transparent; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #091828 0%, #0d2240 100%);
    border-right: 1px solid rgba(200,168,75,0.4);
}
[data-testid="stSidebar"] * { color: #f0f6fc !important; }
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span { color: #e8f2fc !important; }
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #f0c84a !important;
    font-family: 'Playfair Display', serif;
}
[data-testid="stSidebar"] a { color: #80c4f0 !important; }

/* ── Tipografía global ── */
html, body, [class*="css"], p, span, li, td, th, div {
    font-family: 'Source Sans 3', sans-serif;
    color: #f0f6fc;
}
h1, h2, h3 { font-family: 'Playfair Display', serif; color: #f5ecd5; }

/* ── Texto en dataframes ── */
[data-testid="stDataFrame"] * { color: #ffffff !important; }
[data-testid="stDataFrame"] th { color: #f0c84a !important; font-weight: 700; }
.stDataFrame { border-radius: 10px; }
iframe { color-scheme: dark; }

/* ── Texto en tablas markdown ── */
.stMarkdown table td { color: #f0f6fc !important; }
.stMarkdown table th { color: #f0c84a !important; }

/* ── Hero portada ── */
.hero-wrap {
    display: flex; align-items: center; gap: 40px;
    background: linear-gradient(135deg, rgba(8,24,52,0.96), rgba(6,16,36,0.98));
    border: 1px solid rgba(200,168,75,0.5);
    border-radius: 18px; padding: 36px 44px; margin-bottom: 10px;
    box-shadow: 0 10px 48px rgba(0,0,0,0.6), 0 0 0 1px rgba(200,168,75,0.1) inset;
}
.hero-ship { flex: 0 0 auto; }
.hero-text { flex: 1; min-width: 0; }
.hero-rms {
    font-size: 0.8rem; color: #d4aa50;
    letter-spacing: 6px; text-transform: uppercase; margin-bottom: 4px;
}
.hero-title {
    font-family: 'Playfair Display', serif; font-size: 3.6rem; font-weight: 900;
    color: #fff8e8; letter-spacing: 2px;
    text-shadow: 0 2px 30px rgba(200,160,40,0.5); line-height: 1.05; margin: 0 0 8px;
}
.hero-subtitle {
    font-size: 1.02rem; color: #cce6f8; letter-spacing: 0.4px;
    line-height: 1.5; margin-bottom: 18px;
}
.hero-gold-line {
    height: 2px; width: 80%; border: none; margin: 12px 0 16px;
    background: linear-gradient(90deg, #d4aa50, rgba(200,168,75,0.1));
}
.hero-uni-tag {
    font-size: 0.7rem; color: #b8d4e8;
    text-transform: uppercase; letter-spacing: 2.5px; margin-bottom: 4px;
}
.hero-uni-name {
    font-family: 'Playfair Display', serif;
    font-size: 1.2rem; font-weight: 700; color: #ffe98a; margin-bottom: 3px;
}
.hero-student { font-size: 1.0rem; color: #d8eeff; margin-bottom: 2px; }
.hero-course  { font-size: 0.84rem; color: #a8cce0; font-style: italic; }

/* ── Divisor ── */
.divider-gold {
    border: none; height: 2px;
    background: linear-gradient(90deg, transparent, #d4aa50, #c8a84b, transparent);
    margin: 14px auto 28px; width: 60%;
}

/* ── KPI cards ── */
.kpi-card {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(200,168,75,0.35);
    border-radius: 12px; padding: 20px 14px;
    text-align: center; backdrop-filter: blur(8px);
    margin-bottom: 12px;
}
.kpi-value {
    font-family: 'Playfair Display', serif;
    font-size: 1.9rem; font-weight: 700; color: #f0c84a; line-height: 1;
}
.kpi-label {
    font-size: 0.72rem; color: #cce0f2;
    text-transform: uppercase; letter-spacing: 1.4px; margin-top: 6px;
}

/* ── Secciones ── */
.section-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem; color: #ffe98a;
    border-left: 4px solid #d4aa50;
    padding-left: 14px; margin: 28px 0 14px;
}
.insight-box {
    background: rgba(200,168,60,0.12);
    border: 1px solid rgba(200,168,60,0.3);
    border-left: 4px solid #d4aa50;
    border-radius: 8px; padding: 16px 20px;
    margin: 14px 0; font-size: 0.97rem;
    line-height: 1.78; color: #f0f8ff;
}
.conclusion-box {
    background: linear-gradient(135deg, rgba(16,52,100,0.6), rgba(8,24,55,0.8));
    border: 1px solid rgba(200,168,80,0.4);
    border-radius: 14px; padding: 26px 30px;
    margin: 18px 0; line-height: 1.88;
    font-size: 1.0rem; color: #f0f8ff;
}
.note-box {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(160,200,230,0.3);
    border-radius: 8px; padding: 12px 16px;
    font-size: 0.85rem; color: #cce0f0;
    font-style: italic; margin-top: 10px;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px; background: rgba(255,255,255,0.06);
    border-radius: 10px; padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px; padding: 8px 22px;
    color: #cce0f4 !important;
    font-family: 'Source Sans 3', sans-serif; font-size: 0.9rem;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1a3a60, #1e4878) !important;
    color: #f0c84a !important;
    border-bottom: 2px solid #d4aa50 !important;
}

/* ── Alerts / success ── */
.stAlert, .stSuccess, .stWarning { border-radius: 10px; }
.stAlert p, .stSuccess p { color: #ffffff !important; }

/* ── Botón de descarga ── */
.stDownloadButton button {
    background: linear-gradient(135deg, #1a3a60, #1e4878) !important;
    color: #f0c84a !important;
    border: 1px solid rgba(200,168,75,0.5) !important;
    font-family: 'Source Sans 3', sans-serif !important;
    font-size: 1rem !important;
    padding: 12px 24px !important;
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SVG DEL BARCO — codificado en base64
# (Streamlit bloquea SVG inline; <img data-uri> sí funciona)
# ─────────────────────────────────────────────
_SHIP_SVG_RAW = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 210" width="420" height="158">
  <defs>
    <linearGradient id="hullG" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1e3a5a"/><stop offset="100%" stop-color="#0d1e30"/>
    </linearGradient>
    <linearGradient id="superG" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#2e5278"/><stop offset="100%" stop-color="#1a3050"/>
    </linearGradient>
    <linearGradient id="fnlG" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#e8c060"/><stop offset="82%" stop-color="#a07828"/>
      <stop offset="100%" stop-color="#1a1a1a"/>
    </linearGradient>
    <linearGradient id="skyG" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#081830" stop-opacity="0"/>
      <stop offset="100%" stop-color="#0a2040" stop-opacity="0.5"/>
    </linearGradient>
  </defs>
  <!-- Cielo de fondo -->
  <rect x="0" y="0" width="560" height="160" fill="url(#skyG)" rx="8"/>
  <!-- Estrellas -->
  <g fill="#ffffff" opacity="0.5">
    <circle cx="30" cy="20" r="1"/><circle cx="80" cy="10" r="1"/>
    <circle cx="130" cy="25" r="1.2"/><circle cx="500" cy="15" r="1"/>
    <circle cx="540" cy="30" r="0.8"/><circle cx="460" cy="8" r="1.2"/>
    <circle cx="380" cy="18" r="0.9"/><circle cx="310" cy="6" r="1"/>
  </g>
  <!-- Agua -->
  <ellipse cx="280" cy="186" rx="260" ry="20" fill="#1a4a7a" opacity="0.55"/>
  <path d="M20,182 Q90,176 160,182 Q230,188 300,182 Q370,176 440,182 Q500,188 540,182"
        stroke="#4a8ab8" stroke-width="1.5" fill="none" opacity="0.6"/>
  <path d="M40,190 Q110,185 180,190 Q250,195 320,190 Q390,185 460,190"
        stroke="#3a7aaa" stroke-width="1" fill="none" opacity="0.35"/>
  <!-- Reflejo dorado agua -->
  <ellipse cx="280" cy="184" rx="120" ry="5" fill="#d4aa50" opacity="0.07"/>
  <!-- Casco -->
  <path d="M50,162 L75,126 L475,126 L505,162 Q480,178 280,179 Q100,178 50,162 Z"
        fill="url(#hullG)" stroke="#2a5a8a" stroke-width="1.2"/>
  <!-- Línea de flotación dorada -->
  <path d="M58,164 L498,164" stroke="#d4aa50" stroke-width="2" opacity="0.75"/>
  <!-- Banda blanca ornamental -->
  <path d="M68,138 L480,138 L482,145 L66,145 Z" fill="#e8f4ff" opacity="0.1"/>
  <!-- Superestructura -->
  <rect x="90" y="90" width="368" height="38" rx="4" fill="url(#superG)" stroke="#3a6898" stroke-width="1"/>
  <!-- Cubierta superior -->
  <rect x="112" y="70" width="318" height="22" rx="3" fill="#1e3858" stroke="#2a5888" stroke-width="0.8"/>
  <!-- Puente de mando -->
  <rect x="185" y="55" width="130" height="17" rx="3" fill="#162c48" stroke="#2a5080" stroke-width="0.8"/>
  <!-- Alas del puente -->
  <rect x="175" y="60" width="15" height="12" rx="2" fill="#1a3450" stroke="#2a5080" stroke-width="0.6"/>
  <rect x="310" y="60" width="15" height="12" rx="2" fill="#1a3450" stroke="#2a5080" stroke-width="0.6"/>
  <!-- Ventanas superestructura -->
  <g fill="#80c0f0" opacity="0.65">
    <rect x="102" y="97" width="10" height="7" rx="1.5"/>
    <rect x="118" y="97" width="10" height="7" rx="1.5"/>
    <rect x="134" y="97" width="10" height="7" rx="1.5"/>
    <rect x="395" y="97" width="10" height="7" rx="1.5"/>
    <rect x="411" y="97" width="10" height="7" rx="1.5"/>
    <rect x="427" y="97" width="10" height="7" rx="1.5"/>
    <rect x="443" y="97" width="10" height="7" rx="1.5"/>
  </g>
  <!-- Ventanas cubierta -->
  <g fill="#a0d4f8" opacity="0.55">
    <rect x="124" y="74" width="8" height="6" rx="1"/>
    <rect x="138" y="74" width="8" height="6" rx="1"/>
    <rect x="152" y="74" width="8" height="6" rx="1"/>
    <rect x="360" y="74" width="8" height="6" rx="1"/>
    <rect x="374" y="74" width="8" height="6" rx="1"/>
    <rect x="388" y="74" width="8" height="6" rx="1"/>
    <rect x="402" y="74" width="8" height="6" rx="1"/>
  </g>
  <!-- Ojos de buey puente -->
  <g fill="#c0e4ff" opacity="0.6">
    <circle cx="200" cy="63" r="4"/><circle cx="220" cy="63" r="4"/>
    <circle cx="240" cy="63" r="4"/><circle cx="260" cy="63" r="4"/>
    <circle cx="280" cy="63" r="4"/>
  </g>
  <!-- 4 Chimeneas -->
  <rect x="190" y="24" width="26" height="48" rx="4" fill="url(#fnlG)" stroke="#906020" stroke-width="0.9"/>
  <rect x="190" y="48" width="26" height="5" fill="#0a0a0a" opacity="0.9"/>
  <rect x="232" y="26" width="26" height="46" rx="4" fill="url(#fnlG)" stroke="#906020" stroke-width="0.9"/>
  <rect x="232" y="48" width="26" height="5" fill="#0a0a0a" opacity="0.9"/>
  <rect x="274" y="26" width="26" height="46" rx="4" fill="url(#fnlG)" stroke="#906020" stroke-width="0.9"/>
  <rect x="274" y="48" width="26" height="5" fill="#0a0a0a" opacity="0.9"/>
  <rect x="316" y="28" width="26" height="44" rx="4" fill="url(#fnlG)" stroke="#906020" stroke-width="0.9"/>
  <rect x="316" y="48" width="26" height="5" fill="#0a0a0a" opacity="0.8"/>
  <!-- Humo chimeneas 1-3 -->
  <g opacity="0.4">
    <ellipse cx="203" cy="17" rx="9" ry="6" fill="#b0c4d8"/>
    <ellipse cx="197" cy="9"  rx="6" ry="5" fill="#a0b4c8"/>
    <ellipse cx="191" cy="3"  rx="4" ry="3" fill="#90a4b8"/>
    <ellipse cx="245" cy="18" rx="9" ry="6" fill="#b0c4d8"/>
    <ellipse cx="240" cy="10" rx="6" ry="5" fill="#a0b4c8"/>
    <ellipse cx="287" cy="18" rx="8" ry="6" fill="#b0c4d8"/>
    <ellipse cx="282" cy="11" rx="5" ry="4" fill="#a0b4c8"/>
  </g>
  <!-- Palo de proa -->
  <line x1="80" y1="70" x2="80" y2="6" stroke="#6090b8" stroke-width="2"/>
  <line x1="80" y1="10" x2="165" y2="68" stroke="#5080a0" stroke-width="1" opacity="0.7"/>
  <line x1="80" y1="10" x2="40"  y2="55" stroke="#5080a0" stroke-width="0.8" opacity="0.5"/>
  <!-- Palo de popa -->
  <line x1="490" y1="88" x2="490" y2="30" stroke="#6090b8" stroke-width="2"/>
  <!-- Cables -->
  <line x1="80"  y1="10" x2="200" y2="52" stroke="#406080" stroke-width="0.7" opacity="0.5"/>
  <line x1="490" y1="32" x2="330" y2="52" stroke="#406080" stroke-width="0.7" opacity="0.5"/>
  <!-- Ancla popa -->
  <text x="470" y="155" font-size="16" fill="#d4aa50" opacity="0.85" font-family="serif">⚓</text>
  <!-- Escotillas cubierta -->
  <g fill="#2a5080" stroke="#3a6898" stroke-width="0.5">
    <rect x="155" y="127" width="20" height="8" rx="1"/>
    <rect x="195" y="127" width="20" height="8" rx="1"/>
    <rect x="390" y="127" width="20" height="8" rx="1"/>
    <rect x="430" y="127" width="20" height="8" rx="1"/>
  </g>
</svg>"""

_SHIP_B64 = base64.b64encode(_SHIP_SVG_RAW.encode("utf-8")).decode("utf-8")
SHIP_IMG_TAG = f'<img src="data:image/svg+xml;base64,{_SHIP_B64}" width="420" height="158" alt="RMS Titanic" style="display:block;">'

# ─────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────
PORTS = {
    "S": {"name": "Southampton",       "country": "Inglaterra",     "lat": 50.9097, "lon": -1.4044},
    "C": {"name": "Cherbourg",         "country": "Francia",        "lat": 49.6337, "lon": -1.6221},
    "Q": {"name": "Queenstown / Cobh", "country": "Irlanda",        "lat": 51.8503, "lon": -8.2943},
    "NY": {"name": "New York",         "country": "Estados Unidos", "lat": 40.7128, "lon": -74.0060}
}
CLASS_LABELS    = {1: "Primera clase", 2: "Segunda clase", 3: "Tercera clase"}
SURVIVAL_LABELS = {0: "No sobrevivió", 1: "Sobrevivió"}

TITANIC_REAL = {
    "Primera clase":  {"pasajeros_reales": 329, "capacidad_max": 735},
    "Segunda clase":  {"pasajeros_reales": 285, "capacidad_max": 674},
    "Tercera clase":  {"pasajeros_reales": 710, "capacidad_max": 1026},
    "Tripulación":    {"pasajeros_reales": 899, "capacidad_max": 900},
}
TOTAL_REAL_PASAJEROS = 1_317
TOTAL_REAL_ABORDO    = 2_224

COLORS = {
    "Primera clase": "#d4aa50",
    "Segunda clase": "#5b9bd5",
    "Tercera clase": "#e07a5f",
}

# ─────────────────────────────────────────────
# CARGA Y LIMPIEZA
# ─────────────────────────────────────────────
@st.cache_data
def load_data(uploaded_file=None):
    source = uploaded_file if uploaded_file is not None else "train.xlsx"
    raw = pd.read_excel(source, header=None)
    possible_header = raw.iloc[1].astype(str).tolist()
    if "PassengerId" in possible_header and "Survived" in possible_header:
        df = raw.iloc[2:].copy()
        df.columns = possible_header
    else:
        df = pd.read_excel(source)
    df.columns = [str(c).strip() for c in df.columns]
    for col in ["PassengerId","Survived","Pclass","Age","SibSp","Parch","Fare"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    if "Embarked" in df.columns:
        df["Embarked"] = df["Embarked"].astype("string").str.strip().str.upper()
        df["Embarked"] = df["Embarked"].replace({"": pd.NA, "NAN": pd.NA})
        df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode(dropna=True).iloc[0])
    if "Sex" in df.columns:
        df["Sex"] = df["Sex"].astype("string").str.strip().str.lower()
    if "Age" in df.columns:
        df["Age_missing"] = df["Age"].isna()
        df["Age"] = df["Age"].fillna(df["Age"].median())
    if "Fare" in df.columns:
        df["Fare"] = df["Fare"].fillna(df["Fare"].median())
    df["Clase"]         = df["Pclass"].map(CLASS_LABELS)
    df["Supervivencia"] = df["Survived"].map(SURVIVAL_LABELS)
    df["Puerto"]        = df["Embarked"].map(lambda x: f"{x} - {PORTS.get(x, {}).get('name', 'Desconocido')}")
    df["Sexo"]          = df["Sex"].map({"male": "Hombre", "female": "Mujer"}).fillna(df["Sex"])
    df["Grupo edad"]    = pd.cut(
        df["Age"],
        bins=[-1, 12, 18, 35, 60, 120],
        labels=["Niñez (0-12)", "Adolescencia (13-18)", "Adulto joven (19-35)", "Adulto (36-60)", "Mayor (60+)"]
    )
    return df

def survival_rate_table(df, group_cols):
    return df.groupby(group_cols, dropna=False).agg(
        Pasajeros=("PassengerId", "count"),
        Sobrevivientes=("Survived", "sum"),
        Tarifa_total=("Fare", "sum"),
        Tarifa_promedio=("Fare", "mean"),
        Edad_promedio=("Age", "mean")
    ).reset_index().assign(
        **{"Probabilidad supervivencia": lambda x: x["Sobrevivientes"] / x["Pasajeros"]}
    )

def fmt_pct(s): return (s * 100).round(1).astype(str) + "%"

def plotly_theme():
    return dict(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e0ecf8", family="Source Sans 3"),
        title_font=dict(family="Playfair Display", color="#f0dc9c"),
        legend=dict(bgcolor="rgba(0,0,0,0.3)", bordercolor="rgba(200,168,75,0.3)", borderwidth=1),
        colorway=list(COLORS.values()),
    )

# ─────────────────────────────────────────────
# ENCABEZADO — portada con barco + datos universitarios
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="hero-wrap">
  <div class="hero-ship">{SHIP_IMG_TAG}</div>
  <div class="hero-text">
    <div class="hero-rms">R &nbsp;·&nbsp; M &nbsp;·&nbsp; S</div>
    <div class="hero-title">Titanic</div>
    <div class="hero-subtitle">
      Análisis de Supervivencia &nbsp;·&nbsp; Estructura de Clase &nbsp;·&nbsp; Rentabilidad del Viaje
    </div>
    <hr class="hero-gold-line">
    <div class="hero-uni-tag">Trabajo · Entrega Final</div>
    <div class="hero-uni-name">Politécnico Gran Colombiano</div>
    <div class="hero-student">👩‍🎓 &nbsp;Sara Santillana</div>
    <div class="hero-course">Análisis y Visualización de Datos</div>
  </div>
</div>
<hr class="divider-gold">
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚓ Panel de Control")
    st.markdown("---")
    uploaded = st.file_uploader("Cargar base Titanic (.xlsx)", type=["xlsx","xls"])
    st.markdown("---")
    st.markdown("### 💰 Parámetros Financieros (£)")
    op_cost_gbp = st.number_input(
        "Costo operativo estimado del viaje (£)",
        min_value=0.0, value=27_000.0, step=500.0,
        help="Costo estimado de operar el Titanic en el viaje Southampton → New York, en libras esterlinas de 1912."
    )
    inflation_factor = st.number_input(
        "Factor de inflación histórico (£1912 → £2025)",
        min_value=1.0, value=128.0, step=1.0,
        help="Según el Banco de Inglaterra, £1 en 1912 equivale a aprox. £128 en 2025. Ajusta si usas otra fuente."
    )
    st.markdown("---")
    st.markdown(
        '<div class="note-box">⚠️ El factor de inflación es una estimación histórica. '
        'El Banco de Inglaterra y MeasuringWorth sugieren un rango de £100 – £135 por £1 de 1912.</div>',
        unsafe_allow_html=True
    )
    st.markdown("---")
    st.markdown("### 📚 Fuentes")
    st.markdown("""
    - [Kaggle – Titanic Dataset](https://www.kaggle.com/c/titanic/data)  
    - [National Archives UK](https://www.nationalarchives.gov.uk/education/resources/life-aboard-titanic/)  
    - [Bank of England Inflation](https://www.bankofengland.co.uk/monetary-policy/inflation/inflation-calculator)  
    - [Encyclopedia Titanica](https://www.encyclopedia-titanica.org)  
    """)

df = load_data(uploaded)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tabs = st.tabs([
    "🔍 Verificación de Datos",
    "📊 Análisis Visual",
    "🗺️ Ruta del Titanic",
    "💷 Conclusión & Rentabilidad"
])

# ══════════════════════════════════════════════
# TAB 1 — VERIFICACIÓN
# ══════════════════════════════════════════════
with tabs[0]:
    st.markdown('<p class="section-header">Módulo 1 · Verificación y Calidad de Datos</p>', unsafe_allow_html=True)
    st.markdown(
        "Antes de extraer conclusiones, es fundamental confirmar que los datos sean consistentes, "
        "completos y representativos del fenómeno que se estudia."
    )

    # ── Métricas KPI ──
    total_p  = len(df)
    surv_pct = df["Survived"].mean() * 100
    fare_tot = df["Fare"].sum()
    age_med  = df["Age"].median()
    null_age = int(df["Age_missing"].sum()) if "Age_missing" in df.columns else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    for col, val, label in [
        (c1, f"{total_p:,}",          "Pasajeros en el dataset"),
        (c2, f"{surv_pct:.1f}%",      "Tasa de supervivencia"),
        (c3, f"£ {fare_tot:,.0f}",    "Total tarifas recaudadas"),
        (c4, f"{age_med:.1f} años",   "Edad mediana"),
        (c5, f"{null_age}",           "Edades imputadas (mediana)"),
    ]:
        col.markdown(
            f'<div class="kpi-card"><div class="kpi-value">{val}</div>'
            f'<div class="kpi-label">{label}</div></div>',
            unsafe_allow_html=True
        )

    st.markdown('<p class="section-header">Validación de campos requeridos</p>', unsafe_allow_html=True)
    required = ["PassengerId","Survived","Pclass","Name","Sex","Age","Fare","Embarked"]
    validation = pd.DataFrame({
        "Campo":           required,
        "Existe":          ["✅" if c in df.columns else "❌" for c in required],
        "Valores nulos":   [int(df[c].isna().sum()) if c in df.columns else "N/A" for c in required],
        "Tipo detectado":  [str(df[c].dtype) if c in df.columns else "—" for c in required],
    })
    st.dataframe(validation, use_container_width=True, hide_index=True)

    # ── Verificación de Ocupación Real ──
    st.markdown('<p class="section-header">Verificación de Ocupación Real vs. Dataset</p>', unsafe_allow_html=True)

    st.markdown(
        '<div class="insight-box">'
        '📌 <strong>Contexto metodológico:</strong> El conjunto de datos de Kaggle contiene <strong>891 registros</strong>, '
        'correspondientes únicamente al conjunto de entrenamiento del dataset público. Sin embargo, el Titanic embarcó '
        'aproximadamente <strong>1.317 pasajeros</strong> y <strong>899 tripulantes</strong>, para un total de '
        '<strong>2.224 personas a bordo</strong>. El dataset cubre el <strong>67,7% de los pasajeros</strong> reales, '
        'lo que permite análisis estadístico válido, aunque con la limitación de no representar el 100% del viaje.'
        '</div>',
        unsafe_allow_html=True
    )

    dataset_por_clase = df.groupby(["Clase","Pclass"]).size().reset_index(name="En dataset").sort_values("Pclass")
    real_data = pd.DataFrame([
        {"Clase": "Primera clase", "Pasajeros reales": 329, "Capacidad máx.": 735},
        {"Clase": "Segunda clase", "Pasajeros reales": 285, "Capacidad máx.": 674},
        {"Clase": "Tercera clase", "Pasajeros reales": 710, "Capacidad máx.": 1026},
    ])
    occ_df = dataset_por_clase[["Clase","En dataset"]].merge(real_data, on="Clase")
    occ_df["Cobertura dataset"] = (occ_df["En dataset"] / occ_df["Pasajeros reales"] * 100).round(1).astype(str) + "%"
    occ_df["Ocupación real"] = (occ_df["Pasajeros reales"] / occ_df["Capacidad máx."] * 100).round(1).astype(str) + "%"
    st.dataframe(occ_df, use_container_width=True, hide_index=True)

    st.markdown(
        f'<div class="note-box">Total real a bordo: <strong>2.224 personas</strong> '
        f'(1.317 pasajeros + 899 tripulantes). '
        f'El dataset de Kaggle captura <strong>{(891/1317*100):.1f}%</strong> de los pasajeros. '
        f'Fuente: Encyclopedia Titanica / National Archives UK.</div>',
        unsafe_allow_html=True
    )

    problems = []
    if not all(c in df.columns for c in required): problems.append("Faltan columnas requeridas.")
    if df["Survived"].dropna().isin([0,1]).mean() < 1: problems.append("La variable Survived tiene valores inesperados.")
    if df["Pclass"].dropna().isin([1,2,3]).mean() < 1: problems.append("La variable Pclass tiene valores fuera de 1, 2, 3.")
    if df["Embarked"].dropna().isin(["S","C","Q"]).mean() < 1: problems.append("La variable Embarked tiene puertos inesperados.")
    if problems:
        for p in problems: st.warning(p)
    else:
        st.success(
            "Base de datos validada ✓ — Estructura consistente. Se procede al análisis exploratorio "
            "de la relación entre clase, tarifa y probabilidad de supervivencia."
        )

    st.markdown('<p class="section-header">Vista previa de datos (primeros 25 registros)</p>', unsafe_allow_html=True)
    st.dataframe(df.head(25), use_container_width=True)

# ══════════════════════════════════════════════
# TAB 2 — ANÁLISIS VISUAL
# ══════════════════════════════════════════════
with tabs[1]:
    st.markdown('<p class="section-header">Módulo 2 · Análisis Visual de Supervivencia</p>', unsafe_allow_html=True)

    # Supervivencia por clase
    class_rate = survival_rate_table(df, ["Clase","Pclass"]).sort_values("Pclass")
    fig1 = px.bar(
        class_rate, x="Clase", y="Probabilidad supervivencia",
        text=fmt_pct(class_rate["Probabilidad supervivencia"]),
        hover_data=["Pasajeros","Sobrevivientes","Tarifa_promedio"],
        color="Clase", color_discrete_map=COLORS,
        title="Probabilidad de supervivencia por clase"
    )
    fig1.update_traces(textfont_size=14, textposition="outside", marker_line_width=0, opacity=0.9)
    fig1.update_layout(yaxis_tickformat=".0%", yaxis_title="Probabilidad", xaxis_title="",
                       showlegend=False, **plotly_theme())
    st.plotly_chart(fig1, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        sex_class = survival_rate_table(df, ["Clase","Pclass","Sexo"]).sort_values(["Pclass","Sexo"])
        fig2 = px.bar(sex_class, x="Clase", y="Probabilidad supervivencia", color="Sexo", barmode="group",
                      text=fmt_pct(sex_class["Probabilidad supervivencia"]),
                      color_discrete_map={"Hombre":"#5b9bd5","Mujer":"#e07a8f"},
                      title="Supervivencia por sexo y clase")
        fig2.update_layout(yaxis_tickformat=".0%", yaxis_title="", xaxis_title="", **plotly_theme())
        st.plotly_chart(fig2, use_container_width=True)
    with col2:
        age_class = survival_rate_table(df, ["Clase","Pclass","Grupo edad"]).sort_values(["Pclass","Grupo edad"])
        fig3 = px.bar(age_class, x="Grupo edad", y="Probabilidad supervivencia", color="Clase", barmode="group",
                      text=fmt_pct(age_class["Probabilidad supervivencia"]),
                      color_discrete_map=COLORS,
                      title="Supervivencia por grupo de edad y clase")
        fig3.update_layout(yaxis_tickformat=".0%", yaxis_title="", xaxis_title="", **plotly_theme())
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<p class="section-header">Pasajeros por puerto de embarque</p>', unsafe_allow_html=True)
    port_class = df.groupby(["Puerto","Clase","Pclass"]).size().reset_index(name="Pasajeros").sort_values(["Puerto","Pclass"])
    fig4 = px.bar(port_class, x="Puerto", y="Pasajeros", color="Clase", barmode="group",
                  color_discrete_map=COLORS, title="Pasajeros por puerto de embarque y clase")
    fig4.update_layout(xaxis_title="", yaxis_title="Pasajeros", **plotly_theme())
    st.plotly_chart(fig4, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        port_s = survival_rate_table(df, ["Puerto"])
        fig5 = px.bar(port_s, x="Puerto", y="Probabilidad supervivencia",
                      text=fmt_pct(port_s["Probabilidad supervivencia"]),
                      color="Puerto", title="Supervivencia por puerto de embarque")
        fig5.update_layout(yaxis_tickformat=".0%", yaxis_title="", xaxis_title="",
                           showlegend=False, **plotly_theme())
        st.plotly_chart(fig5, use_container_width=True)
    with col4:
        fig6 = px.box(df, x="Clase", y="Fare", points="outliers",
                      color="Clase", color_discrete_map=COLORS,
                      title="Distribución de tarifas por clase (£)")
        fig6.update_layout(xaxis_title="", yaxis_title="Tarifa (£)",
                           showlegend=False, **plotly_theme())
        st.plotly_chart(fig6, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 3 — RUTA
# ══════════════════════════════════════════════
with tabs[2]:
    st.markdown('<p class="section-header">Ruta del RMS Titanic — Abril de 1912</p>', unsafe_allow_html=True)
    route = ["S","C","Q","NY"]
    route_df = pd.DataFrame([{
        "Puerto": PORTS[k]["name"], "Código": k, "País": PORTS[k]["country"],
        "lat": PORTS[k]["lat"], "lon": PORTS[k]["lon"], "Orden": i+1
    } for i, k in enumerate(route)])

    fig_r = go.Figure()
    fig_r.add_trace(go.Scattergeo(
        lon=route_df["lon"], lat=route_df["lat"],
        mode="lines+markers+text",
        text=route_df["Puerto"], textposition="top center",
        textfont=dict(size=13, color="#d4aa50", family="Playfair Display"),
        marker=dict(size=12, color="#d4aa50", symbol="circle",
                    line=dict(width=2, color="#f0e6c8")),
        line=dict(width=3, color="#5b9bd5"),
        hovertext=route_df["Código"]+" — "+route_df["Puerto"]+", "+route_df["País"],
        hoverinfo="text"
    ))
    fig_r.update_geos(
        projection_type="natural earth",
        showcountries=True, showland=True, showocean=True,
        landcolor="#1a2e42", oceancolor="#0a1628",
        countrycolor="rgba(180,150,80,0.3)",
        fitbounds="locations",
        bgcolor="rgba(0,0,0,0)"
    )
    fig_r.update_layout(
        title=dict(text="Southampton → Cherbourg → Queenstown / Cobh → New York",
                   font=dict(family="Playfair Display", size=16, color="#e8d5a0")),
        height=600, margin=dict(l=0, r=0, t=60, b=0),
        **plotly_theme()
    )
    st.plotly_chart(fig_r, use_container_width=True)

    st.markdown(
        '<div class="insight-box">'
        '🗓️ <strong>10 de abril de 1912</strong>: El Titanic zarpó de Southampton hacia Nueva York, '
        'con escalas en Cherbourg (Francia) e Queenstown (Irlanda). '
        'En la madrugada del <strong>15 de abril de 1912</strong>, el buque colisionó con un iceberg '
        'y se hundió en el Atlántico Norte, a aproximadamente 600 km al sur de Terranova.'
        '</div>',
        unsafe_allow_html=True
    )

# ══════════════════════════════════════════════
# TAB 4 — CONCLUSIÓN & RENTABILIDAD EN £
# ══════════════════════════════════════════════
with tabs[3]:
    st.markdown('<p class="section-header">Módulo 3 · Conclusión · Rentabilidad del Viaje (£ Históricas y £ 2025)</p>', unsafe_allow_html=True)

    # ── Cálculo financiero por clase ──
    fare_cls = (
        df.groupby(["Clase","Pclass"])
          .agg(Tarifa_total_gbp=("Fare","sum"), Pasajeros=("PassengerId","count"))
          .reset_index()
          .sort_values("Pclass")
    )
    total_recaudado_gbp  = fare_cls["Tarifa_total_gbp"].sum()
    ganancia_gbp         = total_recaudado_gbp - op_cost_gbp
    total_recaudado_2025 = total_recaudado_gbp * inflation_factor
    op_cost_2025         = op_cost_gbp         * inflation_factor
    ganancia_2025        = ganancia_gbp         * inflation_factor

    fare_cls["% del total recaudado"] = (fare_cls["Tarifa_total_gbp"] / total_recaudado_gbp * 100).round(1)
    fare_cls["Cobertura del costo op."] = (fare_cls["Tarifa_total_gbp"] / op_cost_gbp * 100).round(1)
    fare_cls["Equiv. £ 2025"] = (fare_cls["Tarifa_total_gbp"] * inflation_factor).round(0).astype(int)

    # ── KPIs Financieros ──
    k1, k2, k3 = st.columns(3)
    k1.markdown(
        f'<div class="kpi-card"><div class="kpi-value">£ {total_recaudado_gbp:,.0f}</div>'
        f'<div class="kpi-label">Total recaudado (£ 1912)</div></div>', unsafe_allow_html=True
    )
    k2.markdown(
        f'<div class="kpi-card"><div class="kpi-value">£ {op_cost_gbp:,.0f}</div>'
        f'<div class="kpi-label">Costo operativo estimado (£ 1912)</div></div>', unsafe_allow_html=True
    )
    color_g = "#5dde8b" if ganancia_gbp >= 0 else "#e05555"
    signo   = "+" if ganancia_gbp >= 0 else ""
    k3.markdown(
        f'<div class="kpi-card"><div class="kpi-value" style="color:{color_g}">'
        f'{signo}£ {ganancia_gbp:,.0f}</div>'
        f'<div class="kpi-label">Ganancia / Pérdida estimada (£ 1912)</div></div>', unsafe_allow_html=True
    )

    k4, k5, k6 = st.columns(3)
    k4.markdown(
        f'<div class="kpi-card"><div class="kpi-value">£ {total_recaudado_2025:,.0f}</div>'
        f'<div class="kpi-label">Total recaudado equiv. (£ 2025)</div></div>', unsafe_allow_html=True
    )
    k5.markdown(
        f'<div class="kpi-card"><div class="kpi-value">£ {op_cost_2025:,.0f}</div>'
        f'<div class="kpi-label">Costo op. equiv. (£ 2025)</div></div>', unsafe_allow_html=True
    )
    k6.markdown(
        f'<div class="kpi-card"><div class="kpi-value" style="color:{color_g}">'
        f'{signo}£ {ganancia_2025:,.0f}</div>'
        f'<div class="kpi-label">Ganancia equiv. (£ 2025)</div></div>', unsafe_allow_html=True
    )

    # ── Tabla por clase ──
    st.markdown('<p class="section-header">Aporte de cada clase a la operación</p>', unsafe_allow_html=True)
    st.dataframe(
        fare_cls[["Clase","Pasajeros","Tarifa_total_gbp","% del total recaudado",
                   "Cobertura del costo op.","Equiv. £ 2025"]]
        .rename(columns={
            "Tarifa_total_gbp": "Tarifa total (£ 1912)",
            "% del total recaudado": "% del total (%)",
            "Cobertura del costo op.": "Cobertura costo op. (%)",
        }),
        use_container_width=True, hide_index=True
    )

    # ── Gráficos ──
    col_a, col_b = st.columns(2)
    with col_a:
        fig_pie = px.pie(
            fare_cls, names="Clase", values="Tarifa_total_gbp",
            color="Clase", color_discrete_map=COLORS,
            title="Participación por clase en ingresos totales (£ 1912)"
        )
        fig_pie.update_traces(textinfo="percent+label", textfont_size=13,
                               marker=dict(line=dict(color="#0a1628", width=2)))
        fig_pie.update_layout(**plotly_theme())
        st.plotly_chart(fig_pie, use_container_width=True)
    with col_b:
        fig_cov = px.bar(
            fare_cls, x="Clase", y="Cobertura del costo op.",
            color="Clase", color_discrete_map=COLORS,
            text=fare_cls["Cobertura del costo op."].astype(str) + "%",
            title="Cobertura del costo operativo por clase (%)"
        )
        fig_cov.add_hline(y=100, line_dash="dot", line_color="#d4aa50",
                          annotation_text="100% — costo cubierto",
                          annotation_font_color="#d4aa50")
        fig_cov.update_layout(yaxis_title="% de cobertura", xaxis_title="",
                               showlegend=False, **plotly_theme())
        st.plotly_chart(fig_cov, use_container_width=True)

    # ── Conclusión narrativa ──
    st.markdown('<p class="section-header">Interpretación del análisis</p>', unsafe_allow_html=True)

    class_rate   = survival_rate_table(df, ["Clase","Pclass"]).sort_values("Pclass")
    best  = class_rate.loc[class_rate["Probabilidad supervivencia"].idxmax()]
    worst = class_rate.loc[class_rate["Probabilidad supervivencia"].idxmin()]
    top_c = fare_cls.loc[fare_cls["Tarifa_total_gbp"].idxmax()]

    st.markdown(f"""
    <div class="conclusion-box">
    <strong style="font-family:'Playfair Display',serif; font-size:1.15rem; color:#d4aa50;">
    Supervivencia y clase social</strong><br><br>
    El análisis evidencia una correlación directa entre la clase del pasajero y su probabilidad de supervivencia.
    Los pasajeros de <strong>{best['Clase']}</strong> presentaron la mayor probabilidad de sobrevivir
    (<strong>{best['Probabilidad supervivencia']*100:.1f}%</strong>), mientras que los de
    <strong>{worst['Clase']}</strong> registraron la menor (<strong>{worst['Probabilidad supervivencia']*100:.1f}%</strong>).
    Esta diferencia es estadísticamente significativa aunque no puede atribuirse exclusivamente al factor económico:
    también incidieron la ubicación física dentro del buque, los protocolos de evacuación y la composición
    sociodemográfica de cada clase.
    <br><br>
    <strong style="font-family:'Playfair Display',serif; font-size:1.15rem; color:#d4aa50;">
    Rentabilidad de la operación</strong><br><br>
    Del total de <strong>£ {total_recaudado_gbp:,.0f}</strong> recaudados en tarifas —según el dataset disponible—,
    la clase que mayor aporte realizó fue <strong>{top_c['Clase']}</strong>, con
    <strong>£ {top_c['Tarifa_total_gbp']:,.0f}</strong> ({top_c['% del total recaudado']:.1f}% del total).
    Frente a un costo operativo estimado de <strong>£ {op_cost_gbp:,.0f}</strong>, el viaje habría generado
    una {'ganancia' if ganancia_gbp >= 0 else 'pérdida'} de
    <strong>£ {abs(ganancia_gbp):,.0f}</strong> en valores de 1912.
    <br><br>
    Ajustado a valores actuales con un factor de inflación de <strong>×{inflation_factor:.0f}</strong>
    (Banco de Inglaterra), esto equivaldría a una {'ganancia' if ganancia_gbp >= 0 else 'pérdida'} de
    <strong style="color:{'#5dde8b' if ganancia_gbp >= 0 else '#e05555'};">
    £ {abs(ganancia_2025):,.0f} (£ 2025)</strong>.
    <br><br>
    <em style="color:#8ba8c4; font-size:0.9rem;">
    ⚠️ Nota: el dataset cubre 891 de los 1.317 pasajeros reales (67,7%), por lo que los ingresos totales
    reales habrían sido mayores. El análisis financiero debe interpretarse como una estimación proporcional
    y no como cifra contable exacta.
    </em>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
    <strong>📌 Reflexión :</strong><br>
    
    "El presente análisis busca ir más allá de una simple descripción de la distribución de los pasajeros a bordo del Titanic en 1912, con el propósito de comprender cómo el mercado de transporte marítimo transatlántico estaba estructurado estratégicamente en clases y así identificar qué segmento generaba un mayor retorno económico. Los resultados evidencian que la primera clase no solo aportaba el mayor ingreso por pasajero —con tarifas significativamente superiores a las de segunda y tercera clase—, sino que también constituía un segmento clave para que la White Star Line pudiera financiar, justificar y rentabilizar la operación de buques de gran escala. En este sentido, analizar la composición de ingresos del Titanic permite establecer un paralelismo con las operaciones actuales de transporte internacional, donde resulta fundamental comprender quién paga y cuánto para determinar la sostenibilidad del modelo de negocio. Adicionalmente, el análisis de los datos permitió identificar una relación directa entre el acceso a una clase superior y una mayor probabilidad de supervivencia, según la información contenida en la base de datos proporcionada. Finalmente, el uso de herramientas de inteligencia artificial facilitó la obtención de información complementaria, como el costo estimado de operación del buque en la época y la ruta planificada, enriqueciendo el contexto y fortaleciendo la interpretación de los resultados."
    )
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="section-header">Fuentes y referencias</p>', unsafe_allow_html=True)
    st.markdown("""
    | Fuente | Descripción | Enlace |
    |--------|-------------|--------|

    | Encyclopedia Titanica | Información histórica detallada por pasajero | [encyclopedia-titanica.org](https://www.encyclopedia-titanica.org) |
    | National Archives UK | Vida a bordo del Titanic | [nationalarchives.gov.uk](https://www.nationalarchives.gov.uk/education/resources/life-aboard-titanic/) |
    | Bank of England | Calculadora de inflación histórica | [bankofengland.co.uk](https://www.bankofengland.co.uk/monetary-policy/inflation/inflation-calculator) |
    | MeasuringWorth | Tasas históricas de cambio | [measuringworth.com](https://www.measuringworth.com/datasets/exchangepound/) |
    """)

    # ── Generador de reporte HTML descargable ──
    st.markdown('<p class="section-header">📥 Exportar Reporte</p>', unsafe_allow_html=True)

    def generate_html_report():
        class_rate_html = survival_rate_table(df, ["Clase", "Pclass"]).sort_values("Pclass")
        filas_supervivencia = ""
        for _, r in class_rate_html.iterrows():
            filas_supervivencia += f"""
            <tr>
              <td>{r['Clase']}</td>
              <td>{int(r['Pasajeros'])}</td>
              <td>{int(r['Sobrevivientes'])}</td>
              <td><strong>{r['Probabilidad supervivencia']*100:.1f}%</strong></td>
              <td>£ {r['Tarifa_promedio']:.2f}</td>
            </tr>"""

        filas_financiero = ""
        for _, r in fare_cls.iterrows():
            cobertura_color = "#5dde8b" if r["Cobertura del costo op."] >= 100 else "#e07a5f"
            filas_financiero += f"""
            <tr>
              <td>{r['Clase']}</td>
              <td>{int(r['Pasajeros'])}</td>
              <td>£ {r['Tarifa_total_gbp']:,.0f}</td>
              <td>{r['% del total recaudado']:.1f}%</td>
              <td style="color:{cobertura_color}; font-weight:700">{r['Cobertura del costo op.']:.1f}%</td>
              <td>£ {r['Equiv. £ 2025']:,}</td>
            </tr>"""

        ganancia_color  = "#5dde8b" if ganancia_gbp >= 0 else "#e05555"
        ganancia_signo  = "+" if ganancia_gbp >= 0 else ""
        resultado_texto = "Ganancia estimada" if ganancia_gbp >= 0 else "Pérdida estimada"

        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>RMS Titanic · Reporte de Análisis</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Source+Sans+3:wght@300;400;600&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Source Sans 3', sans-serif;
      background: linear-gradient(160deg, #0c1e38 0%, #0f2848 50%, #122f54 100%);
      color: #e8f2fc; min-height: 100vh;
    }}
    /* ── PORTADA ── */
    .cover {{
      background: linear-gradient(160deg, #061220 0%, #0a1e3a 60%, #112540 100%);
      border-bottom: 2px solid #c8a84b;
      padding: 52px 56px 48px;
      position: relative; overflow: hidden;
    }}
    .cover::before {{
      content: ''; position: absolute; inset: 0;
      background: radial-gradient(ellipse at 60% 100%, rgba(200,168,50,0.1) 0%, transparent 65%);
    }}
    .cover-inner {{ display: flex; align-items: center; gap: 52px; position: relative; z-index: 1; }}
    .cover-ship {{ flex: 0 0 auto; }}
    .cover-info {{ flex: 1; }}
    .cover-rms {{ font-size: 0.82rem; color: #c8a84b; letter-spacing: 6px; text-transform: uppercase; margin-bottom: 4px; }}
    .cover-title {{
      font-family: 'Playfair Display', serif; font-size: 3.8rem; font-weight: 900;
      color: #f5ecd5; letter-spacing: 2px;
      text-shadow: 0 2px 28px rgba(180,140,40,0.5); line-height: 1.05; margin: 0 0 10px;
    }}
    .cover-subtitle {{ font-size: 1.0rem; color: #d0e8f8; letter-spacing: 0.5px; line-height: 1.5; margin-bottom: 18px; }}
    .cover-gold-line {{ height: 2px; width: 75%; background: linear-gradient(90deg, #c8a84b, rgba(200,168,75,0.15)); margin: 16px 0; }}
    .cover-uni-label {{ font-size: 0.72rem; color: #a0bcd0; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 3px; }}
    .cover-uni-name {{ font-family: 'Playfair Display', serif; font-size: 1.25rem; color: #f0dc9c; font-weight: 700; margin-bottom: 3px; }}
    .cover-uni-student {{ font-size: 1.05rem; color: #c8e4f8; margin-bottom: 2px; }}
    .cover-uni-course {{ font-size: 0.88rem; color: #90b8d0; font-style: italic; margin-bottom: 14px; }}
    .cover-meta {{ font-size: 0.8rem; color: #7a9ab8; margin-top: 10px; line-height: 1.7; }}
    /* ── CONTENIDO ── */
    .container {{ max-width: 1000px; margin: 0 auto; padding: 48px 32px 72px; }}
    .section-title {{
      font-family: 'Playfair Display', serif; font-size: 1.55rem; color: #f0dc9c;
      border-left: 4px solid #c8a84b; padding-left: 14px; margin: 40px 0 18px;
    }}
    /* ── KPI GRID ── */
    .kpi-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(175px, 1fr)); gap: 16px; margin-bottom: 10px; }}
    .kpi-card {{
      background: rgba(255,255,255,0.06); border: 1px solid rgba(200,168,75,0.28);
      border-radius: 12px; padding: 20px 16px; text-align: center;
    }}
    .kpi-value {{ font-family: 'Playfair Display', serif; font-size: 1.7rem; font-weight: 700; color: #e2bb60; line-height: 1; }}
    .kpi-label {{ font-size: 0.72rem; color: #b0c8dc; text-transform: uppercase; letter-spacing: 1.5px; margin-top: 6px; }}
    /* ── TABLA ── */
    table {{ width: 100%; border-collapse: collapse; margin-bottom: 8px; background: rgba(255,255,255,0.03); border-radius: 10px; overflow: hidden; }}
    thead {{ background: rgba(200,168,60,0.16); }}
    thead th {{ font-family: 'Playfair Display', serif; font-size: 0.85rem; color: #e2bb60; text-transform: uppercase; letter-spacing: 1px; padding: 13px 14px; text-align: left; border-bottom: 1px solid rgba(200,168,80,0.3); }}
    tbody tr {{ border-bottom: 1px solid rgba(255,255,255,0.07); }}
    tbody tr:last-child {{ border-bottom: none; }}
    tbody td {{ padding: 12px 14px; font-size: 0.95rem; color: #dceef8; }}
    tbody tr:hover {{ background: rgba(255,255,255,0.05); }}
    /* ── CAJAS DE TEXTO ── */
    .insight-box {{
      background: rgba(200,168,60,0.1); border: 1px solid rgba(200,168,60,0.25);
      border-left: 4px solid #c8a84b; border-radius: 8px; padding: 18px 22px;
      margin: 16px 0; font-size: 0.97rem; line-height: 1.78; color: #e4eff8;
    }}
    .conclusion-box {{
      background: linear-gradient(135deg, rgba(20,60,110,0.5), rgba(10,28,60,0.7));
      border: 1px solid rgba(200,168,80,0.32); border-radius: 14px;
      padding: 28px 30px; margin: 18px 0; line-height: 1.88; color: #e8f2fc;
    }}
    .conclusion-box h3 {{ font-family: 'Playfair Display', serif; font-size: 1.1rem; color: #e2bb60; margin-bottom: 12px; }}
    .note-box {{
      background: rgba(255,255,255,0.06); border: 1px solid rgba(140,180,210,0.25);
      border-radius: 8px; padding: 12px 16px; font-size: 0.83rem; color: #a8c8dc; font-style: italic; margin-top: 10px;
    }}
    /* ── OCUPACIÓN ── */
    .occ-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 14px; margin: 16px 0; }}
    .occ-card {{
      background: rgba(255,255,255,0.05); border: 1px solid rgba(200,168,80,0.22);
      border-radius: 10px;
      padding: 18px 16px; text-align: center;
    }}
    .occ-card .big {{ font-family:'Playfair Display',serif; font-size:1.4rem; color:#e2bb60; }}
    .occ-card .sub {{ font-size:0.75rem; color:#a0bcd0; text-transform:uppercase; letter-spacing:1px; margin-top:4px; }}
    .occ-card .detail {{ font-size:0.85rem; color:#c8e0f0; margin-top:6px; }}
    /* ── BARRA GANANCIA ── */
    .balance-bar {{
      display: flex; align-items: stretch; border-radius: 10px; overflow: hidden;
      height: 48px; margin: 18px 0; border: 1px solid rgba(200,168,80,0.22);
    }}
    .bar-cost {{
      background: rgba(240,112,80,0.22); display: flex; align-items: center;
      justify-content: center; font-size: 0.82rem; color: #f09878; font-weight: 600; padding: 0 12px;
    }}
    .bar-profit {{
      background: rgba(100,240,160,0.16); display: flex; align-items: center;
      justify-content: center; font-size: 0.82rem; color: #6aeea0; font-weight: 600;
      padding: 0 12px; flex: 1;
    }}
    /* ── FUENTES ── */
    .sources-list {{
      list-style: none; display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 12px; margin-top: 10px;
    }}
    .sources-list li {{
      background: rgba(255,255,255,0.05); border: 1px solid rgba(200,168,80,0.18);
      border-radius: 8px; padding: 12px 14px; font-size: 0.85rem; color: #c8e0f0;
    }}
    .sources-list li a {{ color: #7ab8e8; text-decoration: none; }}
    .sources-list li a:hover {{ text-decoration: underline; }}
    .source-name {{ color: #e2bb60; font-weight: 600; font-size: 0.9rem; }}
    /* ── FOOTER ── */
    .footer {{
      text-align: center; padding: 28px;
      border-top: 1px solid rgba(200,168,80,0.2);
      font-size: 0.8rem; color: #6a8aaa; margin-top: 40px;
    }}
  </style>
</head>
<body>

<!-- PORTADA -->
<div class="cover">
  <div class="cover-inner">
    <div class="cover-ship">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 200" width="420" height="162">
        <defs>
          <linearGradient id="h2" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" style="stop-color:#1e3a5a"/><stop offset="100%" style="stop-color:#0d1e30"/>
          </linearGradient>
          <linearGradient id="s2" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" style="stop-color:#2a4a70"/><stop offset="100%" style="stop-color:#1a3050"/>
          </linearGradient>
          <linearGradient id="f2" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" style="stop-color:#c8a84b"/>
            <stop offset="85%" style="stop-color:#a07828"/>
            <stop offset="100%" style="stop-color:#1a1a1a"/>
          </linearGradient>
        </defs>
        <ellipse cx="260" cy="174" rx="240" ry="18" fill="#1a4a7a" opacity="0.6"/>
        <path d="M20,170 Q80,165 140,170 Q200,175 260,170 Q320,165 380,170 Q440,175 500,170" stroke="#3a7aaa" stroke-width="1.5" fill="none" opacity="0.5"/>
        <path d="M40,150 L60,118 L440,118 L470,150 Q450,165 260,166 Q80,166 40,150 Z" fill="url(#h2)" stroke="#2a5a8a" stroke-width="1"/>
        <path d="M48,152 L462,152" stroke="#c8a84b" stroke-width="1.5" opacity="0.7"/>
        <rect x="80" y="82" width="340" height="38" rx="3" fill="url(#s2)" stroke="#3a6090" stroke-width="0.8"/>
        <rect x="100" y="64" width="290" height="20" rx="2" fill="#1e3858" stroke="#2a5080" stroke-width="0.8"/>
        <rect x="160" y="50" width="120" height="16" rx="2" fill="#162c48" stroke="#2a5080" stroke-width="0.8"/>
        <g fill="#6aaae0" opacity="0.6">
          <rect x="92" y="88" width="8" height="6" rx="1"/><rect x="106" y="88" width="8" height="6" rx="1"/>
          <rect x="120" y="88" width="8" height="6" rx="1"/><rect x="350" y="88" width="8" height="6" rx="1"/>
          <rect x="364" y="88" width="8" height="6" rx="1"/><rect x="378" y="88" width="8" height="6" rx="1"/>
        </g>
        <g fill="#90c4e8" opacity="0.5">
          <rect x="112" y="68" width="6" height="5" rx="1"/><rect x="124" y="68" width="6" height="5" rx="1"/>
          <rect x="340" y="68" width="6" height="5" rx="1"/><rect x="352" y="68" width="6" height="5" rx="1"/>
        </g>
        <rect x="168" y="22" width="24" height="44" rx="3" fill="url(#f2)" stroke="#806020" stroke-width="0.8"/>
        <rect x="210" y="24" width="24" height="42" rx="3" fill="url(#f2)" stroke="#806020" stroke-width="0.8"/>
        <rect x="252" y="24" width="24" height="42" rx="3" fill="url(#f2)" stroke="#806020" stroke-width="0.8"/>
        <rect x="294" y="26" width="24" height="40" rx="3" fill="url(#f2)" stroke="#806020" stroke-width="0.8"/>
        <g opacity="0.35" fill="#c8d8e8">
          <ellipse cx="180" cy="16" rx="7" ry="5"/><ellipse cx="175" cy="9" rx="5" ry="4"/>
          <ellipse cx="222" cy="17" rx="7" ry="5"/><ellipse cx="218" cy="10" rx="5" ry="4"/>
          <ellipse cx="264" cy="17" rx="6" ry="4"/>
        </g>
        <line x1="70" y1="64" x2="70" y2="8" stroke="#5a8ab0" stroke-width="1.5"/>
        <line x1="70" y1="12" x2="140" y2="64" stroke="#4a7a9a" stroke-width="0.8" opacity="0.7"/>
        <line x1="450" y1="80" x2="450" y2="30" stroke="#5a8ab0" stroke-width="1.5"/>
        <text x="430" y="142" font-size="14" fill="#c8a84b" opacity="0.8" font-family="serif">⚓</text>
      </svg>
    </div>
    <div class="cover-info">
      <div class="cover-rms">R · M · S</div>
      <h1 class="cover-title">Titanic</h1>
      <div class="cover-subtitle">Análisis de Supervivencia · Estructura de Clase · Rentabilidad del Viaje</div>
      <div class="cover-gold-line"></div>
      <div class="cover-uni-label">Trabajo · Entrega Final</div>
      <div class="cover-uni-name">Politécnico Gran Colombiano</div>
      <div class="cover-uni-student">👩‍🎓 Sara Santillana</div>
      <div class="cover-uni-course">Análisis y Visualización de Datos</div>
      <div class="cover-meta">
        Generado el {pd.Timestamp.now().strftime('%d de %B de %Y')} &nbsp;·&nbsp;
        {len(df):,} pasajeros analizados &nbsp;·&nbsp; Tasa supervivencia: {df['Survived'].mean()*100:.1f}%
      </div>
    </div>
  </div>
</div>

<div class="container">

  <!-- SECCIÓN 1: OCUPACIÓN -->
  <h2 class="section-title">Verificación de Ocupación Real</h2>
  <div class="occ-grid">
    <div class="occ-card">
      <div class="big">891</div>
      <div class="sub">Pasajeros en dataset</div>
      <div class="detail">Kaggle Training Set</div>
    </div>
    <div class="occ-card">
      <div class="big">1.317</div>
      <div class="sub">Pasajeros reales</div>
      <div class="detail">Encyclopedia Titanica</div>
    </div>
    <div class="occ-card">
      <div class="big">899</div>
      <div class="sub">Tripulantes</div>
      <div class="detail">National Archives UK</div>
    </div>
    <div class="occ-card">
      <div class="big">2.216</div>
      <div class="sub">Total a bordo</div>
      <div class="detail">Pasajeros + Tripulación</div>
    </div>
    <div class="occ-card">
      <div class="big">67,7%</div>
      <div class="sub">Cobertura del dataset</div>
      <div class="detail">891 / 1.317 pasajeros</div>
    </div>
  </div>
  <div class="note-box">
    El dataset de Kaggle corresponde únicamente al conjunto de entrenamiento y no incluye a todos los pasajeros reales.
    El análisis estadístico es válido como estimación, pero los totales financieros reales habrían sido superiores.
  </div>

  <!-- SECCIÓN 2: SUPERVIVENCIA -->
  <h2 class="section-title">Supervivencia por Clase</h2>
  <table>
    <thead>
      <tr>
        <th>Clase</th>
        <th>Pasajeros</th>
        <th>Sobrevivientes</th>
        <th>Probabilidad</th>
        <th>Tarifa promedio (£)</th>
      </tr>
    </thead>
    <tbody>
      {filas_supervivencia}
    </tbody>
  </table>
  <div class="insight-box">
    Los pasajeros de <strong>{best['Clase']}</strong> tuvieron la mayor probabilidad de sobrevivir
    (<strong>{best['Probabilidad supervivencia']*100:.1f}%</strong>), mientras que los de
    <strong>{worst['Clase']}</strong> registraron la menor (<strong>{worst['Probabilidad supervivencia']*100:.1f}%</strong>).
    La diferencia refleja la interacción entre clase social, ubicación en el buque y protocolos de evacuación.
  </div>

  <!-- SECCIÓN 3: FINANCIERO -->
  <h2 class="section-title">Análisis de Rentabilidad (£ Históricas y £ 2025)</h2>
  <div class="kpi-grid">
    <div class="kpi-card">
      <div class="kpi-value">£ {total_recaudado_gbp:,.0f}</div>
      <div class="kpi-label">Recaudado (£ 1912)</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-value">£ {op_cost_gbp:,.0f}</div>
      <div class="kpi-label">Costo operativo (£ 1912)</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-value" style="color:{ganancia_color}">{ganancia_signo}£ {abs(ganancia_gbp):,.0f}</div>
      <div class="kpi-label">{resultado_texto} (£ 1912)</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-value">£ {total_recaudado_2025:,.0f}</div>
      <div class="kpi-label">Recaudado equiv. (£ 2025)</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-value">£ {op_cost_2025:,.0f}</div>
      <div class="kpi-label">Costo equiv. (£ 2025)</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-value" style="color:{ganancia_color}">{ganancia_signo}£ {abs(ganancia_2025):,.0f}</div>
      <div class="kpi-label">{resultado_texto} (£ 2025)</div>
    </div>
  </div>

  <div class="balance-bar">
    <div class="bar-cost" style="width:{min(op_cost_gbp/total_recaudado_gbp*100, 100):.1f}%">
      Costo op. £ {op_cost_gbp:,.0f}
    </div>
    <div class="bar-profit">
      {resultado_texto}: {ganancia_signo}£ {abs(ganancia_gbp):,.0f}
    </div>
  </div>

  <table>
    <thead>
      <tr>
        <th>Clase</th>
        <th>Pasajeros</th>
        <th>Tarifa total (£ 1912)</th>
        <th>% del total</th>
        <th>Cobertura costo op.</th>
        <th>Equiv. £ 2025</th>
      </tr>
    </thead>
    <tbody>
      {filas_financiero}
    </tbody>
  </table>

  <!-- SECCIÓN 4: CONCLUSIÓN -->
  <h2 class="section-title">Conclusión e Interpretación</h2>
  <div class="conclusion-box">
    <h3>Supervivencia y clase social</h3>
    El análisis evidencia una correlación directa entre la clase del pasajero y su probabilidad de supervivencia.
    Esta diferencia es estadísticamente significativa, aunque no puede atribuirse exclusivamente al factor económico:
    también incidieron la ubicación física dentro del buque, los protocolos de evacuación y la composición
    sociodemográfica de cada clase.
    <br><br>
    <h3>Rentabilidad de la operación</h3>
    La clase que mayor aporte realizó a los ingresos fue <strong>{top_c['Clase']}</strong>, con
    <strong>£ {top_c['Tarifa_total_gbp']:,.0f}</strong> ({top_c['% del total recaudado']:.1f}% del total recaudado).
    Frente a un costo operativo estimado de <strong>£ {op_cost_gbp:,.0f}</strong>, el viaje habría generado
    una {resultado_texto.lower()} de <strong style="color:{ganancia_color}">£ {abs(ganancia_gbp):,.0f}</strong> (1912),
    equivalente a <strong style="color:{ganancia_color}">£ {abs(ganancia_2025):,.0f}</strong> en valores de 2025
    (factor ×{inflation_factor:.0f}, Banco de Inglaterra).
  </div>

  <div class="insight-box">
    <strong>📌 Reflexión </strong><br>
    st.markdown(
    st.markdown(
    "El presente análisis busca ir más allá de una simple descripción de la distribución de los pasajeros a bordo del Titanic en 1912, con el propósito de comprender cómo el mercado de transporte marítimo transatlántico estaba estructurado estratégicamente en clases y así identificar qué segmento generaba un mayor retorno económico. Los resultados evidencian que la primera clase no solo aportaba el mayor ingreso por pasajero —con tarifas significativamente superiores a las de segunda y tercera clase—, sino que también constituía un segmento clave para que la White Star Line pudiera financiar, justificar y rentabilizar la operación de buques de gran escala. En este sentido, analizar la composición de ingresos del Titanic permite establecer un paralelismo con las operaciones actuales de transporte internacional, donde resulta fundamental comprender quién paga y cuánto para determinar la sostenibilidad del modelo de negocio. Adicionalmente, el análisis de los datos permitió identificar una relación directa entre el acceso a una clase superior y una mayor probabilidad de supervivencia, según la información contenida en la base de datos proporcionada. Finalmente, el uso de herramientas de inteligencia artificial facilitó la obtención de información complementaria, como el costo estimado de operación del buque en la época y la ruta planificada, enriqueciendo el contexto y fortaleciendo la interpretación de los resultados."
)
  </div>

  <!-- SECCIÓN 5: FUENTES -->
  <h2 class="section-title">Fuentes y Referencias</h2>
  <ul class="sources-list">
    <li>
      <div class="source-name">Encyclopedia Titanica</div>
      Información histórica por pasajero<br>
      <a href="https://www.encyclopedia-titanica.org" target="_blank">encyclopedia-titanica.org</a>
    </li>
    <li>
      <div class="source-name">National Archives UK</div>
      Vida a bordo del Titanic<br>
      <a href="https://www.nationalarchives.gov.uk/education/resources/life-aboard-titanic/" target="_blank">nationalarchives.gov.uk</a>
    </li>
    <li>
      <div class="source-name">Bank of England</div>
      Calculadora de inflación histórica<br>
      <a href="https://www.bankofengland.co.uk/monetary-policy/inflation/inflation-calculator" target="_blank">bankofengland.co.uk</a>
    </li>
    <li>
      <div class="source-name">MeasuringWorth</div>
      Tasas históricas de cambio £/USD<br>
      <a href="https://www.measuringworth.com/datasets/exchangepound/" target="_blank">measuringworth.com</a>
    </li>
  </ul>

</div>

<div class="footer">
  Análisis desarrollado con Python · Streamlit · Pandas · Plotly &nbsp;|&nbsp;
  Asistido por inteligencia artificial · Perspectiva y criterio: del estudiante &nbsp;|&nbsp;
  Datos: Kaggle Titanic Dataset
</div>

</body>
</html>"""
        return html

    html_reporte = generate_html_report()
    st.download_button(
        label="⬇️  Descargar Reporte Completo (.html)",
        data=html_reporte.encode("utf-8"),
        file_name="titanic_reporte_analisis.html",
        mime="text/html",
        use_container_width=True,
        help="Descarga un reporte HTML completo con todos los datos, tablas y conclusiones — listo para entregar o imprimir."
    )
