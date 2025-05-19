Proyecto AgentIASeven
Un pipeline end-to-end para extraer datos contables desde SQL Server, analizarlos con CrewAI y entregar un informe financiero generado por IA.

¿Qué hace?

1. Extracción

* DataLoader ejecuta una consulta SQL (almacenada en data/qry.sql) contra la base Stage/Seven usando SQLAlchemy + pyodbc.

* Las credenciales se cargan de forma segura desde un archivo .env.

2. Preparación

* El resultado se guarda opcionalmente en data/data.csv y se resume con pandas.describe() para generar un snapshot estadístico.

3. Generación de agentes

* AgentFactory crea un Analista contable (LLM Groq / Llama-3-70B) con temperatura configurable.

4. Definición de tareas

* TaskFactory construye la tarea: “Elabora un balance y recomienda oportunidades”, inyectando como “plantilla de salida” el archivo data/plantilla.txt.

5. Orquestación

* Crew agrupa agente + tarea y ejecuta crew.kickoff() para producir un informe con:

* Análisis de cifras clave

* Balance formateado

* Recomendaciones y conclusión

***Estructura de carpetas***
AgentIASenven/
│
├── data/
│   ├── qry.sql            # Consulta SQL
│   ├── plantilla.txt      # Formato esperado de respuesta
│   └── data.csv           # Extracto en disco (opcional)
│
├── src/
│   ├── data_loader.py     # Clase DataLoader
│   ├── agent_factory.py   # Clase AgentFactory
│   ├── task_factory.py    # Clase TaskFactory
│   └── main.py            # Punto de entrada
│
├── .env.example           # Variables de entorno necesarias
└── requirements.txt       # Dependencias mínimas


***Instalación rápida***

# 1. Crear entorno (ejemplo con conda)
conda create -n AgentIASeven python=3.11
conda activate AgentIASeven

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables
cp .env.example .env              # Rellena con servidor, usuario, etc.

# 4. Ejecutar
python src/main.py


**Créditos**
Desarrollado por ***CristhianT.*** con ❤️ utilizando:

* CrewAI

* LangChain-Groq

* Pandas • SQLAlchemy • pyodbc • dotenv

