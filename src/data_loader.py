import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# ------------------------------------------------------------------------------
#  CARGA LAS VARIABLES DE ENTORNO (.env)
#  -----------------------------------------------------------------------------
#  - override=True permite que, si ya existían variables con el mismo nombre
#    en el entorno de la sesión, sean reemplazadas por las del archivo .env.
# ------------------------------------------------------------------------------
load_dotenv(override=True)


class DataLoader:
    """
    ---------------------------------------------------------------------------
    Clase encargada de extraer datos desde SQL Server y devolverlos en un
    DataFrame de pandas.
    ---------------------------------------------------------------------------
    Atributos
    ----------
    ruta_query : str
        Ruta al archivo .sql que contiene la consulta a ejecutar.

    servidor   : str
    nombre_bd  : str
    usuario    : str
    Pass       : str
        Credenciales para la conexión. Se obtienen de variables de entorno
        con los nombres:
            SERVIDOR_NAME, DB_NAME, USUARIO_NAME, SECRET_KEY
    ---------------------------------------------------------------------------
    Métodos
    -------
    load_data_from_sql()
        Lee el archivo .sql, ejecuta la consulta y devuelve un DataFrame.
    ---------------------------------------------------------------------------
    """

    def __init__(self, ruta_query: str):
        # -----------------------------
        # Almacena la ruta del .sql
        # -----------------------------
        self.ruta_query = ruta_query

        # ----------------------------------------------------------
        # Lee las credenciales / parámetros de conexión del .env
        # ----------------------------------------------------------
        self.servidor = os.getenv('SERVIDOR_NAME')
        self.nombre_bd = os.getenv('DB_NAME')
        self.usuario = os.getenv('USUARIO_NAME')
        self.Pass = os.getenv('SECRET_KEY')

    # --------------------------------------------------------------------------
    # MÉTODO PRINCIPAL DE EXTRACCIÓN
    # --------------------------------------------------------------------------
    def load_data_from_sql(self) -> pd.DataFrame:
        """
        Ejecuta la consulta SQL almacenada en `ruta_query` y devuelve el
        resultado como DataFrame de pandas.

        Returns
        -------
        pd.DataFrame
            Datos obtenidos de la base de datos.
        """

        # ------------------------------------------------------------
        # 1. Leer la consulta SQL desde archivo de texto
        # ------------------------------------------------------------
        with open(self.ruta_query, 'r', encoding='utf-8') as archivo:
            query = archivo.read()

        # ------------------------------------------------------------
        # 2. Construir la cadena de conexión con SQLAlchemy + pyodbc
        #    - Driver 17 for SQL Server
        #    - Formato: mssql+pyodbc://USUARIO:PASSWORD@SERVIDOR/BD?driver=...
        # ------------------------------------------------------------
        cadena_conexion = (
            f"mssql+pyodbc://{self.usuario}:{self.Pass}"
            f"@{self.servidor}/{self.nombre_bd}?driver=ODBC+Driver+17+for+SQL+Server"
        )

        # ------------------------------------------------------------
        # 3. Crear el engine; abrir una conexión de contexto
        #    para ejecutar la consulta y cargar el resultado
        #    directo a un DataFrame.
        # ------------------------------------------------------------
        engine = create_engine(cadena_conexion)
        with engine.connect() as conexion:
            df = pd.read_sql(query, conexion)

        # ------------------------------------------------------------
        # 4. Devolver los datos
        # ------------------------------------------------------------
        return df
