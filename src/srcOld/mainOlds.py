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
        SELECT [Id]
            ,[IdFileHead4505]
            ,[TypeRegister]
            ,[IdRegister]
            ,[HabilitationCode]
            ,[IdentificationType]
            ,[DocumentNumber]
            ,[FirstLastName]
            ,[SecondLastName]
            ,[FirstName]
            ,[SecondName]
            ,[BirthDate]
            ,[IdSex]
            ,[CodeEthnic]
            ,[OccupationCode]
            ,[CodeEducaLevel]
            ,[Gestation]
            ,[GestaCongeSyphilis]
            ,[ResultTestMiniMentalState]
            ,[CongeHypothyroidism]
            ,[SymptRespiratory]
            ,[TobaccoConsumption]
            ,[Leprosy]
            ,[ObesCaloProtMalnut]
            ,[RectalTouchResult]
            ,[FolicAcidPreconceptional]
            ,[ResultTestingBloodHiddenMateriaFecalScreeningCaColon]
            ,[DiagMentalIllness]
            ,[CervixCancer]
            ,[AcuityVisualFarEyeLeft]
            ,[AcuityVisualFarEyeRight]
            ,[DateWeight]
            ,[WeightKg]
            ,[DateHeight]
            ,[HeightCm]
            ,[DateEstimPartitium]
            ,[CountryCode]
            ,[ClassificationGestationalRisk]
            ,[ResultColonoscopyScreening]
            ,[ResultScreeningHearingNeonatal]
            ,[NeonatalVisualScreeningResult]
            ,[DPTUnderFiveYears]
            ,[ResultScreening]
            ,[Pneumococcus]
            ,[HepatitisCScreeningResult]
            ,[ResultScaleShortenedDevelopmentAreaMotorSkillsThick]
            ,[ResultScaleShortDevelopmentAreaMotorFineadaptative]
            ,[ResultScaleShortenedDevelopmentAreaPersonalSocial]
            ,[ResultScaleShortenedDevelopmentAreaMotorAuditionLanguage]
            ,[TreatmentAblativeExcisionPosterior]
            ,[ResultScreeningOximetryPreyPostDuctal]
            ,[DateAttenPartiCesar]
            ,[ExitDateAttenPartiCesar]
            ,[DateBreastfeeding]
            ,[DateConsultValuationIntegral]
            ,[DateCareHealthCounselingContraception]
            ,[SupplyContracMethod]
            ,[DateContracDelivery]
            ,[DateFirstTimePrenaCtrl]
            ,[GlycemicResult]
            ,[DateLastPrenatalCtrl]
            ,[FolicAcidLastPrenaCtrl]
            ,[FerrSulfLastPrenaCtrl]
            ,[CalciumLastPrenaCtrl]
            ,[DateVisualAssessment]
            ,[DateScreening]
            ,[RectalExamDate]
            ,[DateScreeningOximetryPreyPostDuctal]
            ,[DatePerformedColonoscopyScreening]
            ,[DateTestingBloodHiddenSubjectFecalScreeningCaColon]
            ,[DatePsychologyConsult]
            ,[DateScreeningHearingNeonatal]
            ,[FerrSulfLastConsuUnderTenY]
            ,[VitALastConsuUnderTenY]
            ,[LDLTakenDate]
            ,[DateTakePSA]
            ,[CondomDelivPatientITS]
            ,[NeonatalVisualScreeningDate]
            ,[DateOralHealthCareProfessionalDentistry]
            ,[IronSupplyEarlyChildhood]
            ,[DateHepatitisBAllPopulation]
            ,[ResultHepatitisBAllPopulation]
            ,[SyphilisScreeningTestTakenDate]
            ,[ResultTestScreeningSyphilis]
            ,[DateTakeVIHTest]
            ,[VIHTestResult]
            ,[DateNeonatalTSH]
            ,[ResultNeonatalTSH]
            ,[CervicalCancerScreening]
            ,[DateCervicalCytology]
            ,[ResultCervicalCytology]
            ,[QualityCytologySample]
            ,[HabilitationCodeCytology]
            ,[DateColposcopy]
            ,[LDLResult]
            ,[DateCervicalBiopsy]
            ,[ResultCervicalBiopsy]
            ,[ResultHDL]
            ,[DateMammography]
            ,[ResultMammography]
            ,[ResultTriglycerides]
            ,[DateBreastBiopsyBACAF]
            ,[DateResultBreastBiopsy]
            ,[ResultBiopsyBreast]
            ,[COPPerson]
            ,[DateHemoglobin]
            ,[ResultHemoglobin]
            ,[DateGlycemia]
            ,[DateCreatinine]
            ,[ResultCreatinine]
            ,[DateGlycosylatedHemoglobin]
            ,[PSAResult]
            ,[DateTakenHepatitisCScreening]
            ,[DateHDL]
            ,[DateBacilloscopy]
            ,[ResultBacilloscopy]
            ,[CardiovascularRiskClassification]
            ,[TreatmentGestationalSyphilis]
            ,[TreatmentCongenitalSyphilis]
            ,[MetabolicRiskClassification]
            ,[DateTakeTriglycerides]
            ,[IsConsolidate]
        FROM [Assurance].[dbo].[FileDetail4505]
    """

    servidor = '192.168.1.23'
    nombreBD = 'Assurance'
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
    role="Analista de Vigilancia en Salud Pública",
    goal="Detectar alertas tempranas en pacientes a partir de datos clínicos y criterios normativos definidos por el Ministerio de Salud, generando recomendaciones para garantizar el cumplimiento oportuno de las actividades de Protección Específica, Detección Temprana y aplicación de las Guías de Atención Integral (GATIS).",
    backstory=(""" 
        Especialista en salud pública con experiencia en análisis normativo, epidemiológico y vigilancia clínica.
        Ha trabajado con EPS e IPS en la implementación de sistemas de información en salud y en el seguimiento al cumplimiento normativo.
        Está entrenado para interpretar resoluciones del Ministerio de Salud y adaptar los análisis de datos clínicos a los anexos técnicos vigentes.
        """),
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    #contexto = CrewBaseContext(name="Resumen de datos contables", content=resumen_datos)
    # Tarea
    tarea = Task(
    description=(
        "Analiza el siguiente resumen de datos clínicos y normativos y responde: "
        "¿Qué alertas tempranas se pueden identificar y qué recomendaciones se deben emitir para mejorar el cumplimiento de las actividades de detección temprana y protección específica?"
            ),
        expected_output=""" 🔔 Se ha detectado una alerta temprana según los criterios definidos por el Ministerio de Salud.

            El paciente presenta una condición que requiere seguimiento o intervención prioritaria, conforme a las actividades de Protección Específica, Detección Temprana y las Guías de Atención Integral (GATIS) para enfermedades de interés en salud pública.

            📌 Se recomienda:
            - Verificar el cumplimiento de los protocolos establecidos.
            - Realizar las intervenciones necesarias antes de la fecha límite de reporte.
            - Registrar la información siguiendo el anexo técnico vigente.

            Este hallazgo contribuye al cumplimiento normativo y a la mejora en la calidad de la atención.

            📅 Fecha límite de reporte: [dd/mm/aaaa]

            —
            Agente Inteligente de Vigilancia en Salud Pública """,
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
