# model/operacion_login.py (Modificado: Sin hasheo para que coincida con la BD)
from conexionBD2 import obtener_conexion 
# import hashlib (YA NO ES NECESARIO)

class OperacionesUsuarios:
    """
    Modelo de Operaciones con la tabla 'usuarios'.
    """
    
    @staticmethod
    def iniciar_sesion(email, contrasena):
        """
        Verifica el email y la contraseña (en texto plano) contra la base de datos.
        """
        # 🔑 CAMBIO CLAVE: Eliminamos el hasheo para coincidir con la BD.
        # contrasena_hasheada = hashlib.sha256(contrasena.encode()).hexdigest()
        
        conexion, cursor = obtener_conexion()
        if not conexion: 
            return None # Falla de conexión

        try:
            # 🔑 CAMBIO CLAVE: Se busca el password directamente (contrasena)
            query = "SELECT ID, nombre, email,telefono FROM usuarios WHERE email=%s AND password=%s"
            cursor.execute(query, (email, contrasena))
            
            usuario = cursor.fetchone()
            
            if usuario:
                return usuario
            else:
                return None      
        except Exception as e:
            print(f"❌ Error al iniciar sesión en el modelo: {e}")
            return None
        finally:
            if cursor: cursor.close()
            if conexion: conexion.close()