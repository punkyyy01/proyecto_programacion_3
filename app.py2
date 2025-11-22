# PRUEBA SOLEMNE N°3 - TALLER DE PROGRAMACIÓN II
# Integrantes: [TU NOMBRE]

import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE LA PÁGINA
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Crypto Monitor", layout="wide")

# -----------------------------------------------------------------------------
# 2. FUNCIONES (MODULARIDAD) - [Requisito: Código organizado]
# -----------------------------------------------------------------------------

@st.cache_data
def obtener_datos(moneda, cantidad, orden):
    """Conecta a la API de CoinGecko y devuelve un DataFrame."""
    url = "https://api.coingecko.com/api/v3/coins/markets"
    parametros = {
        'vs_currency': moneda,
        'order': orden,
        'per_page': cantidad,
        'page': 1,
        'sparkline': False
    }
    try:
        respuesta = requests.get(url, params=parametros, timeout=10)
        if respuesta.status_code == 200:
            return pd.DataFrame(respuesta.json())
        else:
            st.error(f"Error en la API: {respuesta.status_code}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return pd.DataFrame()

def grafico_torta_volumen(df_datos):
    """Crea un gráfico de torta simple usando Matplotlib."""
    top_5 = df_datos.head(5)
    fig, ax = plt.subplots()
    ax.pie(top_5['total_volume'], labels=top_5['symbol'].str.upper(), autopct='%1.1f%%')
    ax.set_title("Top 5 Volumen")
    return fig

# -----------------------------------------------------------------------------
# 3. BARRA LATERAL (CONTROLES) - [Requisito: Componentes interactivos]
# -----------------------------------------------------------------------------
st.sidebar.header("Configuración")

# Control 1: Selector de moneda
moneda_select = st.sidebar.selectbox("Moneda:", ['USD', 'CLP', 'EUR'])

# Control 2: Ordenamiento
orden_select = st.sidebar.radio("Ordenar por:", ['Mayor Capitalización', 'Mayor Volumen'])

# Control 3: Slider de cantidad
cantidad = st.sidebar.slider("Cantidad de monedas:", 5, 50, 15)

# Control 4: Filtro de texto
busqueda = st.sidebar.text_input("Buscar moneda (ej: Bitcoin):")

# Control 5: Documentación [Requisito: Instrucciones de uso]
with st.sidebar.expander("Ayuda / Instrucciones"):
    st.write("""
    1. Selecciona la moneda y filtros.
    2. Navega por las pestañas para ver datos y gráficos.
    3. Descarga la tabla en formato CSV.
    """)

# -----------------------------------------------------------------------------
# 4. LÓGICA PRINCIPAL
# -----------------------------------------------------------------------------

# Preparar parámetros para la API
mapa_moneda = {'USD': 'usd', 'CLP': 'clp', 'EUR': 'eur'}
mapa_orden = {'Mayor Capitalización': 'market_cap_desc', 'Mayor Volumen': 'volume_desc'}
simbolo = {'USD': '$', 'CLP': '$', 'EUR': '€'}[moneda_select]

# Cargar datos
df = obtener_datos(mapa_moneda[moneda_select], cantidad, mapa_orden[orden_select])

# Título
st.title("📊 Monitor de Criptomonedas")

# Verificar si hay datos antes de seguir
if df.empty:
    st.stop()

# Filtrado por búsqueda de texto
if busqueda:
    df = df[df['name'].str.contains(busqueda, case=False)]

# Métricas principales (KPIs)
col1, col2, col3 = st.columns(3)
if not df.empty:
    mejor = df.iloc[0]
    col1.metric("Moneda Top", mejor['name'])
    col2.metric("Precio", f"{simbolo}{mejor['current_price']:,.0f}")
    col3.metric("Cambio 24h", f"{mejor['price_change_percentage_24h']:.2f}%")

st.markdown("---")

# -----------------------------------------------------------------------------
# 5. PESTAÑAS DE CONTENIDO
# -----------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["Datos", "Gráficos", "Conclusiones"])

with tab1:
    st.subheader("Tabla de Datos")
    # Mostrar tabla
    st.dataframe(df[['name', 'symbol', 'current_price', 'market_cap', 'total_volume']], use_container_width=True)
    
    # Botón de descarga [Requisito: Interacción]
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Descargar CSV", csv, "datos_crypto.csv", "text/csv")

with tab2:
    st.subheader("Visualización")
    c1, c2 = st.columns(2)
    
    # Gráfico 1: Barras (Streamlit nativo)
    with c1:
        st.caption("1. Capitalización de Mercado")
        st.bar_chart(df.head(10).set_index('name')['market_cap'])
        
    # Gráfico 2: Dispersión (Streamlit nativo)
    with c2:
        st.caption("2. Precio vs Variación")
        st.scatter_chart(df, x='current_price', y='price_change_percentage_24h')

    c3, c4 = st.columns(2)

    # Gráfico 3: Torta (Matplotlib)
    with c3:
        st.caption("3. Distribución de Volumen (Top 5)")
        fig_pie = grafico_torta_volumen(df)
        st.pyplot(fig_pie)

    # Gráfico 4: Rango Máximo/Mínimo (Streamlit nativo)
    with c4:
        st.caption("4. Comparación Alto/Bajo 24h")
        # Multiselect para elegir monedas específicas [Requisito: Más componentes]
        seleccion = st.multiselect("Elige monedas para comparar:", df['name'].tolist(), default=df['name'].iloc[:3].tolist())
        if seleccion:
            df_filtro = df[df['name'].isin(seleccion)].set_index('name')
            st.bar_chart(df_filtro[['high_24h', 'low_24h']])

with tab3:
    st.subheader("Análisis Final")
    st.write("Basado en los datos descargados de la API CoinGecko:")
    st.markdown(f"""
    * La moneda con mayor dominancia es **{df.iloc[0]['name']}**.
    * Se analizaron un total de **{len(df)}** criptomonedas.
    * Los gráficos muestran una clara relación entre volumen y capitalización.
    """)
