from Model import operaciones 
# Ya no necesitamos 'import flet as ft' aquí

class Controlador:
    # Aceptar 4 argumentos para coincidir con la llamada en vista_tabla.py y manejar la recarga
    @staticmethod
    def agregar(nombre, capacidad, page, callback_reload): 
        respuesta = operaciones.OperacionesSalas.insertar(nombre, capacidad)
        if respuesta:
            callback_reload(None) 
        return respuesta 

    @staticmethod
    def mostrar(texto_busqueda=None, orden=None): 
        if texto_busqueda:
            texto_busqueda = texto_busqueda.upper() 
        return operaciones.OperacionesSalas.consultar(texto_busqueda, orden)

    @staticmethod
    def modificar(id_sala, nombre, capacidad, page, callback_reload): 
        respuesta = operaciones.OperacionesSalas.actualizar(id_sala, nombre, capacidad)
        if respuesta:
            callback_reload(None) # Ejecuta el callback solo si la operación BD fue exitosa
        return respuesta 

    # Aceptar 3 argumentos para coincidir con la llamada en vista_tabla.py (id_sala, page, callback_reload)
    @staticmethod
    def eliminar(id_sala, page, callback_reload):
        respuesta = operaciones.OperacionesSalas.eliminar(id_sala)
        if respuesta:
            callback_reload(None) # Ejecuta el callback solo si la operación BD fue exitosa
        return respuesta
    
    

     
    
    