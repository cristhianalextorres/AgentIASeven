# ------------------------------- tasks.py -------------------------------
# Fábrica de objetos `crewai.Task` que encapsulan una *tarea* concreta para
# un agente.  Extraemos la lógica de construcción para no duplicar código y
# centralizar la lectura de la plantilla de salida.

from crewai import Task


class TaskFactory:
    """
    Fábrica que genera un `Task` pre-cargado con su descripción, plantilla
    de respuesta y agente asignado.

    Parameters
    ----------
    description : str
        Instrucción que describe qué debe hacer el agente.
    agent : crewai.Agent
        Agente al que se le asignará la tarea.
    resumen_datos : str
        Texto (habitualmente un resumen estadístico) que se pasa como *input*
        al modelo para que lo analice.

    Usage
    -----
    >>> factory = TaskFactory(description="Analiza…", agent=my_agent, resumen_datos=data)
    >>> task = factory.create_task()
    """

    def __init__(self, description, agent, resumen_datos):
        # Guardamos los parámetros como atributos de instancia
        self.description = description
        self.agent = agent
        self.resumen_datos = resumen_datos

    # ------------------------------------------------------------------
    # Método que construye y devuelve un objeto `Task`
    # ------------------------------------------------------------------
    def create_task(self):
        # 1) Cargamos la plantilla de respuesta desde un archivo de texto.
        #    Esta plantilla se usará como `expected_output`, es decir, el
        #    formato que la salida del agente debería seguir.
        ruta_query = r"..\data\plantilla.txt"   # raw-string para evitar escapes.
        with open(ruta_query, 'r', encoding='utf-8') as archivo:
            plantilla = archivo.read()

        # 2) Construimos y devolvemos el objeto Task.
        #    • description   : prompt que verá el agente.
        #    • expected_output: plantilla con estructura esperada.
        #    • agent         : agente que la ejecutará.
        #    • input         : datos a analizar (string).
        return Task(
            description=self.description,
            expected_output=plantilla,
            agent=self.agent,
            input=self.resumen_datos
        )

        
