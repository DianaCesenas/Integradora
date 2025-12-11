# conexionBD.py
import mysql.connector

def obtener_conexion():
    """
    Establece y retorna la conexión a la base de datos MySQL y el cursor.
    Utiliza la configuración local (localhost, root, sin password).
    """
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='', 
            database='bd_reservaciones'
        )
        # Usamos un cursor con 'buffered=True' para evitar problemas con múltiples resultados.
        cursor = conexion.cursor(buffered=True) 
        print("✅ Conexión con 'bd_reservaciones' establecida correctamente.")
        return conexion, cursor
    except Exception as e:
        print(f"❌ Error al conectar con la BD: {e}") 
        return None, None