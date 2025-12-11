import flet as ft
from Views.vista_salas import VistasSalas
from Views.vistaTable import ClienteView
from Views.viewInicio import SalasView
from Views.ususarios import  LoginVista
from Views.vista_login import LoginView
from Views.MainView import VistaReservas
from Views.gestion_reservas import VistasReservas
#from Controlador.controlador_usuarios import UsuariosController
#from Model.usuarios_model import UsuariosModel
from database import Database

def obtener_vista(ruta, page):

    #modelo = UsuariosModel()
    #controlador = UsuariosController(modelo)
    db = Database()
    
    if ruta == "/inicio":
        page.client_storage.clear()
        return SalasView(page)
    if ruta == "/gestion_clientes":
        # MVC Correcto: Instanciamos la VISTA, pasándole la DB si es necesario para que se la pase al controller
        page.client_storage.clear()
        return ClienteView(page, db)
    elif ruta == "/gestion_reservas":
        page.client_storage.clear()
        return   VistasReservas(page)
    elif ruta == "/perfil":
        page.client_storage.clear()
        return LoginVista(page)
    elif ruta == "/salass":
        page.client_storage.clear()
        return  VistasSalas(page)
    elif ruta=="/login":
        page.client_storage.clear()
        return  LoginView(page,None)
    elif ruta=="/reservas":
        return   VistaReservas(page)