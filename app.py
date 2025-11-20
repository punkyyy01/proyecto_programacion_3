# PRUEBA SOLEMNE N°3
# INGE B001 TALLER DE PROGRAMACIÓN II

# --------------------------------------------------- ////// ---------------------------------------------------

import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

# --- 1. CONFIGURACIÓN DE PÁGINA (Componente 1) ---
# Configuracion del titulo de la pestaña del navegador y del diseño ancho
st.set_page_config(page_title='Crypto Dashboard - Solemne 3', layout='wide')

st.title("Dashboard de Criptomonedas")
st.markdown("Aplicación para analizar el mercado acual utilizando la APi de CoinGecko.")

# --------------------------------------------------- ////// ---------------------------------------------------

# --- 2. BARRA LATERAL Y CONFIGURACIÓN ---
st.sidebar.header("Configuracón")
st.sidebar.write("Ajusta los parámetros de la API:")

# Componentes: Slider para definir cuantas monedas descargar
cantidad_monedas = st.sidebar.slider("Cantidad de monedas a analizar", min_value=5, max_value=50, value=10)

# --------------------------------------------------- ////// ---------------------------------------------------

# --- 3. FUNCIÓN DE DATOS (API TEST) ---

# API CoinGecko
url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    'vs_currency': 'usd',
    'order': 'market_cap_desc',
    'per_page': cantidad_monedas, # Usamos el valor del slider
    'page': 1
}

# Manejo de errores
try:
    resp = requests.get(url, params=params)
    if resp.status_code == 200:
        data = resp.json()
        df = pd.DataFrame(data)
        st.sidebar.success("Datos cargados correctamente") # La API cargo correctamente
    else:
        st.error(f"Error al cargar datos. Código: {resp.status_code}")
        st.stop() # Detenemos todo si falla
except Exception as e:
    st.error(f"Error de conexión: {e}")
    st.stop()

# --------------------------------------------------- ////// ---------------------------------------------------

# --- 4. VISUALIZACIÓN Y ANÁLISIS ---

# Creamos pestañas para organizar la información
tab1, tab2, tab3 = st.tabs(["Datos Crudos.", "Gráficos Interactivos", "Conclusiones"])

# --- PESTAÑA 1: DATOS ---
with tab1:
    st.header("Conjunto de Datos")
    # Checkbox para mostrar/ocultar
    if st.checkbox("Mostrar tabla de datos completa", value=True):
        st.dataframe(df[['name', 'symbol', 'current_price', 'market_cap', 'price_change_percentage_24h']])
    
    col1, col2 = st.columns(2)
    top_coin = df.iloc[0]
    col1.metric("Moneda Top #1", top_coin['name'], f"${top_coin['current_price']}")
    col2.metric("Cambio 24h (Top 1)", f"{top_coin['price_change_percentage_24h']}%")

# --- PESTAÑA 2: GRÁFICOS ---
with tab2:
    st.header("Análisis Visual")

    # --- Gráfico 1: Barras (Capitalización de Mercado)
    st.subheader("1. Capitalización de Mercado (Top Monedas)")
    st.caption("Comparación del tamaño de mercado de cada criptomoneda.")
    chart_data_cap = df.set_index('name')['market_cap']
    st.bar_chart(chart_data_cap) # Gráfico interactivo nativo

    # --- Gráfico 2: Scatter (Precio vs Variación)
    st.subheader("2. Relación Precio vs Variación (24h)")
    st.caption("Permite ver si las monedas más caras son más volátiles.")
    st.scatter_chart(df, x='current_price', y='price_change_percentage_24h', color='name')

    # Divisor visual
    st.markdown("---")

    # --- Gráfico 3: Selección dinámica y Gráfico de Líneas
    st.subheader("3. Comparación de Precios (Altos vs Bajos en 24h)")

    # Multiselecter para filtrar gráfico
    moneda_seleccionadas = st.multiselect(
        "Selecciona monedas para comprar sus rangos",
        df['name'].tolist(),
        default=df['name'].iloc[:3].tolist()
    )

    if moneda_seleccionadas:
        df_filtered = df[df['name'].isin(moneda_seleccionadas)]
        # Preparamos datos para gráfico de líneas
        df_char3 = df_filtered[['name', 'high_24h', 'low_24h']].set_index('name')
    else:
        st.warning("Selecciona al menos una moneda.")
    
    # --- Gráfico 3: Gráfico circular (Pie chart) ---
    # Usamos matplotlib 
    st.subheader("4. Distribución de volumen (Top 4)")

    # Radio Button
    opcion_volumen = st.radio("Selecciona visualización", ['Volumen Bruto', 'Porcentaje Relativo'])

    if opcion_volumen:
        fig, ax = plt.subplots() 
        top5 = df.head(5)
        ax.pie(top5['total_volume'], labels=top5['symbol'].str.upper(), autopct='%1.1f%%')
        st.pyplot(fig)

# --- PESTAÑA 3: CONCLUSIONES ---

with tab3:
    st.header("Interpretación de Resultados")

    # Componente 11: Area de Texto (simulada)
    st.markdown("""
    ** Análisis preliminar basado en los datos obtenidos:
    
    1. 
""")
    
    # Info extra
    with st.expander("Ver nota sobre la API"):
        st.info(".")
