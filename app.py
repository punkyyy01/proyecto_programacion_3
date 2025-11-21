# Importacion de librerias
import streamlit as st
import pandas as pd
import requests
import ast

# -----------------------------------------------------------------------------
# BLOQUE 1: CONFIGURACIÓN DE ENTORNO
# -----------------------------------------------------------------------------
# Inicialización del contexto de la aplicación. Se define el layout 'wide' 
# para maximizar el espacio de visualización de datos tabulares y gráficos.
st.set_page_config(
    page_title='Crypto Lab - Solemne 3', 
    layout='wide',
    initial_sidebar_state="expanded",
    page_icon="💠"
)

st.title("💠 Crypto Lab: Análisis de Mercado")
st.markdown("Entorno de visualización de activos digitales mediante CoinGecko API.")

# -----------------------------------------------------------------------------
# BLOQUE 2: CONTROLES
# -----------------------------------------------------------------------------
st.sidebar.header("🎛️ Centro de Control")

# Captura de parámetros de entrada para el filtrado dinámico del dataset.
moneda_base = st.sidebar.selectbox("Divisa de referencia:", ['USD', 'EUR', 'CLP'], index=0)
tipo_orden = st.sidebar.radio("Criterio de clasificación:", ['Capitalización', 'Volumen'])
cantidad_monedas = st.sidebar.slider("Alcance del análisis (N° monedas)", 5, 50, 10)
filtro_nombre = st.sidebar.text_input("🔭 Rastrear activo específico:")

# Mecanismo de invalidación manual de caché. Permite al usuario forzar 
# una nueva petición HTTP si los datos están obsoletos antes del TTL.
if st.sidebar.button("🔄 Refrescar Datos"):
    st.cache_data.clear()

st.sidebar.markdown("---")
st.sidebar.caption("📡 Datos sincronizados con CoinGecko")

# -----------------------------------------------------------------------------
# BLOQUE 3: LÓGICA DE DATOS Y API
# -----------------------------------------------------------------------------
# Implementación de caché con TTL (Time To Live) de 300 segundos. 
# Esto reduce la latencia y evita el bloqueo por Rate Limiting de la API.
@st.cache_data(ttl=300)
def cargar_datos(cantidad: int, moneda: str, orden: str) -> pd.DataFrame:
    """
    Orquesta la petición de datos. Implementa un patrón 'Fail-Safe':
    si la API falla (especialmente error 429), recurre a un almacenamiento local (CSV)
    para garantizar la continuidad del servicio.
    """
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': moneda.lower(),
        'order': orden,
        'per_page': cantidad,
        'page': 1,
        'sparkline': 'true', 
        'price_change_percentage': '7d'
    }
    archivo_respaldo = "respaldo_seguridad.csv"

    try:
        # Timeout establecido en 10s para evitar bloqueos indefinidos del hilo principal.
        resp = requests.get(url, params=params, timeout=10)
        
        if resp.status_code == 200:
            data = resp.json()
            df_api = pd.DataFrame(data)
            
            # Persistencia de datos exitosos para uso futuro en caso de fallo de red.
            try:
                df_api.to_csv(archivo_respaldo, index=False)
            except:
                pass 
                
            return df_api
            
        elif resp.status_code == 429:
            # Manejo explícito de saturación de API (Rate Limit).
            st.warning("🚧 API saturada (Error 429). Intentando cargar respaldo local...")
            raise Exception("API 429")
        else:
            st.error(f"🚫 Error HTTP {resp.status_code}")
            raise Exception(f"HTTP {resp.status_code}")
            
    except Exception as e:
        # Bloque de recuperación: Carga el dataset local si la conexión falla.
        try:
            df_backup = pd.read_csv(archivo_respaldo)
            st.warning(f"⚠️ Modo Offline: Mostrando datos de respaldo ({archivo_respaldo}) por fallo de conexión.")
            return df_backup
        except FileNotFoundError:
            st.error("💀 Error crítico: API caída y no existe archivo de respaldo local.")
            return pd.DataFrame()

# Mapeo de constantes para normalizar inputs de usuario vs parámetros de API.
moneda_map = {'USD': 'usd', 'EUR': 'eur', 'CLP': 'clp'}
orden_map = {'Capitalización': 'market_cap_desc', 'Volumen': 'volume_desc'}
simbolo_moneda = {'usd': '$', 'eur': '€', 'clp': '$'}[moneda_map[moneda_base]]

with st.spinner('Sincronizando bloques...'):
    df = cargar_datos(cantidad_monedas, moneda_map[moneda_base], orden_map[tipo_orden])

# Validación temprana de estructura de datos para prevenir errores en renderizado posterior.
if df.empty:
    st.warning("☁️ No se pudieron obtener datos. Intenta más tarde.")
    st.stop()

def limpiar_sparkline(row):
    # Deserialización de datos: Al leer desde CSV, las listas se interpretan como strings.
    # ast.literal_eval recupera la estructura de lista original para los gráficos.
    if isinstance(row, str):
        try:
            row = ast.literal_eval(row)
        except:
            return []
            
    if isinstance(row, dict) and 'price' in row:
        return row['price']
    return []

# Aplicación de transformación solo si la columna existe (prevención de KeyError).
if 'sparkline_in_7d' in df.columns:
    df['tendencia_7d'] = df['sparkline_in_7d'].apply(limpiar_sparkline)

# Filtrado local post-fetch para búsquedas específicas por nombre o símbolo.
if filtro_nombre:
    df = df[df['name'].str.contains(filtro_nombre, case=False) | df['symbol'].str.contains(filtro_nombre, case=False)]
    if df.empty:
        st.warning(f"👻 Activo '{filtro_nombre}' no encontrado.")
        st.stop()

# -----------------------------------------------------------------------------
# BLOQUE 4: DASHBOARD KPI
# -----------------------------------------------------------------------------
col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
top_coin = df.iloc[0]

# Indicadores de alto nivel para evaluación rápida del estado del activo principal.
col_kpi1.metric("🚀 Activo Dominante", top_coin['name'])
col_kpi2.metric("💳 Cotización", f"{simbolo_moneda}{top_coin['current_price']:,.2f}")
col_kpi3.metric("🌊 Flujo 24h", f"{top_coin['price_change_percentage_24h']:.2f}%", 
                delta_color="normal" if top_coin['price_change_percentage_24h'] >= 0 else "inverse")

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["🗃️ Bóveda de Datos", "📡 Radar Visual", "🧭 Hallazgos"])

# -----------------------------------------------------------------------------
# PESTAÑA 1: TABLA INTELIGENTE
# -----------------------------------------------------------------------------
with tab1:
    st.subheader("Inventario de Activos en Tiempo Real")
    
    cols_to_show = ['image', 'name', 'symbol', 'current_price', 'market_cap', 'tendencia_7d', 'price_change_percentage_24h']

    # Configuración del DataFrame: Se definen tipos de columnas específicos
    # (ImageColumn, LineChartColumn) para enriquecer la visualización tabular.
    st.dataframe(
        df[cols_to_show],
        column_config={
            "image": st.column_config.ImageColumn("Token"),
            "name": "Nombre",
            "symbol": "Ticker",
            "current_price": st.column_config.NumberColumn(f"Precio ({moneda_base})", format=f"{simbolo_moneda}%.2f"),
            "market_cap": st.column_config.NumberColumn("Capitalización", format=f"{simbolo_moneda}%.0f"),
            "price_change_percentage_24h": st.column_config.NumberColumn("24h %", format="%.2f%%"),
            "tendencia_7d": st.column_config.LineChartColumn(
                "Tendencia (7 Días)",
                y_min=0,
                y_max=None,
                help="Comportamiento gráfico de la última semana"
            )
        },
        use_container_width=True,
        hide_index=True,
        height=500
    )
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("💿 Exportar CSV", csv, 'crypto_data.csv', 'text/csv')

# -----------------------------------------------------------------------------
# PESTAÑA 2: GRÁFICOS (NATIVOS)
# -----------------------------------------------------------------------------
with tab2:
    st.header("Telemétrica de Mercado")

    # Visualización de distribución de capitalización (Top 10).
    st.subheader("1. Dominio de Capitalización Global")
    st.bar_chart(df.head(10).set_index('name')['market_cap'])
    
    st.divider() 

    # Análisis de series temporales para un activo seleccionado.
    st.subheader("2. Cronograma de Precios (Semanal) - Interactivo")
    
    lista_monedas = df['name'].tolist()
    moneda_select = st.selectbox("Selecciona el activo a proyectar:", lista_monedas)
    
    datos_moneda = df[df['name'] == moneda_select].iloc[0]
    precios_historia = datos_moneda['tendencia_7d']

    # Lógica condicional para renderizado del gráfico de líneas.
    # Se define el color de la traza basándose en el delta de rendimiento (Verde/Rojo).
    if len(precios_historia) > 0:
        chart_data = pd.DataFrame(precios_historia, columns=["Precio"])
        color_hex = '#00E676' if precios_historia[-1] >= precios_historia[0] else '#FF1744'
        
        st.line_chart(chart_data, color=color_hex, use_container_width=True)
        
        delta_semanal = ((precios_historia[-1] - precios_historia[0]) / precios_historia[0]) * 100
        st.caption(f"📈 Rendimiento semanal de **{moneda_select}**: {delta_semanal:+.2f}%")
    else:
        st.warning("⚠️ Datos históricos no disponibles para este activo.")

    st.divider()

    # Comparativa de volatilidad intradiaria (High/Low).
    st.subheader("3. Amplitud Térmica (Máx/Mín 24h)")
    monedas_default = df['name'].iloc[:3].tolist()
    seleccion = st.multiselect("Comparativa de volatilidad diaria:", df['name'].tolist(), default=monedas_default)

    if seleccion:
        df_r = df[df['name'].isin(seleccion)].set_index('name')[['low_24h', 'high_24h']]
        df_r = df_r.rename(columns={'low_24h': 'Mínimo', 'high_24h': 'Máximo'})
        st.bar_chart(df_r)

    st.divider()

    # Gráfico de dispersión multidimensional: Precio (X) vs Volumen (Y) vs Market Cap (Tamaño).
    # Permite identificar anomalías de valoración o volumen.
    st.subheader("4. Mapa de Dispersión: Precio vs Volumen")
    st.markdown("Relación entre el valor del activo, su volumen de transacciones y su tamaño de mercado (tamaño de la burbuja).")
    
    df_scatter = df.rename(columns={
        'current_price': f'Precio ({moneda_base})', 
        'total_volume': 'Volumen Total',
        'market_cap': 'Capitalización de Mercado',
        'name': 'Activo'
    })
    
    st.scatter_chart(
        df_scatter,
        x=f'Precio ({moneda_base})',
        y='Volumen Total',
        size='Capitalización de Mercado',
        color='Activo',
        use_container_width=True,
        height=500
    )

# -----------------------------------------------------------------------------
# PESTAÑA 3: INSIGHTS Y CONCLUSIONES
# -----------------------------------------------------------------------------
with tab3:
    st.header("📊 Informe de Análisis y Conclusiones")
    
    # Cálculo dinámico de extremos del dataset (máximo ganador y máximo perdedor).
    st.subheader("1. Hallazgos de Volatilidad (24h)")
    
    mejor = df.loc[df['price_change_percentage_24h'].idxmax()]
    peor = df.loc[df['price_change_percentage_24h'].idxmin()]

    col_res1, col_res2 = st.columns(2)
    
    with col_res1:
        st.success(f"🏆 **Mejor Desempeño:** {mejor['name']}")
        st.metric("Crecimiento", f"+{mejor['price_change_percentage_24h']:.2f}%", delta="Alcista")
        st.caption("El activo con mayor fuerza de compra en el último día.")
    
    with col_res2:
        st.error(f"🥀 **Mayor Corrección:** {peor['name']}")
        st.metric("Retracción", f"{peor['price_change_percentage_24h']:.2f}%", delta="Bajista", delta_color="inverse")
        st.caption("El activo con mayor presión de venta en el último día.")
    
    st.divider()

    st.subheader("2. Interpretación de Datos")
    
    # Generación de texto dinámico basado en los cálculos previos para automatizar el reporte.
    top_coin_name = df.iloc[0]['name']
    dominancia_aprox = (df.iloc[0]['market_cap'] / df['market_cap'].sum()) * 100
    
    st.markdown(f"""
    A partir de la visualización de datos en las pestañas anteriores, se desprenden los siguientes análisis:
    
    * **Concentración de Mercado (Gráfico 1):** Se observa una clara hegemonía de **{top_coin_name}**, la cual representa aproximadamente el **{dominancia_aprox:.1f}%** de la capitalización total de la muestra seleccionada.
        
    * **Correlación Precio-Volumen (Gráfico 4):**
        El **Mapa de Dispersión** permite visualizar anomalías. Activos con burbujas grandes (alta **Capitalización de Mercado**) pero ubicados abajo en el eje Y (bajo **Volumen Total**) indican activos "dormidos", mientras que activos pequeños con alto volumen sugieren alta especulación.
        
    * **Tendencia Semanal (Gráfico 2):**
        Gracias al **gráfico interactivo**, podemos analizar en detalle la evolución de precios de los últimos 7 días, permitiendo identificar soportes y resistencias dinámicas.
    """)

    st.subheader("3. Conclusiones Preliminares")
    
    avg_change = df['price_change_percentage_24h'].mean()
    tendencia_global = "ALCISTA" if avg_change > 0 else "BAJISTA"
    
    st.info(f"""
    **💡 Diagnóstico del Mercado:**
    
    En base a los {cantidad_monedas} activos analizados, el mercado presenta hoy una tendencia general **{tendencia_global}** (promedio de variación del {avg_change:.2f}%).
    
    **Recomendación:** Dada la volatilidad observada en los rangos Máx/Mín (Gráfico 3), se sugiere precaución operar en activos 
    de baja capitalización que muestren divergencias fuertes respecto a la tendencia general del mercado.
    """)
