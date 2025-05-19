import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv(override=True)

class DataLoader:
    def __init__(self, ruta_query):
        self.ruta_query = ruta_query
        self.servidor = os.getenv('SERVIDOR_NAME')
        self.nombre_bd = os.getenv('DB_NAME')
        self.usuario = os.getenv('USUARIO_NAME')
        self.Pass = os.getenv('SECRET_KEY')


    def load_data_from_sql(self):

        with open(self.ruta_query, 'r', encoding='utf-8') as archivo:
            query = archivo.read()
        # Crear la cadena de conexión segura
        cadena_conexion = (
            f"mssql+pyodbc://{self.usuario}:{self.Pass}"
            f"@{self.servidor}/{self.nombre_bd}?driver=ODBC+Driver+17+for+SQL+Server"
        )

        # Crear el engine y ejecutar la consulta
        engine = create_engine(cadena_conexion)
        with engine.connect() as conexion:
            df = pd.read_sql(query, conexion)

        return df