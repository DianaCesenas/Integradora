from conexionBD import conexion, cursor

class UsuariosModel:

    @staticmethod
    def obtener_usuarios(id):
        try:
            cursor.execute("SELECT nombre,email,telefono FROM usuarios WHERE ID=%s"),(id,)
            print(cursor.fetchall())
        except Exception as e:
            print(f"❌ Error al obtener usuarios: {e}")
            return []

    @staticmethod
    def agregar_usuario(nombre, email, password):
        try:
            cursor.execute(
                "INSERT INTO usuarios (nombre,apellidos, email,telefono,email, password) VALUES (%s, %s, %s)",
                (nombre, email, password)
            )
            conexion.commit()
            return True
        except Exception as e:
            print(f"❌ Error al agregar usuario: {e}")
            return False

    @staticmethod
    def eliminar_usuario_por_id(id):
        try:
            cursor.execute("DELETE FROM usuarios WHERE ID=%s", (id,))
            conexion.commit()
            return True
        except Exception as e:
            print(f"❌ Error al eliminar usuario: {e}")
            return False

    @staticmethod
    def modificar(nombre,email,telefono,id):
        try:
            cursor.execute("UPDATE usuarios SET  nombre=%s, email=%s,telefono=%s WHERE ID=%s", (nombre,email,telefono,id))
            conexion.commit()
            return True
        except Exception as e:
            print(f"❌ Error al eliminar usuario: {e}")
            return False