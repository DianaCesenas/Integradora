import flet as ft

class Interfaz:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Perfil de Usuario"
        self.page.bgcolor = "#F4F5F9"
        self.page.window_width = 900
        self.page.window_height = 650

        self.usuario = {
            "nombre": "Marlene",
            "apellido": "Heredia",
            "email": "marlene@gmail.com",
            "telefono": "1234567890"
        }

        self.etiqueta_nombre = ft.Text(
            f"{self.usuario['nombre']} {self.usuario['apellido']}",
            size=22,
            weight="bold",
            color="black"
        )
        

    def abrir_editar_usuario(self, e):

        self.edit_nombre = ft.TextField(label="Nombre", value=self.usuario["nombre"], width=200)
        self.edit_apellido = ft.TextField(label="Apellido", value=self.usuario["apellido"], width=200)
        self.edit_email = ft.TextField(label="Email", value=self.usuario["email"], width=420)
        self.edit_tel = ft.TextField(label="Teléfono", value=self.usuario["telefono"], width=200)

        def guardar(ev):
            # Limpiar el mensaje de error anterior
            self.mensaje_error.value = ""
            
            # --- VALIDACIÓN 1: Email debe contener "@" ---
            if "@" not in self.edit_email.value:
                self.mensaje_error.value = "introducir @ en el Email"
                self.page.update()
                return # Detiene la ejecución
            
            # --- VALIDACIÓN 2: Teléfono debe contener solo dígitos ---
            if not self.edit_tel.value.isdigit():
                self.mensaje_error.value = "Teléfono: solo números"
                self.page.update()
                return # Detiene la ejecución

            # Si ambas validaciones pasan:
            
            # Actualizar datos del usuario
            self.usuario["nombre"] = self.edit_nombre.value
            self.usuario["apellido"] = self.edit_apellido.value
            self.usuario["email"] = self.edit_email.value
            self.usuario["telefono"] = self.edit_tel.value

            # actualiza el nombre del menu
            self.etiqueta_nombre.value = f"{self.usuario['nombre']} {self.usuario['apellido']}"

            # actualiza el read only
            self.campo_nombre.value = self.usuario["nombre"]
            self.campo_apellido.value = self.usuario["apellido"]
            self.campo_email.value = self.usuario["email"]
            self.campo_tel.value = self.usuario["telefono"]

            self.dialogo.open = False
            self.page.update()

        def cancelar(ev):
            # Limpiar el mensaje de error al cancelar
            self.mensaje_error.value = ""
            self.dialogo.open = False
            self.page.update()

        self.dialogo = ft.AlertDialog(
            title=ft.Text("Editar Perfil"),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.ElevatedButton("Guardar", on_click=guardar),
            ],
            content=ft.Container(
                width=550,
                height=280, 
                padding=10,
                alignment=ft.alignment.center,
                content=ft.Column(
                    [
                        ft.Row([self.edit_nombre, self.edit_apellido]),
                        self.edit_email,
                        self.edit_tel,
                        self.mensaje_error, # Agregar el mensaje de error
                    ],
                    spacing=15,
                    tight=True
                ),
            )
        )

        self.page.open(self.dialogo)

    def mostrar_interfaz(self):

        boton_editar = ft.ElevatedButton(
            "Editar datos",
            icon=ft.Icons.EDIT,
            bgcolor="#A11F1F",
            color="white",
            height=45,
            on_click=self.abrir_editar_usuario
        )

        # FOTO
        foto = ft.Container(
            width=140,
            height=140,
            border_radius=100,
            bgcolor="#CCCCCC",
            alignment=ft.alignment.center,
            content=ft.Text("FOTO")
        )

        self.campo_nombre = ft.TextField(
            label="Nombre",
            value=self.usuario["nombre"],
            read_only=True,
            text_style=ft.TextStyle(color="#555555")
        )

        self.campo_apellido = ft.TextField(
            label="Apellido",
            value=self.usuario["apellido"],
            read_only=True,
            text_style=ft.TextStyle(color="#555555")
        )

        self.campo_email = ft.TextField(
            label="Email",
            value=self.usuario["email"],
            read_only=True,
            text_style=ft.TextStyle(color="#555555")
        )

        self.campo_tel = ft.TextField(
            label="Teléfono",
            value=self.usuario["telefono"],
            read_only=True,
            text_style=ft.TextStyle(color="#555555")
        )

        # menu
        menu_lateral = ft.Container(
            width=250,
            bgcolor="white",
            padding=20,
            border=ft.border.all(1, "#DDDDDD"),
            content=ft.Column(
                [
                    foto,
                    self.etiqueta_nombre,
                    boton_editar,
                ],
                spacing=20,
                horizontal_alignment="center",
                alignment="start"
            )
        )

        # info usuario
        info_usuario = ft.Container(
            padding=30,
            expand=True,
            content=ft.Column(
                [
                    ft.Text(
                        "Información del usuario",
                        size=20,
                        weight="bold",
                        color="black"
                    ),
                    ft.Divider(height=20, color="#999999"),
                    self.campo_nombre,
                    self.campo_apellido,
                    self.campo_email,
                    self.campo_tel,
                ],
                spacing=20
            )
        )

        layout = ft.Row(
            [
                menu_lateral,
                info_usuario
            ],
            expand=True
        )

        self.page.add(layout)


# main
def main(page: ft.Page):
    ui = Interfaz(page)
    ui.mostrar_interfaz()

ft.app(target=main)