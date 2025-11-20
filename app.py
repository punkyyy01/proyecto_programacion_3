# PRUEBA SOLEMNE N°3
# INGE B001 TALLER DE PROGRAMACIÓN II

# --------------------------------------------------- ////// ---------------------------------------------------

import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title='Crypto Dashboard - Solemne 3', layout='wide')

st.title("Dashboard de Criptomonedas")
st.markdown("Aplicación para analizar el mercado actual utilizando la API de CoinGecko.")

# --------------------------------------------------- ////// ---------------------------------------------------

# --- 2. BARRA LATERAL ---
st.sidebar.header("Configuración") # Corregido ortografía
st.sidebar.write("Ajusta los parámetros de la API:")

cantidad_monedas = st.sidebar.slider("Cantidad de monedas a analizar", min_value=5, max_value=50, value=10)

# --------------------------------------------------- ////// ---------------------------------------------------

# --- 3. FUNCIÓN DE DATOS (OPTIMIZADA CON CACHÉ) ---

# Usamos @st.cache_data para no llamar a la API cada vez que tocamos un botón
@st.cache_data
def cargar_datos(cantidad):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': cantidad,
        'page': 1
    }
    try:
        resp = requests.get(url, params=params)
        if resp.status_code == 200:
            return pd.DataFrame(resp.json())
        else:
            st.error(f"Error {resp.status_code} en la API")
            return pd.DataFrame() # Retorna vacío si falla
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return pd.DataFrame()

# Llamamos a la función
df = cargar_datos(cantidad_monedas)

# Verificamos que el df no venga vacío antes de seguir
if df.empty:
    st.warning("No se cargaron datos. Intenta recargar la página.")
    st.stop()
else:
    st.sidebar.success("Datos actualizados correctamente")

# --------------------------------------------------- ////// ---------------------------------------------------

# --- 4. VISUALIZACIÓN Y ANÁLISIS ---

tab1, tab2, tab3 = st.tabs(["Datos Crudos", "Gráficos Interactivos", "Conclusiones"])

# --- PESTAÑA 1: DATOS ---
with tab1:
    st.header("Conjunto de Datos")
    
    if st.checkbox("Mostrar tabla de datos completa", value=True):
        # Configuramos las columnas para que se vean bonitas (formato numérico)
        st.dataframe(
            df[['name', 'symbol', 'current_price', 'market_cap', 'price_change_percentage_24h']],
            column_config={
                "current_price": st.column_config.NumberColumn("Precio (USD)", format="$%.2f"),
                "market_cap": st.column_config.NumberColumn("Market Cap", format="$%d"),
                "price_change_percentage_24h": st.column_config.NumberColumn("Cambio 24h", format="%.2f%%")
            },
            use_container_width=True
        )
    
    col1, col2 = st.columns(2)
    top_coin = df.iloc[0]
    col1.metric("Moneda Top #1", top_coin['name'], f"${top_coin['current_price']:,.2f}")
    col2.metric("Cambio 24h (Top 1)", f"{top_coin['price_change_percentage_24h']:.2f}%")

# --- PESTAÑA 2: GRÁFICOS ---
with tab2:
    st.header("Análisis Visual")

    # --- Gráfico 1
    st.subheader("1. Capitalización de Mercado (Top Monedas)")
    chart_data_cap = df.set_index('name')['market_cap']
    st.bar_chart(chart_data_cap)

    # --- Gráfico 2
    st.subheader("2. Relación Precio vs Variación (24h)")
    st.scatter_chart(df, x='current_price', y='price_change_percentage_24h', color='name')

    st.markdown("---")

    # --- Gráfico 3
    st.subheader("3. Comparación de Precios (High vs Low 24h)")

    moneda_seleccionadas = st.multiselect(
        "Selecciona monedas para comparar sus rangos:",
        df['name'].tolist(),
        default=df['name'].iloc[:3].tolist()
    )

    if moneda_seleccionadas:
        df_filtered = df[df['name'].isin(moneda_seleccionadas)]
        df_char3 = df_filtered[['name', 'high_24h', 'low_24h']].set_index('name')
        
        # ¡FALTABA ESTA LÍNEA! Sin esto, calculabas los datos pero no mostrabas nada.
        st.bar_chart(df_char3) 
    else:
        st.warning("Selecciona al menos una moneda.")
    
    # --- Gráfico 4 (Matplotlib) ---
    st.subheader("4. Distribución de volumen (Top 5)")
    
    if st.checkbox("Mostrar gráfico de torta (Matplotlib)"):
        fig, ax = plt.subplots()
        top5 = df.head(5)
        # Agregué colores y sombra para que se vea menos "plano"
        ax.pie(top5['total_volume'], labels=top5['symbol'].str.upper(), autopct='%1.1f%%', shadow=True, startangle=90)
        ax.axis('equal') # Para que sea un círculo perfecto
        st.pyplot(fig)

# --- PESTAÑA 3: CONCLUSIONES ---
with tab3:
    st.header("Interpretación de Resultados")
    
    # Usamos f-strings para que las conclusiones sean dinámicas según los datos reales
    top_gainer = df.loc[df['price_change_percentage_24h'].idxmax()]
    
    st.markdown(f"""
    **Análisis preliminar:**
    
    1. La moneda con mayor capitalización sigue siendo **{df.iloc[0]['name']}**, lo que indica su dominancia.
    2. La criptomoneda con mejor rendimiento hoy es **{top_gainer['name']}** con un alza de {top_gainer['price_change_percentage_24h']:.2f}%.
    3. Se observa una correlación variable entre precio y volatilidad en el gráfico de dispersión.
    """)
    
    with st.expander("Ver nota técnica"):
        st.info("Los datos son obtenidos en tiempo real mediante la API pública de CoinGecko (Plan Gratuito).")
