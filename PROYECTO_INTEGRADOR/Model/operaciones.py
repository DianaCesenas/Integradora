from conexionBD2 import obtener_conexion 

class OperacionesSalas:
    
    @staticmethod
    def insertar(nombre, capacidad):
        conexion, cursor = obtener_conexion()
        if not conexion: return False
        try:
            # Inserta la sala con estatus 1 (Activo)
            cursor.execute(
                "INSERT INTO salas (id, nombre, capacidad, estatus) VALUES (NULL, %s, %s, 1)", 
                (nombre, capacidad)
            )
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error al insertar: {e}")
            if conexion: conexion.rollback()
            return False
        finally:
            if cursor: cursor.close()
            if conexion: conexion.close()

    @staticmethod
    def consultar(texto_busqueda=None, orden=None):
        conexion, cursor = obtener_conexion() # 🔑 CORRECCIÓN: Obtener la conexión y cursor
        if not conexion: return []            # Si falla, retornar lista vacía
        
        try:
            query = "SELECT * FROM salas WHERE estatus = 1"
            params = []
            
            if texto_busqueda:
                query += " AND nombre LIKE %s"
                params.append(f"%{texto_busqueda}%")
            
            # 🔑 IMPLEMENTACIÓN: Aplicar la ordenación alfabética
            if orden == "nombre_asc":
                query += " ORDER BY nombre ASC"
            
            cursor.execute(query, tuple(params))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error en consultar: {e}")
            return []
        finally:
            if cursor: cursor.close() # 🔑 CORRECCIÓN: Cerrar recursos
            if conexion: conexion.close() # 🔑 CORRECCIÓN: Cerrar recursos
            
    @staticmethod
    def actualizar(id_sala, nombre, capacidad):
        conexion, cursor = obtener_conexion()
        if not conexion: return False
        try:
            cursor.execute(
                "UPDATE salas SET nombre=%s, capacidad=%s WHERE id=%s",
                (nombre, capacidad, id_sala)
            )
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar: {e}")
            if conexion: conexion.rollback()
            return False
        finally:
            if cursor: cursor.close()
            if conexion: conexion.close()

    @staticmethod
    def eliminar(id_sala):
        conexion, cursor = obtener_conexion()
        if not conexion: return False
        try:
            # Cambia estatus a 0 (Desactivado/Borrado Lógico)
            cursor.execute("UPDATE salas SET estatus = 0 WHERE id=%s", (id_sala,))
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar: {e}")
            if conexion: conexion.rollback()
            return False
        finally:
            if cursor: cursor.close()
            if conexion: conexion.close()