# controller/controlador_login.py

import flet as ft
# Importamos el modelo OperacionesUsuarios
from Model.model_login import OperacionesUsuarios 

class ControladorLogin:

    @staticmethod
    def autenticar(email, password, page: ft.Page, callback_success):
        """
        Llama al modelo para iniciar sesión y gestiona la respuesta en la UI de Flet.
        """
        
        # 1. Llamada al Modelo (OperacionesUsuarios)
        registro = OperacionesUsuarios.iniciar_sesion(email, password)
        
        if registro:
            # Si el registro existe: Login Exitoso
            user_id = registro[0]
            user_name = registro[1]
            user_email=registro[2]
            user_telefono=registro[3]
            usuario_data = { "id": user_id,          
            "nombre": user_name,
            "email": user_email, 
            "telefono":user_telefono,  
            "rol": "administrador"}
            
            page.snack_bar = ft.SnackBar(
                ft.Text(f"¡Bienvenido, {user_name}!"),
                open=True,
                bgcolor=ft.Colors.GREEN_700
            )
            page.update()
            
            # 2. Llamar a la función de navegación/éxito proporcionada por main.py
            #callback_success(id_usuario)
            return usuario_data
            
        else:
            # Login Fallido o error de conexión
            page.snack_bar = ft.SnackBar(
                ft.Text("Credenciales incorrectas o error de conexión."),
                open=True,
                bgcolor=ft.Colors.RED_700
            )
            page.update()
            return 0