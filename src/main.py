from data_loader import DataLoader
from agent_factory import AgentFactory
from task_factory import TaskFactory
from crewai import Crew
import pandas as pd

"""
query = "..\data\qry.sql"
extraccion = DataLoader(query)
df_load = extraccion.load_data_from_sql()
df_load.to_csv('..\data\data.csv', index=False)
"""

df = pd.read_csv('..\data\data.csv')



resumen_datos = df.describe(include='all').to_string()

Agent = AgentFactory(
    role="Analista contable",
    goal="Responder preguntas sobre los saldos contables usando datos proporcionados",
    backstory="Especialista financiero con experiencia en análisis de datos contables de empresas.",
    temperature= 0.1
).create_accounting_agent()

task = TaskFactory(
    description="Analiza el siguiente resumen de datos y responde: ¿Elabora una balance y recomienda que oportunidades hay?",
    expected_output="Análisis detallado de las cuentas y una respuesta concisa y precisa",
    agent = Agent,
    resumen_datos=resumen_datos,
).create_task()


# Crear Crew
crew = Crew(
    agents=[Agent],
    tasks=[task],
    verbose=True
)

resultado = crew.kickoff()
print("\n🧠 Resultado del análisis:\n")
print(resultado)