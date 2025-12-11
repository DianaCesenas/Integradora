import flet as ft
import re

from Views.Vistas_Base import VistaBase
 
if 'UsuariosController' not in locals():
    class UsuariosController:
        @staticmethod
        def agregar_usuario(n, e, p): return True
        @staticmethod
        def eliminar_usuario_por_id(id): return True

PIN = "123"

class LoginVista(VistaBase):
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.bgcolor = "#FFFFFF"
        # Manejo seguro si no hay datos en client_storage para pruebas
        self.datos_usuario = self.page.session.get("usuario_data") 
        

        # --- PANEL IZQUIERDO ---
        titulo_administracion = ft.Text(
            "Opciones de Administración",
            weight=ft.FontWeight.BOLD, size=16, color="#000000"
        )

        self.nombre_usuario_text = ft.Text(
            f"{self.datos_usuario['nombre']}",
            weight=ft.FontWeight.BOLD, size=18, color="#000000"
        )

        # Botones del menú lateral
        self.boton_editar = ft.ElevatedButton(
            "Editar datos", icon=ft.Icons.EDIT,
            bgcolor="#BBC3CB", color="#2B2B2B", height=40,
            on_click=self.abrir_formulario_edicion,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
        )
        self.boton_agregar = ft.ElevatedButton(
            "Agregar usuario", icon=ft.Icons.PERSON_ADD,
            bgcolor="#BBC3CB", color="#2B2B2B", height=40,
            on_click=self.agregar_usuario_pin,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
        )
        self.boton_eliminar = ft.ElevatedButton(
            "Eliminar usuario", icon=ft.Icons.PERSON_REMOVE,
            bgcolor="#BBC3CB", color="#2B2B2B", height=40,
            on_click=self.eliminar_usuario_pin,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
        )
        self.boton_cerrar = ft.ElevatedButton(
            "Cerrar sesión", icon=ft.Icons.EXIT_TO_APP,
            bgcolor="#BBC3CB", color="#2B2B2B", height=40,
            on_click=self.cerrar_sesion,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
        )

        panel_perfil = ft.Container(
            width=260,
            bgcolor="#FFFFFF",
            padding=20,
            border_radius=10,
            border=ft.border.all(1, "#E0E0E0"),
            content=ft.Column([
                self.nombre_usuario_text,
                ft.Container(height=10), # Pequeña separación
                self.boton_editar,
                ft.Divider(height=30, thickness=1),
                titulo_administracion,
                ft.Container(height=10), # Pequeña separación
                self.boton_agregar,
                self.boton_eliminar,
                ft.Container(height=10),
                self.boton_cerrar
            ], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.STRETCH) 
            # STRETCH hace que los botones ocupen todo el ancho del panel
        )

       
        self.campo_nombre = ft.TextField(
            label="Nombre", 
            value=self.datos_usuario['nombre'], 
            read_only=True, 
            border_color="#E0E0E0", 
            dense=True, # Hace el campo más compacto
            text_size=14,
            label_style=ft.TextStyle(color="#555555"), 
            text_style=ft.TextStyle(color="#000000")
        )
        self.campo_email = ft.TextField(
            label="Email", 
            value=self.datos_usuario['email'], 
            read_only=True, 
            border_color="#E0E0E0", 
            dense=True,
            text_size=14,
            label_style=ft.TextStyle(color="#555555"), 
            text_style=ft.TextStyle(color="#000000")
        )
        self.campo_telefono = ft.TextField(
            label="Teléfono", 
            value=self.datos_usuario['telefono'], 
            read_only=True, 
            border_color="#E0E0E0", 
            dense=True,
            text_size=14,
            label_style=ft.TextStyle(color="#555555"), 
            text_style=ft.TextStyle(color="#000000")
        )

        panel_info = ft.Container(
            expand=True,
            bgcolor="#F9F9F9", # Un gris muy suave de fondo para diferenciar
            padding=30,
            border_radius=10,
            content=ft.Column([
                ft.Text("Información del usuario", weight=ft.FontWeight.BOLD, size=20, color="#000000"),
                ft.Divider(height=20, thickness=1),
                self.campo_nombre,   
                self.campo_email,
                self.campo_telefono
            ], spacing=15, scroll=ft.ScrollMode.AUTO) # Spacing controlado entre campos
        )

        contenido_principal = ft.Container(
            expand=True,
            content=ft.Column([
                ft.Container( # Contenedor para dar margen al contenido principal
                    content=ft.Row(
                        [panel_perfil, panel_info], 
                        expand=True, 
                        vertical_alignment=ft.CrossAxisAlignment.START, 
                        spacing=20
                    ),
                    padding=20,
                    expand=True
                )
            ], spacing=0)
        )

        super().__init__(page, "/perfil", "Perfil", 5, contenido_principal)

    # --- MÉTODOS DE LÓGICA ---

    def abrir_formulario_edicion(self, e):
        self.edit_nombre = ft.TextField(label="Nombre", value=self.datos_usuario['nombre'], dense=True)
        self.edit_email = ft.TextField(label="Email", value=self.datos_usuario['email'], dense=True)
        self.edit_telefono = ft.TextField(label="Teléfono", value=self.datos_usuario['telefono'],
                                          input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]"), max_length=10, dense=True)

        def guardar_cambios_dialog(ev):
            nombre = self.edit_nombre.value.strip()
            email = self.edit_email.value.strip()
            telefono = self.edit_telefono.value

            # Validaciones simples
            if not nombre or not email or not telefono:
                 self.mostrar_alerta("Todos los campos son obligatorios.")
                 return

            self.datos_usuario["nombre"] = nombre
            self.datos_usuario["email"] = email
            self.datos_usuario["telefono"] = telefono

            self.actualizar_campos_vista_principal()
            self.page.close(dialog)
            

        def cerrar_dialog(ev):
            self.page.close(dialog)

        content_dialog = ft.Column([
            self.edit_nombre,
            self.edit_email,
            self.edit_telefono
        ], width=400)

        dialog = ft.AlertDialog(
            title=ft.Text("Editar Datos"),
            content=content_dialog,
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar_dialog),
                ft.ElevatedButton("Guardar", on_click=guardar_cambios_dialog, bgcolor="#43A047", color="white")
            ]
        )
        self.page.open(dialog)

    def actualizar_campos_vista_principal(self):
        self.campo_nombre.value = self.datos_usuario['nombre']
        self.campo_email.value = self.datos_usuario['email']
        self.campo_telefono.value = self.datos_usuario['telefono']
        from Controlador.controlador_usuarios import UsuariosController
        resp=UsuariosController.modificar(self.campo_nombre.value,self.campo_email.value, self.campo_telefono.value,self.datos_usuario['id'])
        if resp:
            self.mostrar_alerta("¡Datos actualizados con éxito!")
            self.campo_nombre.update()
            self.campo_email.update()
            self.campo_telefono.update()
            self.nombre_usuario_text.update() # Actualizamos el texto del nombre
            
            # Si prefieres una opción más genérica que actualice todo en la pantalla:
            # self.page.update()

    def solicitar_pin(self, callback):
        self.pin_field = ft.TextField(label="PIN", password=True, text_align=ft.TextAlign.CENTER, width=100)
        
        def verificar(ev):
            if self.pin_field.value == PIN:
                self.page.close(self.dialogo_pin)
                callback()
            else:
                self.pin_field.error_text = "PIN incorrecto"
                self.pin_field.update()

        self.dialogo_pin = ft.AlertDialog(
            title=ft.Text("Autorización"),
            content=ft.Column([ft.Text("Ingresa tu PIN de admin:"), self.pin_field], tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.page.close(self.dialogo_pin)),
                ft.ElevatedButton("Verificar", on_click=verificar)
            ]
        )
        self.page.open(self.dialogo_pin)

    def mostrar_alerta(self, mensaje):
        snack = ft.SnackBar(ft.Text(mensaje), bgcolor="#333333")
        self.page.open(snack)
        
        

    def agregar_usuario_pin(self, e):
        self.solicitar_pin(self.agregar_usuario)

    def eliminar_usuario_pin(self, e):
        self.solicitar_pin(self.eliminar_usuario_por_id)

    def agregar_usuario(self):
        # Lógica simplificada para el ejemplo
        self.mostrar_alerta("Abriendo diálogo de agregar usuario...")

    def eliminar_usuario_por_id(self):
        # Lógica simplificada para el ejemplo
        self.mostrar_alerta("Abriendo diálogo de eliminar usuario...")

    def cerrar_sesion(self, e):
        self.page.go("/login")

    def recargar_tabla(self):
        # 1. Generamos la nueva estructura visual
        nuevo_contenido = LoginVista()
        
        # 2. Asignamos este contenido a los controles DE LA VISTA (self), no de la page
        self.controls = [nuevo_contenido]
        
        # 3. Actualizamos la página para reflejar los cambios en la vista actual
        self.page.update()    