import flet as ft
#style: remove unnecessary blank lines in view
class MenuView:
    def __init__(self, page, al_clic_cliente, al_clic_instrumento, al_clic_sala, al_clic_reserva):
        self.page = page
        
        self.ir_a_clientes = al_clic_cliente
        self.ir_a_instrumentos = al_clic_instrumento
        self.ir_a_salas = al_clic_sala
        self.ir_a_reservas = al_clic_reserva

    def inicializar(self, contenedor):
        contenedor.controls.clear()
        
        #botones grandes
        def crear_boton(texto, icono, color, accion):
            return ft.Container(
                content=ft.Column([
                    ft.Icon(icono, size=40, color="white"),
                    ft.Text(texto, color="white", weight="bold")
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                width=150, height=150, bgcolor=color, border_radius=15,
                on_click=accion, alignment=ft.alignment.center,
                shadow=ft.BoxShadow(blur_radius=10, color="#1A000000")
            )

        titulo = ft.Text("Yourself Music Studio", size=30, weight="bold", color="#333")
        subtitulo = ft.Text("Sistema de Gestión", size=16, color="grey")

        grid_botones = ft.Row([
            crear_boton("Clientes", ft.Icons.PEOPLE, "#A11F1F", self.ir_a_clientes),
            crear_boton("Instrumentos", ft.Icons.PIANO, "#E67E22", self.ir_a_instrumentos),
            crear_boton("Salas", ft.Icons.MEETING_ROOM, "#3498DB", self.ir_a_salas),
            crear_boton("Reservas", ft.Icons.CALENDAR_MONTH, "#27AE60", self.ir_a_reservas),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20, wrap=True)

        columna_menu = ft.Column([
            ft.Container(height=50), 
            ft.Container(height=30),
            grid_botones
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        contenedor.controls.append(ft.Container(columna_menu, alignment=ft.alignment.center, expand=True))

        contenedor.update()
