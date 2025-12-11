from Model.usuarios_model import UsuariosModel

class UsuariosController:

    @staticmethod
    def obtener_usuarios(id):
        return UsuariosModel.obtener_usuarios(id)

    @staticmethod
    def agregar_usuario(nombre, email, password):
        return UsuariosModel.agregar_usuario(nombre, email, password)

    @staticmethod
    def eliminar_usuario_por_id( user_id):
        return UsuariosModel.eliminar_usuario_por_id(user_id)
    
    @staticmethod
    def modificar(nombre,email,telefono,id):
        return UsuariosModel.modificar(nombre,email,telefono,id)