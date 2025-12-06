import flet as ft
from Controlador.controlador_login import ControladorLogin 
from Views.Vistas_Base import VistaBase
# Asumo que importas tu ClaseBase de algún lado, por ejemplo:
# from Vistas.clase_base import ClaseBase

class LoginView(VistaBase): # 1. Hereda de la Clase Base
    def __init__(self, page: ft.Page, on_success_login):
        # Guardamos referencias necesarias antes de generar el contenido
        self.page = page 
        self.on_success_login = on_success_login
        
        # 2. Generamos el contenido encapsulado en un contenedor
        Tabla = self.generalcontenido()

        # 3. Llamamos al constructor de la clase padre con los parámetros solicitados
        # Nota: Asumo que 'ClaseBase' se encarga de añadir 'Tabla' a los controles de la vista.
        super().__init__(page, "/login", "Inicio", 0, Tabla)

    def generalcontenido(self):
        # --- Elementos de la Derecha ---
        self.email_field = ft.TextField(
            label="Email", 
            width=350 
        )
        self.password_field = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            width=350 
        )
        
        # Botón de Login
        login_button = ft.ElevatedButton(
            "Iniciar",
            on_click=self.handle_login_click,
            bgcolor="#A11F1F", 
            color=ft.Colors.WHITE,
            width=100,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
        )
        
        # Contenido del Formulario 
        columna_formulario = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Iniciar sesión", size=24, weight=ft.FontWeight.BOLD),
                    ft.Divider(height=10, color="transparent"),
                    self.email_field,
                    self.password_field,
                    ft.Row(
                        [login_button], 
                        alignment=ft.MainAxisAlignment.END
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.START,
                spacing=20,
            ),
            padding=50,
            expand=True,
            bgcolor=ft.Colors.WHITE
        )

        # --- Elementos de la Izquierda ---
        columna_marca = ft.Container(
            content=ft.Column(
                [
                    ft.Text("SE PARTE", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                    ft.Text("DE LA", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                    ft.Text("MÚSICA", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                    ft.Text(
                        "YOUR\nSELF", 
                        size=60, 
                        weight=ft.FontWeight.W_900, 
                        color=ft.Colors.BLACK,
                        font_family="Roboto Condensed"
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5
            ),
            bgcolor="#A11F1F", 
            expand=True,
            width=250,
            padding=ft.padding.only(top=50, bottom=50)
        )
        
        # --- Contenedor Principal (La "tarjeta" de login) ---
        # Este Row une las dos columnas
        tarjeta_login = ft.Row(
            controls=[
                columna_marca,
                columna_formulario,
            ],
            spacing=0, 
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        # Empaquetamos todo en el Contenedor final (Tabla) con el estilo que tenía la clase original
        contenedor_principal = ft.Container(
            content=tarjeta_login,
            border_radius=15,
            width=600,
            height=450,
            shadow=ft.BoxShadow(blur_radius=15, color="#33000000")
        )

        return contenedor_principal

    # --- Métodos de Lógica (Se mantienen igual) ---

    def _close_dialog(self, e):
        """Cierra el diálogo de alerta."""
        if self.page.dialog: 
            self.page.dialog.open = False
            self.page.update()
    
    def handle_login_click(self, e):
        email = self.email_field.value.strip() 
        password = self.password_field.value
        
        # --- VALIDACIÓN DE CAMPOS VACÍOS EN LA VISTA ---
        if not email or not password:
            alerta_dialogo = ft.AlertDialog(
                modal=True,
                title=ft.Text("⚠️ Datos Faltantes"),
                content=ft.Text("❌ Por favor, ingrese usuario y contraseña."),
                actions=[
                    ft.TextButton(
                        "Aceptar", 
                        on_click=self._close_dialog 
                    ),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=ft.Colors.RED_100,
            )

            self.page.dialog = alerta_dialogo
            alerta_dialogo.open = True
            self.page.update()
            return # Detiene la ejecución
        
        # --- LLAMADA AL CONTROLADOR SI LA VALIDACIÓN ES EXITOSA ---
        resp=ControladorLogin.autenticar(email, password, self.page, self.on_success_login)
        if resp:
            self.page.go("/inicio")
        