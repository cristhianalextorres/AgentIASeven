import os
import pandas as pd
from sqlalchemy import create_engine
from crewai import Crew, Agent, Task
from langchain_groq import ChatGroq  # Necesitas este wrapper para usar Groq en CrewAI
from dotenv import load_dotenv
import os

load_dotenv()


def load_data_from_sql():
    query = """ 
        SELECT
            cn_salge.SAL_ANOP AS ANNIO
            ,cn_salge.SAL_MESP AS MES
            ,CN_CUENT.CUE_NO01 AS NOMNIVEL1
            ,CN_CUENT.CUE_NO02 AS NOMNIVEL2
            ,CN_CUENT.CUE_NO03 AS NOMNIVEL3
            ,CAST(ROUND(CASE
                WHEN CN_CUENT.CUE_NATU ='D' THEN cn_salge.SCE_VADB - cn_salge.SCE_VACR 
                WHEN CN_CUENT.CUE_NATU ='C' THEN cn_salge.SCE_VACR - cn_salge.SCE_VADB
                ELSE 0 END, 0) AS numeric) AS Saldo
        FROM [Stage].[Seven].[cn_salge]
        INNER JOIN [Stage].[Seven].CN_CUENT ON CN_CUENT.CUE_CONT = cn_salge.CUE_CONT
                                            AND CN_CUENT.EMP_CODI = cn_salge.EMP_CODI
        --WHERE NCU_CODI IN ('1','2','3')
        WHERE NCU_CODI = '1'
    """

    servidor = 'dwbiimp2'
    nombreBD = 'Stage'
    Usuario = 'ServicesBI'
    Pass = 'B1Serv1c3$'
    engine = create_engine(f"mssql+pyodbc://{Usuario}:{Pass}@{servidor}/{nombreBD}?driver=ODBC+Driver+17+for+SQL+Server")

    with engine.connect() as con:
        df = pd.read_sql(query, con)
    
    return df

def main():
    df = load_data_from_sql()

    # Convertimos el DataFrame a un resumen de texto
    resumen_datos = df.describe(include='all').to_string()

    # Inicializar el modelo Groq
    llm = ChatGroq(
        groq_api_key=os.environ["GROQ_API_KEY"],
        temperature=0.7,
        max_completion_tokens=1024,
        top_p=0.9,
        stop=None,
        stream=False,
        model_name="groq/llama-3.3-70b-versatile"
        )

    # Agente contable
    agente = Agent(
        role="Analista contable",
        goal="Responder preguntas sobre los saldos contables usando datos proporcionados",
        backstory="Especialista financiero con experiencia en análisis de datos contables de empresas.",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    #contexto = CrewBaseContext(name="Resumen de datos contables", content=resumen_datos)
    # Tarea
    tarea = Task(
        description="Analiza el siguiente resumen de datos y responde: ¿Elabora una balance y recomienda que oportunidades hay?",
        expected_output=""" Análisis detallado de las cuentas y una respuesta concisa y precisa, por favor usa el siguiente ejemplo como estructura de respuesta:
        Resultado del análisis:

        Para elaborar un balance y recomendar oportunidades, es fundamental analizar detalladamente las cuentas y los datos proporcionados. A continuación, se presentará un análisis detallado de las cuentas y se identificarán oportunidades para mejorar la situación financiera de la empresa.

        **Análisis de las Cuentas**

        1. **Activo**: El activo de la empresa se compone de los siguientes elementos:
        * Caja y Bancos: $100,000
        * Cuentas por Cobrar: $200,000
        * Inventarios: $300,000
        * Propiedades, Planta y Equipo: $500,000
        * Otros Activos: $50,000
        Total Activo: $1,150,000
        2. **Pasivo**: El pasivo de la empresa se compone de los siguientes elementos:
        * Cuentas por Pagar: $150,000
        * Préstamos a Corto Plazo: $200,000
        * Préstamos a Largo Plazo: $300,000
        * Otros Pasivos: $50,000
        Total Pasivo: $700,000
        3. **Patrimonio**: El patrimonio de la empresa se compone de los siguientes elementos:
        * Capital Social: $300,000
        * Reservas: $100,000
        * Utilidades Retenidas: $50,000
        Total Patrimonio: $450,000

        **Balance**

        El balance de la empresa se presenta a continuación:

        | Activo | $1,150,000 |
        | --- | --- |
        | Pasivo | $700,000 |
        | Patrimonio | $450,000 |
        | Total | $1,150,000 |

        **Análisis y Recomendaciones**

        A continuación, se presentan algunas recomendaciones y oportunidades para mejorar la situación financiera de la empresa:

        1. **Gestión de Cuentas por Cobrar**: La empresa tiene un monto significativo de cuentas por cobrar, lo que puede generar problemas de liquidez. Se recomienda implementar un sistema de seguimiento y cobro de cuentas por cobrar para reducir el plazo de cobro y mejorar la liquidez.
        2. **Optimización de Inventarios**: La empresa tiene un monto significativo de inventarios, lo que puede generar costos de almacenamiento y mantenimiento. Se recomienda analizar los niveles de inventarios y optimizarlos para reducir costos y mejorar la eficiencia.
        3. **Inversión en Propiedades, Planta y Equipo**: La empresa tiene un monto significativo de propiedades, planta y equipo, lo que puede generar oportunidades de crecimiento y expansión. Se recomienda analizar las oportunidades de inversión y expansión para mejorar la competitividad y el crecimiento de la empresa.4. **Gestión de Préstamos**: La empresa tiene un monto significativo de préstamos a corto y largo plazo, lo que puede generar costos de intereses y reducir la liquidez. Se recomienda analizar las opciones de refinanciamiento y reestructuración de préstamos para reducir costos y mejorar la liquidez.
        5. **Mejora de la Eficiencia**: La empresa puede mejorar la eficiencia y reducir costos mediante la implementación de procesos y sistemas más eficientes. Se 
        recomienda analizar las oportunidades de mejora de la eficiencia y implementar cambios para mejorar la competitividad y el crecimiento de la empresa.        

        En resumen, la empresa tiene oportunidades para mejorar la situación financiera mediante la gestión de cuentas por cobrar, la optimización de inventarios, la inversión en propiedades, planta y equipo, la gestión de préstamos y la mejora de la eficiencia. Se recomienda analizar y implementar estas recomendaciones 
        para mejorar la competitividad y el crecimiento de la empresa.""",
        agent=agente,
        input=resumen_datos,
        #context=[contexto],
    )

    # Crear Crew
    crew = Crew(
        agents=[agente],
        tasks=[tarea],
        verbose=True
    )

    resultado = crew.kickoff()
    print("\n🧠 Resultado del análisis:\n")
    print(resultado)

if __name__ == "__main__":
    main()
