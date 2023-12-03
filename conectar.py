from config import config
import mysql.connector


def conectar():
    conexion = None
    try:
        params = config()
        print("Estableciendo conexión con la Base de Datos")
        conexion = mysql.connector.connect(**params)

        conexion.autocommit = True

        cursor = conexion.cursor()
        cursor.execute("SELECT version();")
        datos = cursor.fetchone()
        print("La versión de MySQL es", datos[0])
        cursor.close()

    except (Exception, mysql.connector.DatabaseError) as error:
        print(error)

    else:
        print("Conexión exitosa a la Base de Datos")

    finally:
        if conexion is not None:
            return conexion