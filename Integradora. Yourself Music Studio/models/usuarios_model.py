from conexionBD2 import obtener_conexion

class UsuariosModel:
    """
    Modelo para manejar la tabla 'usuarios' en la base de datos.
    """

    def obtener_usuarios(self):
        conexion, cursor = obtener_conexion()
        if not conexion:
            return []
        try:
            cursor.execute("SELECT ID, nombre, email FROM usuarios")
            return cursor.fetchall()
        except Exception as e:
            print(f"❌ Error al obtener usuarios: {e}")
            return []
        finally:
            if cursor: cursor.close()
            if conexion: conexion.close()

    def agregar_usuario(self, nombre, email, password):
        # La variable se llama 'password' y se guarda directamente.
        conexion, cursor = obtener_conexion()
        if not conexion:
            return False
        try:
            cursor.execute(
                "INSERT INTO usuarios (nombre, email, password) VALUES (%s,%s,%s)",
                (nombre, email, password) 
            )
            conexion.commit()
            return True
        except Exception as e:
            print(f"❌ Error al agregar usuario: {e}")
            return False
        finally:
            if cursor: cursor.close()
            if conexion: conexion.close()

    # --- MÉTODO CORREGIDO Y MEJORADO PARA ELIMINAR POR ID ---
    
# Archivo: Model/usuarios_model.py

# ... (resto del código) ...

    def eliminar_usuario_por_id(self, user_id: int):
        conexion, cursor = obtener_conexion()
        if not conexion:
            return False
        try:
            # Línea de DEBUG: Imprime el ID que se intenta borrar
            print(f"DEBUG: Intentando eliminar el usuario con ID: {user_id}") 
            
            # --- ASEGÚRATE DE USAR EL NOMBRE DE COLUMNA CORRECTO (ID o id) ---
            cursor.execute("DELETE FROM usuarios WHERE ID=%s", (user_id,)) 
            conexion.commit()
            
            rows_affected = cursor.rowcount 
            
            # Línea de DEBUG: Imprime cuántas filas fueron afectadas
            print(f"DEBUG: Filas afectadas por la eliminación: {rows_affected}")
            
            return rows_affected > 0
            
        except Exception as e:
            print(f"❌ Error al eliminar usuario por ID: {e}")
            return False
        finally:
            if cursor: cursor.close()
            if conexion: conexion.close()


