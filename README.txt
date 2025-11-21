=====================================================
DASHBOARD DE CRIPTOMONEDAS
=====================================================

--- DESCRIPCIÓN ---

Aplicación web interactiva (Streamlit) que consume la API REST de CoinGecko para mostrar
información actualizada sobre criptomonedas, incluyendo precios, capitalización
de mercado y variaciones en las últimas 24 horas.

--- REQUISITOS ---

* Python: Versión 3.11.x (o superior).
* Librerías: Listadas en el archivo requirements.txt

--- INSTALACIÓN Y CONFIGURACIÓN ---

IMPORTANTE: Todos los comandos a continuación deben ejecutarse en la **TERMINAL**
del sistema o en la Terminal Integrada de **Visual Studio Code (VS Code)**.

1. CREAR ENTORNO VIRTUAL:
   Para aislar las dependencias del proyecto:
   python -m venv venv

2. ACTIVAR ENTORNO VIRTUAL:
   - Windows (PowerShell/CMD): .\venv\Scripts\activate
   - macOS/Linux: source venv/bin/activate
   (En VS Code, a menudo es suficiente con reiniciar la terminal después de crear el venv).

3. INSTALAR DEPENDENCIAS:
   Con el entorno activado, instala las librerías con sus versiones exactas:
   pip install -r requirements.txt
   (se demora unos minutos, ten paciencia)

--- EJECUCIÓN ---

Para iniciar la aplicación:

streamlit run app.py

La aplicación se abrirá automáticamente en tu navegador en http://localhost:8501

--- USO ---

1. Ajusta los parámetros en la barra lateral (moneda base, orden, cantidad).
2. Explora las pestañas ("Datos Crudos", "Gráficos Interactivos", "Conclusiones").

--- API UTILIZADA ---
CoinGecko API (https://www.coingecko.com/api)
- Endpoint: /api/v3/coins/markets
- Método: GET
- Sin necesidad de autenticación
