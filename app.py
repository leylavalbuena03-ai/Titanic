import streamlit as st

st.title("App funcionando 🚀")
st.write("Si ves esto, el problema no es Streamlit")

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Análisis Titanic | Supervivencia, clase y tarifa",
    page_icon="🚢",
    layout="wide"
)

PORTS = {
    "S": {"name": "Southampton", "country": "Inglaterra", "lat": 50.9097, "lon": -1.4044},
    "C": {"name": "Cherbourg", "country": "Francia", "lat": 49.6337, "lon": -1.6221},
    "Q": {"name": "Queenstown / Cobh", "country": "Irlanda", "lat": 51.8503, "lon": -8.2943},
    "NY": {"name": "New York", "country": "Estados Unidos", "lat": 40.7128, "lon": -74.0060}
}
CLASS_LABELS = {1: "Primera clase", 2: "Segunda clase", 3: "Tercera clase"}
SURVIVAL_LABELS = {0: "No sobrevivió", 1: "Sobrevivió"}

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
    numeric_cols = ["PassengerId", "Survived", "Pclass", "Age", "SibSp", "Parch", "Fare"]
    for col in numeric_cols:
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
    df["Clase"] = df["Pclass"].map(CLASS_LABELS)
    df["Supervivencia"] = df["Survived"].map(SURVIVAL_LABELS)
    df["Puerto"] = df["Embarked"].map(lambda x: f"{x} - {PORTS.get(x, {}).get('name', 'Desconocido')}")
    df["Sexo"] = df["Sex"].map({"male": "Hombre", "female": "Mujer"}).fillna(df["Sex"])
    df["Grupo edad"] = pd.cut(
        df["Age"],
        bins=[-1, 12, 18, 35, 60, 120],
        labels=["Niñez (0-12)", "Adolescencia (13-18)", "Adulto joven (19-35)", "Adulto (36-60)", "Mayor (60+)"]
    )
    return df

def survival_rate_table(df, group_cols):
    out = df.groupby(group_cols, dropna=False).agg(
        Pasajeros=("PassengerId", "count"),
        Sobrevivientes=("Survived", "sum"),
        Tarifa_total=("Fare", "sum"),
        Tarifa_promedio=("Fare", "mean"),
        Edad_promedio=("Age", "mean")
    ).reset_index()
    out["Probabilidad supervivencia"] = out["Sobrevivientes"] / out["Pasajeros"]
    return out

def format_pct(series):
    return (series * 100).round(1).astype(str) + "%"

st.markdown("""
<style>
.main {background-color: #f7f9fc;}
.block-container {padding-top: 2rem;}
.metric-card {
    background: white;
    padding: 1.2rem;
    border-radius: 1.2rem;
    box-shadow: 0 6px 22px rgba(0,0,0,.06);
    border: 1px solid #edf0f5;
}
h1, h2, h3 {letter-spacing: -0.02em;}
.small-note {color:#667085; font-size:.93rem;}
</style>
""", unsafe_allow_html=True)

st.title("🚢 Titanic: relación entre clase, tarifa y supervivencia")
st.caption("Aplicación de análisis exploratorio creada en Streamlit para evaluar si pagar más, especialmente viajar en primera clase, representó una ventaja frente a la supervivencia.")

with st.sidebar:
    st.header("Configuración")
    uploaded = st.file_uploader("Cargar base Titanic en Excel", type=["xlsx", "xls"])
    operation_cost_usd = st.number_input("Costo operativo estimado del trayecto (USD)", min_value=0.0, value=25000.0, step=1000.0)
    gbp_to_usd_1912 = st.number_input("Conversión histórica estimada USD por £", min_value=0.0, value=4.87, step=0.01)
    st.info("La variable Fare del dataset Titanic suele estar expresada en libras esterlinas históricas. Para comparar con USD se usa una conversión editable.")

df = load_data(uploaded)

tabs = st.tabs(["1. Verificación de datos", "2. Análisis visual", "3. Ruta del Titanic", "4. Conclusión final"])

with tabs[0]:
    st.header("Módulo 1: verificación de datos")
    required = ["PassengerId", "Survived", "Pclass", "Name", "Sex", "Age", "Fare", "Embarked"]
    validation = pd.DataFrame({
        "Campo requerido": required,
        "Existe en la base": [col in df.columns for col in required],
        "Valores nulos": [int(df[col].isna().sum()) if col in df.columns else None for col in required],
        "Tipo detectado": [str(df[col].dtype) if col in df.columns else "No existe" for col in required]
    })
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Pasajeros", f"{len(df):,}")
    c2.metric("Supervivencia general", f"{df['Survived'].mean()*100:.1f}%")
    c3.metric("Tarifa total (£)", f"{df['Fare'].sum():,.0f}")
    c4.metric("Edad mediana", f"{df['Age'].median():.1f}")
    st.subheader("Resultado de validación")
    st.dataframe(validation, use_container_width=True)
    st.subheader("Vista previa de datos limpios")
    st.dataframe(df.head(25), use_container_width=True)
    st.subheader("Observaciones automáticas")
    problems = []
    if not all(validation["Existe en la base"]):
        problems.append("Faltan columnas requeridas para el análisis.")
    if df["Survived"].dropna().isin([0,1]).mean() < 1:
        problems.append("La variable Survived contiene valores diferentes de 0 y 1.")
    if df["Pclass"].dropna().isin([1,2,3]).mean() < 1:
        problems.append("La variable Pclass contiene valores fuera de 1, 2 y 3.")
    if df["Embarked"].dropna().isin(["S","C","Q"]).mean() < 1:
        problems.append("La variable Embarked contiene puertos fuera de S, C o Q.")
    if problems:
        for p in problems:
            st.warning(p)
    else:
        st.success("La base está lista para el análisis. El caos humano queda, pero los datos ya obedecen.")

with tabs[1]:
    st.header("Módulo 2: análisis visual")
    st.markdown("### ¿Qué clase tuvo mayor probabilidad de supervivencia?")
    class_rate = survival_rate_table(df, ["Clase", "Pclass"]).sort_values("Pclass")
    fig1 = px.bar(
        class_rate,
        x="Clase",
        y="Probabilidad supervivencia",
        text=format_pct(class_rate["Probabilidad supervivencia"]),
        hover_data=["Pasajeros", "Sobrevivientes", "Tarifa_promedio"],
        title="Probabilidad de supervivencia por clase"
    )
    fig1.update_layout(yaxis_tickformat=".0%", yaxis_title="Probabilidad", xaxis_title="")
    st.plotly_chart(fig1, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        sex_class = survival_rate_table(df, ["Clase", "Pclass", "Sexo"]).sort_values(["Pclass", "Sexo"])
        fig2 = px.bar(
            sex_class, x="Clase", y="Probabilidad supervivencia", color="Sexo",
            barmode="group", text=format_pct(sex_class["Probabilidad supervivencia"]),
            title="Supervivencia por sexo y clase"
        )
        fig2.update_layout(yaxis_tickformat=".0%", yaxis_title="Probabilidad", xaxis_title="")
        st.plotly_chart(fig2, use_container_width=True)
    with col2:
        age_class = survival_rate_table(df, ["Clase", "Pclass", "Grupo edad"]).sort_values(["Pclass", "Grupo edad"])
        fig3 = px.bar(
            age_class, x="Grupo edad", y="Probabilidad supervivencia", color="Clase",
            barmode="group", text=format_pct(age_class["Probabilidad supervivencia"]),
            title="Supervivencia por edad y clase"
        )
        fig3.update_layout(yaxis_tickformat=".0%", yaxis_title="Probabilidad", xaxis_title="")
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("### ¿Qué tipo de pasajero se embarcó por cada puerto?")
    port_class = df.groupby(["Puerto", "Clase", "Pclass"]).size().reset_index(name="Pasajeros").sort_values(["Puerto", "Pclass"])
    fig4 = px.bar(
        port_class, x="Puerto", y="Pasajeros", color="Clase", barmode="group",
        title="Pasajeros por puerto de embarque y clase"
    )
    fig4.update_layout(xaxis_title="", yaxis_title="Pasajeros")
    st.plotly_chart(fig4, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        port_survival = survival_rate_table(df, ["Puerto"])
        fig5 = px.bar(
            port_survival, x="Puerto", y="Probabilidad supervivencia",
            text=format_pct(port_survival["Probabilidad supervivencia"]),
            title="Supervivencia por ciudad/puerto de embarque"
        )
        fig5.update_layout(yaxis_tickformat=".0%", yaxis_title="Probabilidad", xaxis_title="")
        st.plotly_chart(fig5, use_container_width=True)
    with col4:
        fig6 = px.box(
            df, x="Clase", y="Fare", points="outliers",
            title="Distribución de tarifas por clase"
        )
        fig6.update_layout(xaxis_title="", yaxis_title="Tarifa del tiquete (£)")
        st.plotly_chart(fig6, use_container_width=True)

    st.markdown("### ¿Qué clase pagó la mayor parte de la operación estimada?")
    fare_by_class = df.groupby(["Clase", "Pclass"]).agg(Tarifa_total_gbp=("Fare","sum"), Pasajeros=("PassengerId","count")).reset_index().sort_values("Pclass")
    fare_by_class["Tarifa_total_usd_1912"] = fare_by_class["Tarifa_total_gbp"] * gbp_to_usd_1912
    fare_by_class["Participación ingreso"] = fare_by_class["Tarifa_total_usd_1912"] / fare_by_class["Tarifa_total_usd_1912"].sum()
    fare_by_class["Cobertura costo operativo"] = fare_by_class["Tarifa_total_usd_1912"] / operation_cost_usd if operation_cost_usd else np.nan
    fig7 = px.pie(
        fare_by_class, names="Clase", values="Tarifa_total_usd_1912",
        title="Participación estimada por clase en ingresos de tiquetes"
    )
    st.plotly_chart(fig7, use_container_width=True)
    st.dataframe(
        fare_by_class.assign(
            **{
                "Participación ingreso": lambda x: (x["Participación ingreso"]*100).round(1),
                "Cobertura costo operativo": lambda x: (x["Cobertura costo operativo"]*100).round(1)
            }
        ),
        use_container_width=True
    )

with tabs[2]:
    st.header("Mapa de ruta del Titanic")
    route = ["S", "C", "Q", "NY"]
    route_df = pd.DataFrame([{
        "Puerto": PORTS[k]["name"],
        "Código": k,
        "País": PORTS[k]["country"],
        "lat": PORTS[k]["lat"],
        "lon": PORTS[k]["lon"],
        "Orden": i + 1
    } for i, k in enumerate(route)])
    fig_route = go.Figure()
    fig_route.add_trace(go.Scattergeo(
        lon=route_df["lon"], lat=route_df["lat"], mode="lines+markers+text",
        text=route_df["Puerto"], textposition="top center",
        marker=dict(size=10), line=dict(width=3),
        hovertext=route_df["Código"] + " - " + route_df["Puerto"] + ", " + route_df["País"],
        hoverinfo="text"
    ))
    fig_route.update_geos(
        projection_type="natural earth",
        showcountries=True, showland=True, showocean=True,
        fitbounds="locations"
    )
    fig_route.update_layout(
        title="Ruta: Southampton → Cherbourg → Queenstown/Cobh → New York",
        height=620,
        margin=dict(l=0, r=0, t=60, b=0)
    )
    st.plotly_chart(fig_route, use_container_width=True)

with tabs[3]:
    st.header("Módulo 3: conclusión final")
    class_rate = survival_rate_table(df, ["Clase", "Pclass"]).sort_values("Pclass")
    best = class_rate.loc[class_rate["Probabilidad supervivencia"].idxmax()]
    worst = class_rate.loc[class_rate["Probabilidad supervivencia"].idxmin()]
    fare_by_class = df.groupby(["Clase", "Pclass"]).agg(Tarifa_total_gbp=("Fare","sum"), Pasajeros=("PassengerId","count")).reset_index().sort_values("Pclass")
    fare_by_class["Tarifa_total_usd_1912"] = fare_by_class["Tarifa_total_gbp"] * gbp_to_usd_1912
    top_payer = fare_by_class.loc[fare_by_class["Tarifa_total_usd_1912"].idxmax()]
    st.success(
        f"Conclusión: sí se observa una relación clara entre clase/tarifa y supervivencia. "
        f"La mayor probabilidad de supervivencia fue para {best['Clase']} ({best['Probabilidad supervivencia']*100:.1f}%), "
        f"mientras que la menor fue para {worst['Clase']} ({worst['Probabilidad supervivencia']*100:.1f}%)."
    )
    st.markdown(f"""
    **Interpretación profesional:**  
    Los pasajeros de primera clase tuvieron una ventaja observable frente a los pasajeros de segunda y tercera clase.
    Esta diferencia no significa que el dinero haya sido la única causa de supervivencia, porque también influyeron factores como sexo, edad,
    ubicación dentro del buque y protocolos de evacuación. Sin embargo, con esta base de datos, la clase del pasajero aparece como una variable
    fuertemente asociada con la probabilidad de sobrevivir.

    **Resultado financiero estimado:**  
    La clase que más aportó a los ingresos de tiquetes fue **{top_payer['Clase']}**, con un total estimado de
    **USD {top_payer['Tarifa_total_usd_1912']:,.0f}** usando la tasa editable de **{gbp_to_usd_1912} USD por £**.
    Frente a un costo operativo estimado de **USD {operation_cost_usd:,.0f}**, esta clase cubrió aproximadamente
    **{(top_payer['Tarifa_total_usd_1912']/operation_cost_usd*100 if operation_cost_usd else 0):.1f}%** del costo.
    """)
    st.caption("Nota metodológica: este análisis muestra asociación, no causalidad absoluta. Porque incluso los datos tienen más pudor que algunas conclusiones humanas apresuradas.")

    st.subheader("Fuentes y referencias")
    st.markdown("""
    - Kaggle, Titanic dataset: https://www.kaggle.com/c/titanic/data  
    - The National Archives UK, Life aboard the Titanic: https://www.nationalarchives.gov.uk/education/resources/life-aboard-titanic/  
    - MeasuringWorth, tasa histórica dólar/libra: https://www.measuringworth.com/datasets/exchangepound/  
    """)
