import flet as ft
# Asumo que estos imports funcionan en tu proyecto
from Controlador.controlador_login import ControladorLogin 
# from Views.Vistas_Base import VistaBase # No parece que lo estés usando aquí, pero lo dejo comentado

class LoginView(ft.View): 
    def __init__(self, page: ft.Page, on_success_login):
        # Guardamos referencias propias (esto está bien)
        self.page = page 
        self.on_success_login = on_success_login
        
        # Generamos el contenido principal
        contenido_principal = self.generalcontenido()
        
        super().__init__(
            route="/login",  # 1. La ruta de esta vista
            controls=[contenido_principal], # 2. Los controles deben ir en una LISTA
            vertical_alignment=ft.MainAxisAlignment.CENTER, # 3. Centra la tarjeta verticalmente
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, # 4. Centra la tarjeta horizontalmente
            padding=0,
            bgcolor="#F2F2F2" # Opcional: un color de fondo para la pantalla completa
        )

    def generalcontenido(self):
        # --- SECCIÓN IZQUIERDA (IMAGEN DESDE ASSETS) ---
        columna_marca = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Image(
                        src="logo2.png", 
                        width=600, 
                        height=300,
                        fit=ft.ImageFit.CONTAIN,
                        error_content=ft.Text("¿Configuraste assets_dir?", color=ft.Colors.WHITE) 
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            ),
            bgcolor="#992626", 
            expand=True,
            width=250, # Ajuste visual sugerido
            padding=ft.padding.all(20)
        )

        # --- SECCIÓN DERECHA (FORMULARIO) ---
        self.email_field = ft.TextField(
            label="Email", 
            width=300, 
            border_color="grey",
            text_style=ft.TextStyle(color="black")
        )
        self.password_field = ft.TextField(
            label="Contraseña", 
            password=True, 
            can_reveal_password=True, 
            width=300, 
            border_color="grey",
            text_style=ft.TextStyle(color="black")
        )
        
        login_button = ft.ElevatedButton(
            "Iniciar",
            on_click=self.handle_login_click,
            bgcolor="#A11F1F", 
            color=ft.Colors.WHITE,
            width=120,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
        )

        columna_formulario = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Iniciar sesión", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                    ft.Divider(height=10, color="transparent"),
                    self.email_field,
                    self.password_field,
                    ft.Row([login_button], alignment=ft.MainAxisAlignment.END),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.START,
                spacing=20,
            ),
            padding=40,
            expand=True,
            bgcolor=ft.Colors.WHITE
        )

        # --- CONTENEDOR PRINCIPAL ---
        tarjeta_login = ft.Row(
            controls=[
                columna_marca,
                columna_formulario,
            ],
            spacing=0, 
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        contenedor_principal = ft.Container(
            content=tarjeta_login,
            border_radius=15,
            width=700,
            height=450,
            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.5, "black")), # Corregí el color shadow para mejor compatibilidad
            bgcolor=ft.Colors.WHITE,
            clip_behavior=ft.ClipBehavior.HARD_EDGE
        )

        return contenedor_principal

    # --- Lógica ---
   # Reemplaza tu método _close_dialog por este:
    def _close_dialog(self, e):
        # Cerramos el diálogo actual
        self.page.close(self.dialogo_actual)

    # Reemplaza tu método handle_login_click por este:
    def handle_login_click(self, e):
        email = self.email_field.value.strip() 
        password = self.password_field.value
        
        if not email or not password:
            self.dialogo_actual = ft.AlertDialog(
                title=ft.Text("⚠️ Datos Faltantes"),
                content=ft.Text("❌ Ingrese usuario y contraseña."),
                actions=[ft.TextButton("Aceptar", on_click=self._close_dialog)],
            )
            self.page.open(self.dialogo_actual)
            return 
        
        user_data = ControladorLogin.autenticar(email, password, self.page, self.on_success_login)
        
        if user_data and len(user_data) > 0:
            self.page.session.set("usuario_data", user_data)
            self.page.go("/inicio")
        else:
            
            self.dialogo_actual = ft.AlertDialog(
                title=ft.Text("⛔ Error de Acceso"),
                content=ft.Text("Usuario o contraseña incorrectos."),
                actions=[ft.TextButton("Intentar de nuevo", on_click=self._close_dialog)],
            )
            self.page.open(self.dialogo_actual)
        
        