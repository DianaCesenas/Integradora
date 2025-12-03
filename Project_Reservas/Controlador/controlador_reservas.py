import flet as ft
from conexionBD import *
from Model import reservas_model

class Controlador_Reservas:

    @staticmethod
    def validacionCampos(cliente,id_salas,fecha,hi,ht,personas,id_cliente):
        from Views.VistaGestionReservas import VistaTablaReservas
        if cliente=="":
           VistaTablaReservas.abrir_validacion("Debes seleccionar un cliente")
        elif int(personas)>9:
            VistaTablaReservas.abrir_validacion("La capacidad maxima de la sala es de 9 personas")
        else:
            Controlador_Reservas.agregar(cliente,id_salas,fecha,hi,ht,personas,id_cliente)

    @staticmethod
    def respuestaSQL(titulo,respuesta):
        from Views.VistaGestionReservas import VistaTablaReservas
        if respuesta:
            VistaTablaReservas.accionRealizada(titulo)
        else:
            VistaTablaReservas.accionNoRealizada(titulo)


    @staticmethod
    def agregar(cliente,id_salas,fecha,hi,ht,personas,id_cliente):
        respuesta=reservas_model.ReservasModel.agregar(cliente,id_salas,fecha,hi,ht,personas,id_cliente)
        Controlador_Reservas.respuestaSQL("Agregado",respuesta)

    @staticmethod
    def mostrar():
        registros=reservas_model.ReservasModel.mostrar()
        return registros
        

    @staticmethod
    def modificar(id,cliente,id_salas,fecha,hi,ht,personas,id_cliente):
        respuesta=reservas_model.ReservasModel.modificar(id,cliente,id_salas,fecha,hi,ht,personas,id_cliente)
        Controlador_Reservas.respuestaSQL("Modificado",respuesta)

    @staticmethod
    def desactivar(id):
        respuesta=reservas_model.ReservasModel(id)
        Controlador_Reservas.respuestaSQL("Eliminado",respuesta)

    @staticmethod
    def mostrarSalas():
            return reservas_model.ReservasModel.salas()
    
    @staticmethod
    def mostrarHorasDisponibles():
            return reservas_model.ReservasModel.mostrar_fechas()

     
    @staticmethod
    def mostrarClientes():
        return reservas_model.ReservasModel.mostrar_clientes()