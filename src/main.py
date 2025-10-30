# ----------------------------- main.py (script principal) -----------------------------
# Importamos nuestras clases “fábrica” y la librería CrewAI.
#   - DataLoader: extrae información de SQL y la devuelve en un DataFrame.
#   - AgentFactory: construye y configura un agente LLM de CrewAI.
#   - TaskFactory: genera un objeto Task con la descripción, el agente y los datos.
#   - Crew       : orquestador que ejecuta uno o varios Task con uno o varios Agent.
from data_loader import DataLoader
from agent_factory import AgentFactory
from task_factory import TaskFactory
from crewai import Crew
import pandas as pd          # Usamos pandas para manipular/leer datos tabulares.

# ------------------------------------------------------------------------------
# (BLOQUE OPCIONAL) ─ CARGA DE DATOS DESDE SQL
# ------------------------------------------------------------------------------
# Si prefieres refrescar la información directamente desde la BD SQL,
# descomenta este bloque.  El DataLoader leerá ‘qry.sql’, ejecutará la consulta
# y guardará el resultado en un .csv para evitar golpear la BD cada vez.

""" query = "..\\data\\qry.sql"                           # Ruta del archivo con la consulta.
extraccion = DataLoader(query)                        # Instancia DataLoader.
df_load = extraccion.load_data_from_sql()             # Ejecuta la consulta y devuelve DataFrame.
df_load.to_csv('..\\data\\data.csv', index=False)     # Persistimos el resultado localmente. """

# ------------------------------------------------------------------------------
# CARGA DEL DATAFRAME DESDE CSV (ruta relativa al proyecto)
# ------------------------------------------------------------------------------
df = pd.read_csv('..\\data\\dataSalud.csv')

# ------------------------------------------------------------------------------
# RESUMEN ESTADÍSTICO DEL DATAFRAME
# ------------------------------------------------------------------------------
# Convertimos el describre() en string para inyectarlo en el prompt del agente.
resumen_datos = df.describe(include='all').to_string()

# ------------------------------------------------------------------------------
# CREACIÓN DEL AGENTE (LLM) MEDIANTE LA FÁBRICA
# ------------------------------------------------------------------------------
#   role        : rol que “interpreta” el LLM.
#   goal        : objetivo principal del agente al resolver tareas.
#   backstory   : contexto o background que alimenta la personalidad del agente.
#   temperature : creatividad/cautela del modelo (0=determinista, 1=creativo).
Agent = AgentFactory(
    role="Analista de Vigilancia en Salud Pública",
    goal="Detectar alertas tempranas en pacientes a partir de datos clínicos y criterios normativos definidos por el Ministerio de Salud, generando recomendaciones para garantizar el cumplimiento oportuno de las actividades de Protección Específica, Detección Temprana y aplicación de las Guías de Atención Integral (GATIS).",
    backstory=(""" 
        Especialista en salud pública con experiencia en análisis normativo, epidemiológico y vigilancia clínica.
        Ha trabajado con EPS e IPS en la implementación de sistemas de información en salud y en el seguimiento al cumplimiento normativo.
        Está entrenado para interpretar resoluciones del Ministerio de Salud y adaptar los análisis de datos clínicos a los anexos técnicos vigentes.
        """),
    temperature=0.1
).create_accounting_agent()   # La fábrica devuelve una instancia crewai.Agent

# ------------------------------------------------------------------------------
# CREACIÓN DEL TASK (tarea específica) MEDIANTE LA FÁBRICA
# ------------------------------------------------------------------------------
# description   : prompt que explica lo que debe hacer el agente.
# agent         : el agente que ejecutará la tarea.
# resumen_datos : input con la estadística descriptiva de las cuentas.
task = TaskFactory(
    description=(
        "Analiza el siguiente resumen de datos clínicos y normativos y responde: "
        "¿Qué alertas tempranas se pueden identificar y qué recomendaciones se deben emitir para mejorar el cumplimiento de las actividades de detección temprana y protección específica?"
            ),
    agent=Agent,
    resumen_datos=resumen_datos,
).create_task()               # Devuelve una instancia crewai.Task

# ------------------------------------------------------------------------------
# CONSTRUCCIÓN Y EJECUCIÓN DEL CREW
# ------------------------------------------------------------------------------
#   agents : lista de agentes que participarán.
#   tasks  : lista (o secuencia) de tareas a resolver.
#   verbose: muestra logs detallados de la ejecución si es True.
crew = Crew(
    agents=[Agent],
    tasks=[task],
    verbose=True
)

# Lanzamos la ejecución secuencial del/los Task con el/los Agent.
resultado = crew.kickoff()

# ------------------------------------------------------------------------------
# SALIDA FINAL EN CONSOLA
# ------------------------------------------------------------------------------
print("\n🧠 Resultado del análisis:\n")
print(resultado)
