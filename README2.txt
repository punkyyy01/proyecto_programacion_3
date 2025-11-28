##  Guía Rápida: Cómo Ejecutar el "Crypto Lab"

Este proceso te permite iniciar la aplicación web interactiva que creaste, la cual usa datos en tiempo real de CoinGecko.

### 1\. Preparación Inicial: Guardar el Código

Lo primero es guardar el código de tu aplicación en un archivo.

1.  Abre un programa de edición de texto plano, como el **Bloc de Notas** (Windows), **TextEdit** (Mac), o cualquier editor de código (como VS Code).
2.  Copia y pega **todo el código Python** que me proporcionaste.
3.  Guarda el archivo en una carpeta que puedas encontrar fácilmente (por ejemplo, en el Escritorio) con el nombre: **`app.py`**.

### 2\. Lo que Necesitas: Instalar Python

Tu aplicación está escrita en **Python**. Si no lo tienes, debes instalarlo:

1.  Ve al sitio oficial de Python: [https://www.python.org/downloads/](https://www.python.org/downloads/).
2.  Descarga e instala la última versión de Python para tu sistema operativo (Windows, Mac o Linux).
      * **¡Punto Clave en Windows\!** Durante la instalación, asegúrate de marcar la casilla que dice: **"Add python.exe to PATH"** (Agregar Python al PATH). Esto es fundamental para que los comandos funcionen fácilmente en la terminal.

-----

## 3\. Instalación de las Herramientas (Librerías)

Tu código necesita herramientas adicionales (llamadas "librerías") como **Streamlit** (para crear la web), **Pandas** (para manejar los datos) y **Requests** (para conectar con la API).

### A. Abrir la Terminal (o Símbolo del Sistema)

Necesitas usar la línea de comandos de tu computador:

  * **Windows:** Haz clic en el menú Inicio, escribe **`cmd`** y presiona Enter. (Se abrirá una ventana negra).
  * **Mac/Linux:** Busca y abre la aplicación **`Terminal`**.

### B. Moverte a la Carpeta del Archivo

Debes "moverte" en la terminal a la misma carpeta donde guardaste `app.py`.

  * Usa el comando **`cd`** (Change Directory).
  * **Ejemplo:** Si guardaste `app.py` en el Escritorio, escribe lo siguiente (y presiona Enter):
    ```bash
    cd Escritorio
    ```
    *(Si la carpeta tiene otro nombre, usa ese nombre.)*

### C. Instalar las Librerías

Escribe este comando y presiona Enter. Esto instalará todo lo que el programa necesita:

bash:
pip install streamlit pandas requests

  * **Nota:** Puede tardar un momento en descargarse e instalarse todo. Espera hasta que la terminal muestre un mensaje de éxito y puedas escribir un nuevo comando.

-----

## 4\. Ejecución del "Crypto Lab"

Una vez que las librerías están instaladas, ¡ya puedes iniciar tu aplicación\!

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
