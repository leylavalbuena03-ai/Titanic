
# App Streamlit: Análisis Titanic

## Problema inicial
¿Existió alguna relación o ventaja entre pagar más, entendido como viajar en primera clase, y haber sobrevivido al hundimiento del Titanic?

## Módulos
1. Verificación de datos.
2. Análisis visual con gráficas por clase, sexo, edad, puerto y tarifas.
3. Mapa de ruta: Southampton → Cherbourg → Queenstown/Cobh → New York.
4. Conclusión final profesional.

## Cómo ejecutarla localmente

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

Mac/Linux:
```bash
source .venv/bin/activate
```

Instalar dependencias:
```bash
pip install -r requirements.txt
```

Ejecutar:
```bash
streamlit run app.py
```

## Cómo publicarla en Streamlit Community Cloud
1. Crea una cuenta en https://streamlit.io/cloud
2. Sube estos archivos a un repositorio de GitHub:
   - app.py
   - requirements.txt
   - train.xlsx
3. En Streamlit Cloud selecciona "New app".
4. Elige tu repositorio.
5. En "Main file path" escribe:
   - app.py
6. Presiona "Deploy".

## Nota metodológica importante
La variable `Fare` del dataset Titanic suele estar expresada en libras esterlinas históricas. Para comparar con un costo operativo en USD, la app usa una tasa editable de 4.87 USD por £, basada en registros históricos aproximados para 1912.
