# Esta es la conexion a la base de datos utilizando los datos de Funciones/Datos.py

from Funciones.Datos import Host, User, Password, Database
import mysql.connector

def conectar():
    try:
        conexion = mysql.connector.connect(
            host=Host,
            user=User,
            password=Password,
            database=Database
        )
        return conexion
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None