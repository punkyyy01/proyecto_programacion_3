


## 3\. Instalación de las Herramientas (Librerías)

Tu código necesita herramientas adicionales (llamadas "librerías") como **Streamlit** (para crear la web), **Pandas** (para manejar los datos) y **Requests** (para conectar con la API).

### A. Abrir la Terminal (o Símbolo del Sistema)

Necesitas usar la línea de comandos de tu computador:

  * **Windows:** Haz clic en el menú Inicio, escribe **`cmd`** y presiona Enter. (Se abrirá una ventana negra).
  * **Mac/Linux:** Busca y abre la aplicación **`Terminal`**.



### B. Instalar las Librerías

Escribe este comando y presiona Enter. Esto instalará todo lo que el programa necesita:

bash:
pip install streamlit pandas requests

 
-----


### Comando de Inicio

Asegúrate de seguir en la carpeta donde tienes `app.py` y escribe:

```bash
streamlit run app.py
```

###  ¡Listo\!

1.  Verás una serie de mensajes en la terminal.
2.  Automáticamente, tu navegador web se abrirá con el título **" Crypto Lab: Análisis de Mercado"** en la dirección `http://localhost:8501`.

### 5\. Uso del Panel

  * **Barra Lateral (Centro de Control):** Usa esta sección para cambiar la divisa (USD, EUR, CLP), el criterio de ordenamiento (Capitalización o Volumen) y cuántas criptomonedas quieres analizar.
  * **Pestañas Centrales:**
      * **Bóveda de Datos:** Muestra la tabla completa y el gráfico de tendencia semanal para cada activo.
      * **Radar Visual:** Contiene los diferentes gráficos (barras, líneas, dispersión) para un análisis visual.
      * **Hallazgos:** Muestra el resumen y las conclusiones automáticas sobre el activo que más subió y el que más bajó en 24 horas.
