# ----------------------------- agent_factory.py -----------------------------
# Esta clase “fábrica” construye y devuelve un objeto `crewai.Agent`
# listo para ser usado en tareas de CrewAI.  Separamos la lógica de creación
# para centralizar la configuración del LLM y mantener limpio el script principal.

import os
from crewai import Agent                     # Clase Agent de CrewAI.
from langchain_groq import ChatGroq          # Wrapper de Groq para LangChain.
from dotenv import load_dotenv               # Para leer variables de entorno.

# Cargamos las variables de entorno (.env) **con override=True** para que, si el
# usuario las define en la shell, prevalezcan sobre las que haya en el archivo.
load_dotenv(override=True)


class AgentFactory:
    """
    Fábrica de agentes LLM para CrewAI.

    Parameters
    ----------
    role : str
        Rol que el agente 'actuará' (ej. "Analista contable").
    goal : str
        Objetivo o misión principal del agente.
    backstory : str
        Contexto, experiencia o historia que alimenta el prompt del agente.
    temperature : float
        Grado de creatividad del modelo (0 = determinista, 1 = creativo).

    Usage
    -----
    >>> factory = AgentFactory(role="Analista", goal="Responder…", ...)
    >>> accounting_agent = factory.create_accounting_agent()
    """

    def __init__(self, role, goal, backstory, temperature):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.temperature = temperature

    # ------------------------------------------------------------------
    # Método público que crea y devuelve un objeto crewai.Agent
    # ------------------------------------------------------------------
    def create_accounting_agent(self):
        # 1) Instanciamos el LLM Groq con el wrapper de LangChain.
        #    · groq_api_key obligatorio  -> debe estar en variables de entorno.
        #    · temperature              -> heredado del constructor.
        #    · max_completion_tokens    -> límite de tokens de la respuesta.
        #    · model_name               -> modelo Groq a utilizar.
        llm = ChatGroq(
            groq_api_key=os.environ["GROQ_API_KEY"],
            temperature=self.temperature,
            max_completion_tokens=1024,
            top_p=0.9,
            stream=False,
            model_name="groq/llama-3.3-70b-versatile"
        )

        # 2) Creamos el agente CrewAI con el LLM configurado.
        agente = Agent(
            role=self.role,
            goal=self.goal,
            backstory=self.backstory,
            verbose=True,           # Muestra logs detallados durante la ejecución.
            allow_delegation=False, # Impide que el agente cree sub-tareas por su cuenta.
            llm=llm
        )

        # 3) Devolvemos la instancia para usarla en el Crew.
        return agente
