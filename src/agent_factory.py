import os
from crewai import Agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv(override=True)

class AgentFactory:
    def __init__(self, role, goal, backstory, temperature):

        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.temperature = temperature

    def create_accounting_agent(self):
        llm = ChatGroq(
            groq_api_key=os.environ["GROQ_API_KEY"],
            temperature = self.temperature,
            max_completion_tokens=1024,
            top_p=0.9,
            stream=False,
            model_name="groq/llama-3.3-70b-versatile"
        )

        agente = Agent(
            role=self.role,
            goal=self.goal,
            backstory=self.backstory,
            verbose=True,
            allow_delegation=False,
            llm=llm
        )
        return agente
