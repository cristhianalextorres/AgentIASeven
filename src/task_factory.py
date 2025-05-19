# tasks.py
from crewai import Task

class TaskFactory:

    def __init__(self, description, expected_output,  agent, resumen_datos):
        self.description = description
        self.expected_output = expected_output
        self.agent = agent
        self.resumen_datos = resumen_datos

    def create_task(self):
        return Task(
            description= self.description,
            expected_output=self.expected_output,
            agent=self.agent,
            input=self.resumen_datos
        )
