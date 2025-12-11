import flet as ft
from Model import reservas_model 

class Controlador_Reservas:

    @staticmethod
    def mostrar(texto_busqueda=None, orden=None):
        if texto_busqueda:
            texto_busqueda = texto_busqueda.upper()
        
        return reservas_model.ReservasModel.mostrar(texto_busqueda, orden)

    @staticmethod
    def desactivar(id):
        return reservas_model.ReservasModel.desactivar(id)

    @staticmethod
    def modificar(id, num_personas):
       
        return reservas_model.ReservasModel.modificar(id, num_personas)

     
    @staticmethod
    def agregar_view(fecha,id_sala,id_cliente,horai,horaf,p):
        respuesta=reservas_model.ReservasModel.agregar(fecha,id_sala,id_cliente,horai,horaf,p)
        return respuesta
    
    @staticmethod
    def mostrarSalas():
            return reservas_model.ReservasModel.salas()
    
    @staticmethod
    def mostrarHorasDisponibles(fecha,hora):
            return reservas_model.ReservasModel.mostrar_fechas(fecha,hora)

     
    @staticmethod
    def mostrarClientes():
        return reservas_model.ReservasModel.mostrar_clientes()
    
    @staticmethod
    def datos_inicio1():
        return reservas_model.ReservasModel.datosSala1()
    
    @staticmethod
    def datos_inicio2():
        return reservas_model.ReservasModel.datosSala2()
    
    @staticmethod
    def datos_inicio3():
        return reservas_model.ReservasModel.datosSala3()
    
    @staticmethod
    def datos_inicio4():
        return reservas_model.ReservasModel.datosSala4()
    
    @staticmethod
    def crear_cliente(campo_nombre,campo_apellido,campo_telefono,campo_email,campo_calle,campo_numero,campo_colonia):
        resp=reservas_model.ReservasModel.agregarCliente(campo_nombre,campo_apellido,campo_telefono,campo_email,campo_calle,campo_numero,campo_colonia)
        if resp:
            registro=reservas_model.ReservasModel.buscarCliente(campo_nombre,campo_apellido,campo_telefono)
            return registro