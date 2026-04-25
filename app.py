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

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Source+Sans+3:wght@300;400;600&display=swap');
[data-testid="stAppViewContainer"] { background: linear-gradient(160deg, #0c1e38 0%, #0f2848 40%, #122f54 100%); background-attachment: fixed; }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #091828 0%, #0d2240 100%); border-right: 1px solid rgba(200,168,75,0.4); }
[data-testid="stSidebar"] * { color: #f0f6fc !important; }
[data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span { color: #e8f2fc !important; }
[data-testid="stSidebar"] .stMarkdown h2, [data-testid="stSidebar"] .stMarkdown h3 { color: #f0c84a !important; font-family: 'Playfair Display', serif; }
[data-testid="stSidebar"] a { color: #80c4f0 !important; }
html, body, [class*="css"], p, span, li, td, th, div { font-family: 'Source Sans 3', sans-serif; color: #f0f6fc; }
h1, h2, h3 { font-family: 'Playfair Display', serif; color: #f5ecd5; }
[data-testid="stDataFrame"] * { color: #ffffff !important; }
[data-testid="stDataFrame"] th { color: #f0c84a !important; font-weight: 700; }
.stDataFrame { border-radius: 10px; }
iframe { color-scheme: dark; }
.stMarkdown table td { color: #f0f6fc !important; }
.stMarkdown table th { color: #f0c84a !important; }
.hero-wrap { display: flex; align-items: center; gap: 40px; background: linear-gradient(135deg, rgba(8,24,52,0.96), rgba(6,16,36,0.98)); border: 1px solid rgba(200,168,75,0.5); border-radius: 18px; padding: 36px 44px; margin-bottom: 10px; box-shadow: 0 10px 48px rgba(0,0,0,0.6); }
.hero-ship { flex: 0 0 auto; }
.hero-text { flex: 1; min-width: 0; }
.hero-rms { font-size: 0.8rem; color: #d4aa50; letter-spacing: 6px; text-transform: uppercase; margin-bottom: 4px; }
.hero-title { font-family: 'Playfair Display', serif; font-size: 3.6rem; font-weight: 900; color: #fff8e8; letter-spacing: 2px; text-shadow: 0 2px 30px rgba(200,160,40,0.5); line-height: 1.05; margin: 0 0 8px; }
.hero-subtitle { font-size: 1.02rem; color: #cce6f8; letter-spacing: 0.4px; line-height: 1.5; margin-bottom: 18px; }
.hero-gold-line { height: 2px; width: 80%; border: none; margin: 12px 0 16px; background: linear-gradient(90deg, #d4aa50, rgba(200,168,75,0.1)); }
.hero-uni-tag { font-size: 0.7rem; color: #b8d4e8; text-transform: uppercase; letter-spacing: 2.5px; margin-bottom: 4px; }
.hero-uni-name { font-family: 'Playfair Display', serif; font-size: 1.2rem; font-weight: 700; color: #ffe98a; margin-bottom: 3px; }
.hero-student { font-size: 1.0rem; color: #d8eeff; margin-bottom: 2px; }
.hero-course { font-size: 0.84rem; color: #a8cce0; font-style: italic; }
.divider-gold { border: none; height: 2px; background: linear-gradient(90deg, transparent, #d4aa50, #c8a84b, transparent); margin: 14px auto 28px; width: 60%; }
.kpi-card { background: rgba(255,255,255,0.08); border: 1px solid rgba(200,168,75,0.35); border-radius: 12px; padding: 20px 14px; text-align: center; backdrop-filter: blur(8px); margin-bottom: 12px; }
.kpi-value { font-family: 'Playfair Display', serif; font-size: 1.9rem; font-weight: 700; color: #f0c84a; line-height: 1; }
.kpi-label { font-size: 0.72rem; color: #cce0f2; text-transform: uppercase; letter-spacing: 1.4px; margin-top: 6px; }
.section-header { font-family: 'Playfair Display', serif; font-size: 1.5rem; color: #ffe98a; border-left: 4px solid #d4aa50; padding-left: 14px; margin: 28px 0 14px; }
.insight-box { background: rgba(200,168,60,0.12); border: 1px solid rgba(200,168,60,0.3); border-left: 4px solid #d4aa50; border-radius: 8px; padding: 16px 20px; margin: 14px 0; font-size: 0.97rem; line-height: 1.78; color: #f0f8ff; }
.conclusion-box { background: linear-gradient(135deg, rgba(16,52,100,0.6), rgba(8,24,55,0.8)); border: 1px solid rgba(200,168,80,0.4); border-radius: 14px; padding: 26px 30px; margin: 18px 0; line-height: 1.88; font-size: 1.0rem; color: #f0f8ff; }
.note-box { background: rgba(255,255,255,0.07); border: 1px solid rgba(160,200,230,0.3); border-radius: 8px; padding: 12px 16px; font-size: 0.85rem; color: #cce0f0; font-style: italic; margin-top: 10px; }
.stTabs [data-baseweb="tab-list"] { gap: 4px; background: rgba(255,255,255,0.06); border-radius: 10px; padding: 4px; }
.stTabs [data-baseweb="tab"] { border-radius: 8px; padding: 8px 22px; color: #cce0f4 !important; font-family: 'Source Sans 3', sans-serif; font-size: 0.9rem; }
.stTabs [aria-selected="true"] { background: linear-gradient(135deg, #1a3a60, #1e4878) !important; color: #f0c84a !important; border-bottom: 2px solid #d4aa50 !important; }
.stAlert p, .stSuccess p { color: #ffffff !important; }
.stDownloadButton button { background: linear-gradient(135deg, #1a3a60, #1e4878) !important; color: #f0c84a !important; border: 1px solid rgba(200,168,75,0.5) !important; font-size: 1rem !important; padding: 12px 24px !important; border-radius: 8px !important; }
</style>
""", unsafe_allow_html=True)

# ── Barco SVG en base64 ──
_SHIP_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 210" width="420" height="158">
  <defs>
    <linearGradient id="hG" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#1e3a5a"/><stop offset="100%" stop-color="#0d1e30"/></linearGradient>
    <linearGradient id="sG" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#2e5278"/><stop offset="100%" stop-color="#1a3050"/></linearGradient>
    <linearGradient id="fG" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#e8c060"/><stop offset="82%" stop-color="#a07828"/><stop offset="100%" stop-color="#1a1a1a"/></linearGradient>
    <linearGradient id="skG" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#081830" stop-opacity="0"/><stop offset="100%" stop-color="#0a2040" stop-opacity="0.5"/></linearGradient>
  </defs>
  <rect x="0" y="0" width="560" height="160" fill="url(#skG)" rx="8"/>
  <g fill="#fff" opacity="0.5"><circle cx="30" cy="20" r="1"/><circle cx="80" cy="10" r="1"/><circle cx="130" cy="25" r="1.2"/><circle cx="500" cy="15" r="1"/><circle cx="460" cy="8" r="1.2"/><circle cx="380" cy="18" r="0.9"/><circle cx="310" cy="6" r="1"/></g>
  <ellipse cx="280" cy="186" rx="260" ry="20" fill="#1a4a7a" opacity="0.55"/>
  <path d="M20,182 Q90,176 160,182 Q230,188 300,182 Q370,176 440,182 Q500,188 540,182" stroke="#4a8ab8" stroke-width="1.5" fill="none" opacity="0.6"/>
  <ellipse cx="280" cy="184" rx="120" ry="5" fill="#d4aa50" opacity="0.07"/>
  <path d="M50,162 L75,126 L475,126 L505,162 Q480,178 280,179 Q100,178 50,162 Z" fill="url(#hG)" stroke="#2a5a8a" stroke-width="1.2"/>
  <path d="M58,164 L498,164" stroke="#d4aa50" stroke-width="2" opacity="0.75"/>
  <path d="M68,138 L480,138 L482,145 L66,145 Z" fill="#e8f4ff" opacity="0.1"/>
  <rect x="90" y="90" width="368" height="38" rx="4" fill="url(#sG)" stroke="#3a6898" stroke-width="1"/>
  <rect x="112" y="70" width="318" height="22" rx="3" fill="#1e3858" stroke="#2a5888" stroke-width="0.8"/>
  <rect x="185" y="55" width="130" height="17" rx="3" fill="#162c48" stroke="#2a5080" stroke-width="0.8"/>
  <rect x="175" y="60" width="15" height="12" rx="2" fill="#1a3450"/><rect x="310" y="60" width="15" height="12" rx="2" fill="#1a3450"/>
  <g fill="#80c0f0" opacity="0.65"><rect x="102" y="97" width="10" height="7" rx="1.5"/><rect x="118" y="97" width="10" height="7" rx="1.5"/><rect x="134" y="97" width="10" height="7" rx="1.5"/><rect x="395" y="97" width="10" height="7" rx="1.5"/><rect x="411" y="97" width="10" height="7" rx="1.5"/><rect x="427" y="97" width="10" height="7" rx="1.5"/><rect x="443" y="97" width="10" height="7" rx="1.5"/></g>
  <g fill="#a0d4f8" opacity="0.55"><rect x="124" y="74" width="8" height="6" rx="1"/><rect x="138" y="74" width="8" height="6" rx="1"/><rect x="360" y="74" width="8" height="6" rx="1"/><rect x="374" y="74" width="8" height="6" rx="1"/><rect x="388" y="74" width="8" height="6" rx="1"/></g>
  <g fill="#c0e4ff" opacity="0.6"><circle cx="200" cy="63" r="4"/><circle cx="220" cy="63" r="4"/><circle cx="240" cy="63" r="4"/><circle cx="260" cy="63" r="4"/><circle cx="280" cy="63" r="4"/></g>
  <rect x="190" y="24" width="26" height="48" rx="4" fill="url(#fG)" stroke="#906020" stroke-width="0.9"/><rect x="190" y="48" width="26" height="5" fill="#0a0a0a" opacity="0.9"/>
  <rect x="232" y="26" width="26" height="46" rx="4" fill="url(#fG)" stroke="#906020" stroke-width="0.9"/><rect x="232" y="48" width="26" height="5" fill="#0a0a0a" opacity="0.9"/>
  <rect x="274" y="26" width="26" height="46" rx="4" fill="url(#fG)" stroke="#906020" stroke-width="0.9"/><rect x="274" y="48" width="26" height="5" fill="#0a0a0a" opacity="0.9"/>
  <rect x="316" y="28" width="26" height="44" rx="4" fill="url(#fG)" stroke="#906020" stroke-width="0.9"/><rect x="316" y="48" width="26" height="5" fill="#0a0a0a" opacity="0.8"/>
  <g opacity="0.4"><ellipse cx="203" cy="17" rx="9" ry="6" fill="#b0c4d8"/><ellipse cx="197" cy="9" rx="6" ry="5" fill="#a0b4c8"/><ellipse cx="245" cy="18" rx="9" ry="6" fill="#b0c4d8"/><ellipse cx="240" cy="10" rx="6" ry="5" fill="#a0b4c8"/><ellipse cx="287" cy="18" rx="8" ry="6" fill="#b0c4d8"/></g>
  <line x1="80" y1="70" x2="80" y2="6" stroke="#6090b8" stroke-width="2"/>
  <line x1="80" y1="10" x2="165" y2="68" stroke="#5080a0" stroke-width="1" opacity="0.7"/>
  <line x1="80" y1="10" x2="40" y2="55" stroke="#5080a0" stroke-width="0.8" opacity="0.5"/>
  <line x1="490" y1="88" x2="490" y2="30" stroke="#6090b8" stroke-width="2"/>
  <line x1="80" y1="10" x2="200" y2="52" stroke="#406080" stroke-width="0.7" opacity="0.5"/>
  <line x1="490" y1="32" x2="330" y2="52" stroke="#406080" stroke-width="0.7" opacity="0.5"/>
  <text x="470" y="155" font-size="16" fill="#d4aa50" opacity="0.85" font-family="serif">⚓</text>
  <g fill="#2a5080" stroke="#3a6898" stroke-width="0.5"><rect x="155" y="127" width="20" height="8" rx="1"/><rect x="195" y="127" width="20" height="8" rx="1"/><rect x="390" y="127" width="20" height="8" rx="1"/><rect x="430" y="127" width="20" height="8" rx="1"/></g>
</svg>"""
_B64 = base64.b64encode(_SHIP_SVG.encode("utf-8")).decode("utf-8")
SHIP_TAG = f'<img src="data:image/svg+xml;base64,{_B64}" width="420" height="158" alt="RMS Titanic" style="display:block;">'

# ── Constantes mínimas ──
PORTS = {
    "S":  {"name": "Southampton",       "country": "Inglaterra",     "lat": 50.9097, "lon": -1.4044},
    "C":  {"name": "Cherbourg",         "country": "Francia",        "lat": 49.6337, "lon": -1.6221},
    "Q":  {"name": "Queenstown / Cobh", "country": "Irlanda",        "lat": 51.8503, "lon": -8.2943},
    "NY": {"name": "New York",          "country": "Estados Unidos", "lat": 40.7128, "lon": -74.0060},
}
CLASS_LABELS    = {1: "Primera clase", 2: "Segunda clase", 3: "Tercera clase"}
SURVIVAL_LABELS = {0: "No sobrevivió", 1: "Sobrevivió"}
COLORS = {"Primera clase": "#d4aa50", "Segunda clase": "#5b9bd5", "Tercera clase": "#e07a5f"}

# ── Carga y limpieza (todo desde el Excel) ──
@st.cache_data
def load_data(uploaded_file=None):
    source = uploaded_file if uploaded_file is not None else "train.xlsx"
    raw = pd.read_excel(source, header=None)
    ph = raw.iloc[1].astype(str).tolist()
    if "PassengerId" in ph and "Survived" in ph:
        df = raw.iloc[2:].copy(); df.columns = ph
    else:
        df = pd.read_excel(source)
    df.columns = [str(c).strip() for c in df.columns]
    for col in ["PassengerId","Survived","Pclass","Age","SibSp","Parch","Fare"]:
        if col in df.columns: df[col] = pd.to_numeric(df[col], errors="coerce")
    if "Embarked" in df.columns:
        df["Embarked"] = df["Embarked"].astype("string").str.strip().str.upper()
        df["Embarked"] = df["Embarked"].replace({"": pd.NA, "NAN": pd.NA})
        df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode(dropna=True).iloc[0])
    if "Sex" in df.columns: df["Sex"] = df["Sex"].astype("string").str.strip().str.lower()
    if "Age" in df.columns:
        df["Age_missing"] = df["Age"].isna()
        df["Age"] = df["Age"].fillna(df["Age"].median())
    if "Fare" in df.columns: df["Fare"] = df["Fare"].fillna(df["Fare"].median())
    df["Clase"]         = df["Pclass"].map(CLASS_LABELS)
    df["Supervivencia"] = df["Survived"].map(SURVIVAL_LABELS)
    df["Puerto"]        = df["Embarked"].map(lambda x: f"{x} - {PORTS.get(x,{}).get('name','Desconocido')}")
    df["Sexo"]          = df["Sex"].map({"male":"Hombre","female":"Mujer"}).fillna(df["Sex"])
    df["Grupo edad"]    = pd.cut(df["Age"], bins=[-1,12,18,35,60,120],
                                  labels=["Niñez (0-12)","Adolescencia (13-18)","Adulto joven (19-35)","Adulto (36-60)","Mayor (60+)"])
    return df

def surv_table(df, cols):
    return df.groupby(cols, dropna=False).agg(
        Pasajeros=("PassengerId","count"), Sobrevivientes=("Survived","sum"),
        Tarifa_total=("Fare","sum"), Tarifa_promedio=("Fare","mean"), Edad_promedio=("Age","mean")
    ).reset_index().assign(**{"Probabilidad supervivencia": lambda x: x["Sobrevivientes"]/x["Pasajeros"]})

def pct(s): return (s*100).round(1).astype(str)+"%"

def theme():
    return dict(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#e0ecf8", family="Source Sans 3"),
                title_font=dict(family="Playfair Display", color="#f0dc9c"),
                legend=dict(bgcolor="rgba(0,0,0,0.3)", bordercolor="rgba(200,168,75,0.3)", borderwidth=1),
                colorway=list(COLORS.values()))

# ── Encabezado ──
st.markdown(f"""
<div class="hero-wrap">
  <div class="hero-ship">{SHIP_TAG}</div>
  <div class="hero-text">
    <div class="hero-rms">R &nbsp;·&nbsp; M &nbsp;·&nbsp; S</div>
    <div class="hero-title">Titanic</div>
    <div class="hero-subtitle">Análisis de Supervivencia &nbsp;·&nbsp; Estructura de Clase &nbsp;·&nbsp; Rentabilidad del Viaje</div>
    <hr class="hero-gold-line">
    <div class="hero-uni-tag">Trabajo · Entrega Final</div>
    <div class="hero-uni-name">Politécnico Gran Colombiano</div>
    <div class="hero-student">👩‍🎓 &nbsp;Sara Santillana</div>
    <div class="hero-course">Análisis y Visualización de Datos</div>
  </div>
</div>
<hr class="divider-gold">
""", unsafe_allow_html=True)

# ── Sidebar ──
with st.sidebar:
    st.markdown("## ⚓ Panel de Control")
    st.markdown("---")
    uploaded = st.file_uploader("Cargar base Titanic (.xlsx)", type=["xlsx","xls"])
    st.markdown("---")
    st.markdown("### 💰 Parámetros Financieros (£)")
    op_cost_gbp = st.number_input("Costo operativo estimado del viaje (£)", min_value=0.0, value=27_000.0, step=500.0,
        help="Costo en libras de 1912. Ajústalo según la fuente que uses.")
    inflation_factor = st.number_input("Factor de inflación (£1912 → £2025)", min_value=1.0, value=128.0, step=1.0,
        help="Banco de Inglaterra: £1 en 1912 ≈ £128 en 2025.")
    st.markdown("---")
    
    st.markdown("---")
    st.markdown("### 📚 Fuentes")
    st.markdown("""
    - [National Archives UK](https://www.nationalarchives.gov.uk/education/resources/life-aboard-titanic/)
    - [Bank of England](https://www.bankofengland.co.uk/monetary-policy/inflation/inflation-calculator)
    - [Encyclopedia Titanica](https://www.encyclopedia-titanica.org)
    """)

df = load_data(uploaded)

tabs = st.tabs(["🔍 Verificación de Datos", "📊 Análisis Visual", "🗺️ Ruta del Titanic", "💷 Conclusión & Rentabilidad"])

# ══════════════════════════════════════════════
# TAB 1 — VERIFICACIÓN (100% desde df, sin datos externos)
# ══════════════════════════════════════════════
with tabs[0]:
    st.markdown('<p class="section-header">Módulo 1 · Verificación y Calidad de Datos</p>', unsafe_allow_html=True)
    st.markdown('<div class="note-box">📌 Todo el análisis se basa <strong>exclusivamente</strong> en el archivo Excel cargado. No se incorpora ningún dato externo.</div>', unsafe_allow_html=True)

    total_p  = len(df)
    surv_pct = df["Survived"].mean() * 100
    fare_tot = df["Fare"].sum()
    age_med  = df["Age"].median()
    null_age = int(df["Age_missing"].sum()) if "Age_missing" in df.columns else 0
    n_cls    = df["Pclass"].nunique()

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    for col,val,lbl in [(c1,f"{total_p:,}","Registros en el archivo"),(c2,f"{surv_pct:.1f}%","Tasa de supervivencia"),
                        (c3,f"£ {fare_tot:,.0f}","Total tarifas (£)"),(c4,f"{age_med:.1f} años","Edad mediana"),
                        (c5,f"{null_age}","Edades imputadas"),(c6,f"{n_cls}","Clases detectadas")]:
        col.markdown(f'<div class="kpi-card"><div class="kpi-value">{val}</div><div class="kpi-label">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown('<p class="section-header">Validación de campos requeridos</p>', unsafe_allow_html=True)
    required = ["PassengerId","Survived","Pclass","Name","Sex","Age","Fare","Embarked"]
    st.dataframe(pd.DataFrame({
        "Campo": required,
        "Existe": ["✅" if c in df.columns else "❌" for c in required],
        "Valores nulos": [int(df[c].isna().sum()) if c in df.columns else "N/A" for c in required],
        "Tipo detectado": [str(df[c].dtype) if c in df.columns else "—" for c in required],
    }), use_container_width=True, hide_index=True)

    st.markdown('<p class="section-header">Composición del dataset por clase</p>', unsafe_allow_html=True)
    comp = (df.groupby(["Clase","Pclass"]).agg(
                Pasajeros=("PassengerId","count"), Sobrevivientes=("Survived","sum"),
                Tarifa_promedio=("Fare","mean"), Edad_promedio=("Age","mean"))
              .reset_index().sort_values("Pclass"))
    comp["% del total"]    = (comp["Pasajeros"]/total_p*100).round(1).astype(str)+"%"
    comp["Tasa superv."]   = pct(comp["Sobrevivientes"]/comp["Pasajeros"])
    comp["Tarifa prom. (£)"] = comp["Tarifa_promedio"].round(2)
    comp["Edad prom."]     = comp["Edad_promedio"].round(1)
    st.dataframe(comp[["Clase","Pasajeros","% del total","Sobrevivientes","Tasa superv.","Tarifa prom. (£)","Edad prom."]], use_container_width=True, hide_index=True)

    st.markdown('<p class="section-header">Composición por puerto de embarque</p>', unsafe_allow_html=True)
    cp = df.groupby("Puerto").agg(Pasajeros=("PassengerId","count"),Sobrevivientes=("Survived","sum")).reset_index()
    cp["% del total"]  = (cp["Pasajeros"]/total_p*100).round(1).astype(str)+"%"
    cp["Tasa superv."] = pct(cp["Sobrevivientes"]/cp["Pasajeros"])
    st.dataframe(cp[["Puerto","Pasajeros","% del total","Sobrevivientes","Tasa superv."]], use_container_width=True, hide_index=True)

    problems = []
    if not all(c in df.columns for c in required): problems.append("Faltan columnas requeridas.")
    if df["Survived"].dropna().isin([0,1]).mean() < 1: problems.append("La variable Survived tiene valores fuera de 0 y 1.")
    if df["Pclass"].dropna().isin([1,2,3]).mean() < 1: problems.append("La variable Pclass tiene valores fuera de 1, 2, 3.")
    if df["Embarked"].dropna().isin(["S","C","Q"]).mean() < 1: problems.append("La variable Embarked tiene valores inesperados.")
    if problems:
        for p in problems: st.warning(p)
    else:
        st.success("Base de datos validada ✓ — Estructura consistente. Se procede al análisis exploratorio.")

    st.markdown('<p class="section-header">Vista previa (primeros 25 registros)</p>', unsafe_allow_html=True)
    st.dataframe(df.head(25), use_container_width=True)

# ══════════════════════════════════════════════
# TAB 2 — ANÁLISIS VISUAL
# ══════════════════════════════════════════════
with tabs[1]:
    st.markdown('<p class="section-header">Módulo 2 · Análisis Visual de Supervivencia</p>', unsafe_allow_html=True)

    cr = surv_table(df, ["Clase","Pclass"]).sort_values("Pclass")
    fig1 = px.bar(cr, x="Clase", y="Probabilidad supervivencia", text=pct(cr["Probabilidad supervivencia"]),
                  hover_data=["Pasajeros","Sobrevivientes","Tarifa_promedio"],
                  color="Clase", color_discrete_map=COLORS, title="Probabilidad de supervivencia por clase")
    fig1.update_traces(textfont_size=14, textposition="outside", marker_line_width=0, opacity=0.9)
    fig1.update_layout(yaxis_tickformat=".0%", yaxis_title="Probabilidad", xaxis_title="", showlegend=False, **theme())
    st.plotly_chart(fig1, use_container_width=True)

    c1,c2 = st.columns(2)
    with c1:
        sc = surv_table(df,["Clase","Pclass","Sexo"]).sort_values(["Pclass","Sexo"])
        fig2 = px.bar(sc, x="Clase", y="Probabilidad supervivencia", color="Sexo", barmode="group",
                      text=pct(sc["Probabilidad supervivencia"]),
                      color_discrete_map={"Hombre":"#5b9bd5","Mujer":"#e07a8f"}, title="Supervivencia por sexo y clase")
        fig2.update_layout(yaxis_tickformat=".0%", yaxis_title="", xaxis_title="", **theme())
        st.plotly_chart(fig2, use_container_width=True)
    with c2:
        ac = surv_table(df,["Clase","Pclass","Grupo edad"]).sort_values(["Pclass","Grupo edad"])
        fig3 = px.bar(ac, x="Grupo edad", y="Probabilidad supervivencia", color="Clase", barmode="group",
                      text=pct(ac["Probabilidad supervivencia"]), color_discrete_map=COLORS,
                      title="Supervivencia por grupo de edad y clase")
        fig3.update_layout(yaxis_tickformat=".0%", yaxis_title="", xaxis_title="", **theme())
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<p class="section-header">Pasajeros por puerto de embarque</p>', unsafe_allow_html=True)
    pc = df.groupby(["Puerto","Clase","Pclass"]).size().reset_index(name="Pasajeros").sort_values(["Puerto","Pclass"])
    fig4 = px.bar(pc, x="Puerto", y="Pasajeros", color="Clase", barmode="group",
                  color_discrete_map=COLORS, title="Pasajeros por puerto y clase")
    fig4.update_layout(xaxis_title="", yaxis_title="Pasajeros", **theme())
    st.plotly_chart(fig4, use_container_width=True)

    c3,c4 = st.columns(2)
    with c3:
        ps = surv_table(df,["Puerto"])
        fig5 = px.bar(ps, x="Puerto", y="Probabilidad supervivencia", text=pct(ps["Probabilidad supervivencia"]),
                      color="Puerto", title="Supervivencia por puerto de embarque")
        fig5.update_layout(yaxis_tickformat=".0%", yaxis_title="", xaxis_title="", showlegend=False, **theme())
        st.plotly_chart(fig5, use_container_width=True)
    with c4:
        fig6 = px.box(df, x="Clase", y="Fare", points="outliers", color="Clase", color_discrete_map=COLORS,
                      title="Distribución de tarifas por clase (£)")
        fig6.update_layout(xaxis_title="", yaxis_title="Tarifa (£)", showlegend=False, **theme())
        st.plotly_chart(fig6, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 3 — RUTA (contexto histórico, no afecta cálculos)
# ══════════════════════════════════════════════
with tabs[2]:
    st.markdown('<p class="section-header">Ruta del RMS Titanic — Abril de 1912</p>', unsafe_allow_html=True)
    route = ["S","C","Q","NY"]
    rdf = pd.DataFrame([{"Puerto":PORTS[k]["name"],"Código":k,"País":PORTS[k]["country"],
                          "lat":PORTS[k]["lat"],"lon":PORTS[k]["lon"],"Orden":i+1} for i,k in enumerate(route)])
    figr = go.Figure()
    figr.add_trace(go.Scattergeo(lon=rdf["lon"], lat=rdf["lat"], mode="lines+markers+text",
        text=rdf["Puerto"], textposition="top center",
        textfont=dict(size=13, color="#d4aa50", family="Playfair Display"),
        marker=dict(size=12, color="#d4aa50", symbol="circle", line=dict(width=2, color="#f0e6c8")),
        line=dict(width=3, color="#5b9bd5"),
        hovertext=rdf["Código"]+" — "+rdf["Puerto"]+", "+rdf["País"], hoverinfo="text"))
    figr.update_geos(projection_type="natural earth", showcountries=True, showland=True, showocean=True,
                     landcolor="#1a2e42", oceancolor="#0a1628", countrycolor="rgba(180,150,80,0.3)",
                     fitbounds="locations", bgcolor="rgba(0,0,0,0)")
    figr.update_layout(title=dict(text="Southampton → Cherbourg → Queenstown / Cobh → New York",
                                  font=dict(family="Playfair Display", size=16, color="#e8d5a0")),
                       height=600, margin=dict(l=0,r=0,t=60,b=0), **theme())
    st.plotly_chart(figr, use_container_width=True)
    st.markdown('<div class="insight-box">🗓️ <strong>10 de abril de 1912</strong>: El Titanic zarpó de Southampton hacia Nueva York, con escalas en Cherbourg (Francia) y Queenstown (Irlanda). En la madrugada del <strong>15 de abril de 1912</strong>, el buque colisionó con un iceberg y se hundió en el Atlántico Norte.</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 4 — CONCLUSIÓN (todo desde df)
# ══════════════════════════════════════════════
with tabs[3]:
    st.markdown('<p class="section-header">Módulo 3 · Conclusión · Rentabilidad del Viaje</p>', unsafe_allow_html=True)

    fare_cls = (df.groupby(["Clase","Pclass"])
                  .agg(Tarifa_total_gbp=("Fare","sum"), Pasajeros=("PassengerId","count"))
                  .reset_index().sort_values("Pclass"))
    tot_gbp  = fare_cls["Tarifa_total_gbp"].sum()
    gan_gbp  = tot_gbp - op_cost_gbp
    tot_2025 = tot_gbp * inflation_factor
    op_2025  = op_cost_gbp * inflation_factor
    gan_2025 = gan_gbp * inflation_factor
    fare_cls["% del total"]    = (fare_cls["Tarifa_total_gbp"]/tot_gbp*100).round(1)
    fare_cls["Cobertura (%)"]  = (fare_cls["Tarifa_total_gbp"]/op_cost_gbp*100).round(1)
    fare_cls["Equiv. £ 2025"]  = (fare_cls["Tarifa_total_gbp"]*inflation_factor).round(0).astype(int)

    cg = "#6aeea0" if gan_gbp >= 0 else "#f07070"
    sg = "+" if gan_gbp >= 0 else ""
    rg = "ganancia" if gan_gbp >= 0 else "pérdida"

    k1,k2,k3 = st.columns(3)
    k1.markdown(f'<div class="kpi-card"><div class="kpi-value">£ {tot_gbp:,.0f}</div><div class="kpi-label">Total recaudado (£ 1912)</div></div>', unsafe_allow_html=True)
    k2.markdown(f'<div class="kpi-card"><div class="kpi-value">£ {op_cost_gbp:,.0f}</div><div class="kpi-label">Costo operativo (£ 1912)</div></div>', unsafe_allow_html=True)
    k3.markdown(f'<div class="kpi-card"><div class="kpi-value" style="color:{cg}">{sg}£ {abs(gan_gbp):,.0f}</div><div class="kpi-label">{"Ganancia" if gan_gbp>=0 else "Pérdida"} estimada (£ 1912)</div></div>', unsafe_allow_html=True)
    k4,k5,k6 = st.columns(3)
    k4.markdown(f'<div class="kpi-card"><div class="kpi-value">£ {tot_2025:,.0f}</div><div class="kpi-label">Total recaudado equiv. (£ 2025)</div></div>', unsafe_allow_html=True)
    k5.markdown(f'<div class="kpi-card"><div class="kpi-value">£ {op_2025:,.0f}</div><div class="kpi-label">Costo op. equiv. (£ 2025)</div></div>', unsafe_allow_html=True)
    k6.markdown(f'<div class="kpi-card"><div class="kpi-value" style="color:{cg}">{sg}£ {abs(gan_2025):,.0f}</div><div class="kpi-label">{"Ganancia" if gan_gbp>=0 else "Pérdida"} equiv. (£ 2025)</div></div>', unsafe_allow_html=True)

    st.markdown('<p class="section-header">Aporte de cada clase a la operación</p>', unsafe_allow_html=True)
    st.dataframe(fare_cls[["Clase","Pasajeros","Tarifa_total_gbp","% del total","Cobertura (%)","Equiv. £ 2025"]]
                 .rename(columns={"Tarifa_total_gbp":"Tarifa total (£ 1912)"}),
                 use_container_width=True, hide_index=True)

    ca,cb = st.columns(2)
    with ca:
        fp = px.pie(fare_cls, names="Clase", values="Tarifa_total_gbp", color="Clase", color_discrete_map=COLORS,
                    title="Participación por clase en ingresos totales (£ 1912)")
        fp.update_traces(textinfo="percent+label", textfont_size=13, marker=dict(line=dict(color="#0a1628",width=2)))
        fp.update_layout(**theme()); st.plotly_chart(fp, use_container_width=True)
    with cb:
        fc = px.bar(fare_cls, x="Clase", y="Cobertura (%)", color="Clase", color_discrete_map=COLORS,
                    text=fare_cls["Cobertura (%)"].astype(str)+"%", title="Cobertura del costo operativo por clase (%)")
        fc.add_hline(y=100, line_dash="dot", line_color="#d4aa50", annotation_text="100% — costo cubierto", annotation_font_color="#d4aa50")
        fc.update_layout(yaxis_title="% de cobertura", xaxis_title="", showlegend=False, **theme())
        st.plotly_chart(fc, use_container_width=True)

    st.markdown('<p class="section-header">Interpretación del análisis</p>', unsafe_allow_html=True)
    crc  = surv_table(df,["Clase","Pclass"]).sort_values("Pclass")
    best = crc.loc[crc["Probabilidad supervivencia"].idxmax()]
    wrst = crc.loc[crc["Probabilidad supervivencia"].idxmin()]
    topc = fare_cls.loc[fare_cls["Tarifa_total_gbp"].idxmax()]

    st.markdown(f"""
    <div class="conclusion-box">
    <strong style="font-family:'Playfair Display',serif;font-size:1.15rem;color:#d4aa50;">Supervivencia y clase social</strong><br><br>
    Según los datos del archivo, los pasajeros de <strong>{best['Clase']}</strong> presentaron la mayor probabilidad de sobrevivir
    (<strong>{best['Probabilidad supervivencia']*100:.1f}%</strong>), mientras que los de <strong>{wrst['Clase']}</strong>
    registraron la menor (<strong>{wrst['Probabilidad supervivencia']*100:.1f}%</strong>).
    Esta diferencia es estadísticamente significativa aunque no puede atribuirse exclusivamente al factor económico:
    también incidieron la ubicación dentro del buque, los protocolos de evacuación y la composición sociodemográfica de cada clase.
    <br><br>
    <strong style="font-family:'Playfair Display',serif;font-size:1.15rem;color:#d4aa50;">Rentabilidad de la operación</strong><br><br>
    Del total de <strong>£ {tot_gbp:,.0f}</strong> recaudados según el archivo,
    la clase que mayor aporte realizó fue <strong>{topc['Clase']}</strong>, con <strong>£ {topc['Tarifa_total_gbp']:,.0f}</strong>
    ({topc['% del total']:.1f}% del total). Frente al costo operativo de <strong>£ {op_cost_gbp:,.0f}</strong>,
    el viaje habría generado una <strong>{rg}</strong> de <strong style="color:{cg}">£ {abs(gan_gbp):,.0f}</strong> en 1912,
    equivalente a <strong style="color:{cg}">£ {abs(gan_2025):,.0f}</strong> en valores de 2025 (factor ×{inflation_factor:.0f}).
    </div>""", unsafe_allow_html=True)

    reflexion = (
        "El presente análisis busca ir más allá de una simple descripción de la distribución de los pasajeros "
        "a bordo del Titanic en 1912, con el propósito de comprender cómo el mercado de transporte marítimo "
        "transatlántico estaba estructurado estratégicamente en clases y así identificar qué segmento generaba "
        "un mayor retorno económico. Los resultados evidencian que la primera clase no solo aportaba el mayor "
        "ingreso por pasajero —con tarifas significativamente superiores a las de segunda y tercera clase—, "
        "sino que también constituía un segmento clave para que la White Star Line pudiera financiar, justificar "
        "y rentabilizar la operación de buques de gran escala. En este sentido, analizar la composición de "
        "ingresos del Titanic permite establecer un paralelismo con las operaciones actuales de transporte "
        "internacional, donde resulta fundamental comprender quién paga y cuánto para determinar la "
        "sostenibilidad del modelo de negocio. Adicionalmente, el análisis de los datos permitió identificar "
        "una relación directa entre el acceso a una clase superior y una mayor probabilidad de supervivencia, "
        "según la información contenida en la base de datos proporcionada. Finalmente, el uso de herramientas "
        "de inteligencia artificial facilitó la obtención de información complementaria, como el costo estimado "
        "de operación del buque en la época y la ruta planificada, enriqueciendo el contexto y fortaleciendo "
        "la interpretación de los resultados."
    )
    st.markdown(f'<div class="insight-box"><strong>📌 Reflexión del estudiante:</strong><br><br>{reflexion}</div>', unsafe_allow_html=True)

    st.markdown('<p class="section-header">Fuentes y referencias</p>', unsafe_allow_html=True)
    st.markdown("""
    | Fuente | Descripción | Enlace |
    |--------|-------------|--------|
    | Encyclopedia Titanica | Información histórica por pasajero | [encyclopedia-titanica.org](https://www.encyclopedia-titanica.org) |
    | National Archives UK | Vida a bordo del Titanic | [nationalarchives.gov.uk](https://www.nationalarchives.gov.uk/education/resources/life-aboard-titanic/) |
    | Bank of England | Calculadora de inflación histórica | [bankofengland.co.uk](https://www.bankofengland.co.uk/monetary-policy/inflation/inflation-calculator) |
    | MeasuringWorth | Tasas históricas de cambio | [measuringworth.com](https://www.measuringworth.com/datasets/exchangepound/) |
    """)

    st.markdown('<p class="section-header">📥 Exportar Reporte</p>', unsafe_allow_html=True)

    def gen_html():
        crt = surv_table(df,["Clase","Pclass"]).sort_values("Pclass")
        rows_comp = "".join(f"<tr><td>{r['Clase']}</td><td>{int(r['Pasajeros'])}</td><td>{r['% del total']}</td><td>{int(r['Sobrevivientes'])}</td><td>{r['Tasa superv.']}</td><td>£ {r['Tarifa prom. (£)']:.2f}</td></tr>" for _,r in comp.iterrows())
        rows_surv = "".join(f"<tr><td>{r['Clase']}</td><td>{int(r['Pasajeros'])}</td><td>{int(r['Sobrevivientes'])}</td><td><strong>{r['Probabilidad supervivencia']*100:.1f}%</strong></td><td>£ {r['Tarifa_promedio']:.2f}</td></tr>" for _,r in crt.iterrows())
        rows_fin  = "".join(f"<tr><td>{r['Clase']}</td><td>{int(r['Pasajeros'])}</td><td>£ {r['Tarifa_total_gbp']:,.0f}</td><td>{r['% del total']:.1f}%</td><td style='color:{'#6aeea0' if r['Cobertura (%)']>=100 else '#f09878'};font-weight:700'>{r['Cobertura (%)']:.1f}%</td><td>£ {r['Equiv. £ 2025']:,}</td></tr>" for _,r in fare_cls.iterrows())
        return f"""<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>RMS Titanic · Reporte</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Source+Sans+3:wght@300;400;600&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Source Sans 3',sans-serif;background:linear-gradient(160deg,#0c1e38,#0f2848,#122f54);color:#e8f2fc;min-height:100vh}}
.cover{{background:linear-gradient(160deg,#061220,#0a1e3a,#112540);border-bottom:2px solid #c8a84b;padding:52px 56px 48px;position:relative;overflow:hidden}}
.cover::before{{content:'';position:absolute;inset:0;background:radial-gradient(ellipse at 60% 100%,rgba(200,168,50,.1),transparent 65%)}}
.ci{{display:flex;align-items:center;gap:52px;position:relative;z-index:1}}
.cs{{flex:0 0 auto}}.cd{{flex:1}}
.rms{{font-size:.82rem;color:#c8a84b;letter-spacing:6px;text-transform:uppercase;margin-bottom:4px}}
.ct{{font-family:'Playfair Display',serif;font-size:3.8rem;font-weight:900;color:#f5ecd5;letter-spacing:2px;text-shadow:0 2px 28px rgba(180,140,40,.5);line-height:1.05;margin:0 0 10px}}
.csub{{font-size:1rem;color:#d0e8f8;line-height:1.5;margin-bottom:18px}}
.cgl{{height:2px;width:75%;background:linear-gradient(90deg,#c8a84b,rgba(200,168,75,.15));margin:16px 0}}
.cul{{font-size:.72rem;color:#a0bcd0;text-transform:uppercase;letter-spacing:2px;margin-bottom:3px}}
.cun{{font-family:'Playfair Display',serif;font-size:1.25rem;color:#f0dc9c;font-weight:700;margin-bottom:3px}}
.cus{{font-size:1.05rem;color:#c8e4f8;margin-bottom:2px}}
.cuc{{font-size:.88rem;color:#90b8d0;font-style:italic;margin-bottom:14px}}
.cm{{font-size:.8rem;color:#7a9ab8;margin-top:10px;line-height:1.7}}
.container{{max-width:1000px;margin:0 auto;padding:48px 32px 72px}}
.st{{font-family:'Playfair Display',serif;font-size:1.55rem;color:#f0dc9c;border-left:4px solid #c8a84b;padding-left:14px;margin:40px 0 18px}}
.kg{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:16px;margin-bottom:10px}}
.kc{{background:rgba(255,255,255,.06);border:1px solid rgba(200,168,75,.28);border-radius:12px;padding:20px 16px;text-align:center}}
.kv{{font-family:'Playfair Display',serif;font-size:1.7rem;font-weight:700;color:#e2bb60;line-height:1}}
.kl{{font-size:.72rem;color:#b0c8dc;text-transform:uppercase;letter-spacing:1.5px;margin-top:6px}}
table{{width:100%;border-collapse:collapse;margin-bottom:8px;background:rgba(255,255,255,.03);border-radius:10px;overflow:hidden}}
thead{{background:rgba(200,168,60,.16)}}
thead th{{font-family:'Playfair Display',serif;font-size:.85rem;color:#e2bb60;text-transform:uppercase;letter-spacing:1px;padding:13px 14px;text-align:left;border-bottom:1px solid rgba(200,168,80,.3)}}
tbody tr{{border-bottom:1px solid rgba(255,255,255,.07)}}
tbody tr:last-child{{border-bottom:none}}
tbody td{{padding:12px 14px;font-size:.95rem;color:#dceef8}}
.ib{{background:rgba(200,168,60,.1);border:1px solid rgba(200,168,60,.25);border-left:4px solid #c8a84b;border-radius:8px;padding:18px 22px;margin:16px 0;font-size:.97rem;line-height:1.78;color:#e4eff8}}
.cb{{background:linear-gradient(135deg,rgba(20,60,110,.5),rgba(10,28,60,.7));border:1px solid rgba(200,168,80,.32);border-radius:14px;padding:28px 30px;margin:18px 0;line-height:1.88;color:#e8f2fc}}
.cb h3{{font-family:'Playfair Display',serif;font-size:1.1rem;color:#e2bb60;margin-bottom:12px}}
.nb{{background:rgba(255,255,255,.06);border:1px solid rgba(140,180,210,.25);border-radius:8px;padding:12px 16px;font-size:.83rem;color:#a8c8dc;font-style:italic;margin-top:10px}}
.bb{{display:flex;align-items:stretch;border-radius:10px;overflow:hidden;height:48px;margin:18px 0;border:1px solid rgba(200,168,80,.22)}}
.bc{{background:rgba(240,112,80,.22);display:flex;align-items:center;justify-content:center;font-size:.82rem;color:#f09878;font-weight:600;padding:0 12px}}
.bp{{background:rgba(100,240,160,.16);display:flex;align-items:center;justify-content:center;font-size:.82rem;color:#6aeea0;font-weight:600;padding:0 12px;flex:1}}
.sl{{list-style:none;display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-top:10px}}
.sl li{{background:rgba(255,255,255,.05);border:1px solid rgba(200,168,80,.18);border-radius:8px;padding:12px 14px;font-size:.85rem;color:#c8e0f0}}
.sl a{{color:#7ab8e8;text-decoration:none}}.sn{{color:#e2bb60;font-weight:600;font-size:.9rem}}
.footer{{text-align:center;padding:28px;border-top:1px solid rgba(200,168,80,.2);font-size:.8rem;color:#6a8aaa;margin-top:40px}}
</style></head><body>
<div class="cover"><div class="ci">
  <div class="cs">{SHIP_TAG}</div>
  <div class="cd">
    <div class="rms">R · M · S</div>
    <div class="ct">Titanic</div>
    <div class="csub">Análisis de Supervivencia · Estructura de Clase · Rentabilidad del Viaje</div>
    <div class="cgl"></div>
    <div class="cul">Trabajo · Entrega Final</div>
    <div class="cun">Politécnico Gran Colombiano</div>
    <div class="cus">👩‍🎓 Sara Santillana</div>
    <div class="cuc">Análisis y Visualización de Datos</div>
    <div class="cm">Generado el {pd.Timestamp.now().strftime('%d de %B de %Y')} &nbsp;·&nbsp; <strong>{total_p:,} registros analizados</strong> &nbsp;·&nbsp; Tasa supervivencia: <strong>{df['Survived'].mean()*100:.1f}%</strong></div>
  </div>
</div></div>
<div class="container">
  <div class="nb">📌 Todos los valores de este reporte se calculan exclusivamente a partir del archivo Excel cargado. No se incorpora información externa al análisis.</div>
  <h2 class="st">Composición del dataset por clase</h2>
  <table><thead><tr><th>Clase</th><th>Pasajeros</th><th>% del total</th><th>Sobrevivientes</th><th>Tasa superv.</th><th>Tarifa prom. (£)</th></tr></thead><tbody>{rows_comp}</tbody></table>
  <h2 class="st">Supervivencia por Clase</h2>
  <table><thead><tr><th>Clase</th><th>Pasajeros</th><th>Sobrevivientes</th><th>Probabilidad</th><th>Tarifa promedio (£)</th></tr></thead><tbody>{rows_surv}</tbody></table>
  <div class="ib">Los pasajeros de <strong>{best['Clase']}</strong> tuvieron la mayor probabilidad de sobrevivir (<strong>{best['Probabilidad supervivencia']*100:.1f}%</strong>), mientras que los de <strong>{wrst['Clase']}</strong> registraron la menor (<strong>{wrst['Probabilidad supervivencia']*100:.1f}%</strong>).</div>
  <h2 class="st">Análisis de Rentabilidad (£ 1912 y £ 2025)</h2>
  <div class="kg">
    <div class="kc"><div class="kv">£ {tot_gbp:,.0f}</div><div class="kl">Recaudado (£ 1912)</div></div>
    <div class="kc"><div class="kv">£ {op_cost_gbp:,.0f}</div><div class="kl">Costo operativo (£ 1912)</div></div>
    <div class="kc"><div class="kv" style="color:{cg}">{sg}£ {abs(gan_gbp):,.0f}</div><div class="kl">{"Ganancia" if gan_gbp>=0 else "Pérdida"} (£ 1912)</div></div>
    <div class="kc"><div class="kv">£ {tot_2025:,.0f}</div><div class="kl">Recaudado equiv. (£ 2025)</div></div>
    <div class="kc"><div class="kv">£ {op_2025:,.0f}</div><div class="kl">Costo equiv. (£ 2025)</div></div>
    <div class="kc"><div class="kv" style="color:{cg}">{sg}£ {abs(gan_2025):,.0f}</div><div class="kl">{"Ganancia" if gan_gbp>=0 else "Pérdida"} (£ 2025)</div></div>
  </div>
  <div class="bb"><div class="bc" style="width:{min(op_cost_gbp/tot_gbp*100,95):.1f}%">Costo £ {op_cost_gbp:,.0f}</div><div class="bp">{"Ganancia" if gan_gbp>=0 else "Pérdida"}: {sg}£ {abs(gan_gbp):,.0f}</div></div>
  <table><thead><tr><th>Clase</th><th>Pasajeros</th><th>Tarifa total (£ 1912)</th><th>% del total</th><th>Cobertura costo op.</th><th>Equiv. £ 2025</th></tr></thead><tbody>{rows_fin}</tbody></table>
  <h2 class="st">Conclusión e Interpretación</h2>
  <div class="cb">
    <h3>Supervivencia y clase social</h3>
    Según los datos del archivo, los pasajeros de <strong>{best['Clase']}</strong> presentaron la mayor probabilidad de sobrevivir ({best['Probabilidad supervivencia']*100:.1f}%), mientras que los de <strong>{wrst['Clase']}</strong> registraron la menor ({wrst['Probabilidad supervivencia']*100:.1f}%). Esta diferencia refleja la interacción entre clase, ubicación en el buque y protocolos de evacuación.
    <br><br><h3>Rentabilidad de la operación</h3>
    La clase que más contribuyó fue <strong>{topc['Clase']}</strong> con £ {topc['Tarifa_total_gbp']:,.0f} ({topc['% del total']:.1f}% del total). El viaje habría generado una <strong style="color:{cg}">{rg} de £ {abs(gan_gbp):,.0f}</strong> (1912), equivalente a <strong style="color:{cg}">£ {abs(gan_2025):,.0f}</strong> en 2025.
  </div>
  <div class="ib"><strong>📌 Reflexión del estudiante:</strong><br><br>{reflexion}</div>
  <h2 class="st">Fuentes y Referencias</h2>
  <ul class="sl">
    <li><div class="sn">Encyclopedia Titanica</div>Información histórica<br><a href="https://www.encyclopedia-titanica.org" target="_blank">encyclopedia-titanica.org</a></li>
    <li><div class="sn">National Archives UK</div>Vida a bordo<br><a href="https://www.nationalarchives.gov.uk/education/resources/life-aboard-titanic/" target="_blank">nationalarchives.gov.uk</a></li>
    <li><div class="sn">Bank of England</div>Inflación histórica<br><a href="https://www.bankofengland.co.uk/monetary-policy/inflation/inflation-calculator" target="_blank">bankofengland.co.uk</a></li>
    <li><div class="sn">MeasuringWorth</div>Tasas históricas £<br><a href="https://www.measuringworth.com/datasets/exchangepound/" target="_blank">measuringworth.com</a></li>
  </ul>
</div>
<div class="footer">Análisis desarrollado con Python · Streamlit · Pandas · Plotly &nbsp;|&nbsp; Asistido por inteligencia artificial · Perspectiva y criterio: del estudiante &nbsp;|&nbsp; Datos: archivo Excel proporcionado</div>
</body></html>"""

    st.download_button(
        label="⬇️  Descargar Reporte Completo (.html)",
        data=gen_html().encode("utf-8"),
        file_name="titanic_reporte_analisis.html",
        mime="text/html",
        use_container_width=True,
        help="Todos los valores del reporte vienen del archivo Excel cargado."
    )
