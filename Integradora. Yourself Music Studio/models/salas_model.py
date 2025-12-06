from conexionBD import *

class OperacionesSalas:
    
    @staticmethod
    def insertar(nombre, capacidad):
        try:
            cursor.execute(
                "INSERT INTO salas VALUES (NULL, %s, %s)",
                (nombre, capacidad)
            )
            conexion.commit()
            return True
        except:
            return False

    @staticmethod
    # Añadido 'texto_busqueda' para filtrar
    def consultar(texto_busqueda=None):
        try:
            if texto_busqueda:
                # Consulta SQL para buscar solo por nombre
                query = "SELECT * FROM salas WHERE nombre LIKE %s" 
                cursor.execute(query, (f"%{texto_busqueda}%",)) 
            else:
                # Si el texto de búsqueda está vacío, consulta TODOS los registros
                cursor.execute("SELECT * FROM salas")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error en consultar: {e}")
            return []

    @staticmethod
    def actualizar(id_sala, nombre, capacidad):
        try:
            cursor.execute(
                "UPDATE salas SET nombre=%s, capacidad=%s WHERE id=%s",
                (nombre, capacidad, id_sala)
            )
            conexion.commit()
            return True
        except:
            return False

    @staticmethod
    def eliminar(id_sala):
        try:
            cursor.execute("DELETE FROM salas WHERE id=%s", (id_sala,))
            conexion.commit()
            return True
        except:
            return False