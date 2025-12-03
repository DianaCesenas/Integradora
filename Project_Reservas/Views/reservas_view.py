import flet as ft
import datetime
import sys
import os

# --- CONFIGURACIÓN DE RUTAS ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from Controlador.controlador_reservas import Controlador_Reservas
except ImportError:
    Controlador_Reservas = None

# ========================================
# 1.CLASE SALA CARD (El Botón de la Sala)
# ========================================
class SalaCard(ft.Container):
    def __init__(self, sala_info, on_click_callback):
        super().__init__()
        self.sala_id = sala_info[0]
        self.name = sala_info[1]
        self.on_click_callback = on_click_callback
        self.is_selected = False

        self.icon_control = ft.Icon(name=ft.Icons.MEETING_ROOM, color="white", size=24)
        self.text_control = ft.Text(self.name, color="white", size=11, weight="bold", text_align="center")

        self.width = 90
        self.height = 80
        self.border_radius = 12
        self.padding = 10
        self.bgcolor = ft.Colors.TRANSPARENT
        self.border = ft.border.all(1, "white54")
        self.animate = ft.Animation(200, ft.AnimationCurve.EASE_OUT)
        self.alignment = ft.alignment.center
        
        self.on_click = lambda e: self.on_click_callback(self)
        self.content = ft.Column([self.icon_control, self.text_control], alignment="center", spacing=5)

    def set_selected(self, selected):
        self.is_selected = selected
        if self.is_selected:
            self.bgcolor = "white"
            self.border = ft.border.all(2, "white")
            self.icon_control.color = "#A11F1F"
            self.text_control.color = "#A11F1F"
        else:
            self.bgcolor = ft.Colors.TRANSPARENT
            self.border = ft.border.all(1, "white54")
            self.icon_control.color = "white"
            self.text_control.color = "white"
        self.update()


# ==========================================
# 2. CLASE VISTA SALAS (La Pantalla Principal)
# ==========================================
class VistaSalas(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/reservas")
        self.page = page
        self.bgcolor = "white"
        self.padding = 0

        color_vino = "#A11F1F"
        color_fondo_inputs = "#F7F9FC"

        # --- A. LÓGICA DEL CALENDARIO ---
        self.selected_date_text = ft.Text(
            value=datetime.date.today().strftime("%d de %B, %Y"),
            size=16, weight="bold", color="#333"
        )

        def on_date_change(e):
            if self.date_picker.value:
                # Formatear la fecha para mostrarla bonita
                fecha = self.date_picker.value
                self.selected_date_text.value = fecha.strftime("%d de %B, %Y")
                self.page.update()

        self.date_picker = ft.DatePicker(on_change=on_date_change)
        self.page.overlay.append(self.date_picker)

        def abrir_calendario(e):
            self.page.open(self.date_picker)

        # --- B. LÓGICA DE SALAS ---
        if Controlador_Reservas:
            try:
                salas_data = Controlador_Reservas.mostrarSalas()
            except:
                salas_data = [(1, "Sala A"), (2, "Sala B"), (3, "Sala C")]
        else:
            salas_data = [(1, "Sala A"), (2, "Sala B"), (3, "Sala C")]

        self.lista_tarjetas = []

        def gestionar_click_sala(tarjeta_clickeada):
            for t in self.lista_tarjetas:
                t.set_selected(t == tarjeta_clickeada)

        for data in salas_data:
            self.lista_tarjetas.append(SalaCard(data, gestionar_click_sala))

        grid_salas = ft.GridView(
            expand=True, runs_count=2, child_aspect_ratio=1.1, 
            spacing=10, run_spacing=10, controls=self.lista_tarjetas
        )

        # --- C. DISEÑO VISUAL ---

        # 1. BARRA LATERAL (Con margen izquierdo agregado)
        sidebar_guinda = ft.Container(
            width=280,
            height=500, # Un poco más alto
            margin=ft.margin.only(left=30, top=20, bottom=20), # <--- MARGEN IZQUIERDO AQUÍ
            bgcolor=color_vino,
            border_radius=30,
            padding=25,
            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.4, color_vino)), # Sombra bonita
            alignment=ft.alignment.center,
            content=ft.Column([
                ft.Text("Salas", size=22, weight="bold", color="white"),
                ft.Text("Selecciona una sala", size=12, color="white70"),
                ft.Divider(height=20, color="transparent"),
                ft.Container(content=grid_salas, height=300), 
                ft.Container(expand=True),
                ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE, color="white70", size=16), ft.Text("Una sala a la vez", color="white70", size=12)], alignment="center")
            ])
        )

        # 2. CARGAR CLIENTES
        clientes_opciones = []
        try:
            datos_sql = Controlador_Reservas.mostrarClientes() if Controlador_Reservas else []
            if len(datos_sql) > 0:
                clientes_opciones = [ft.dropdown.Option(key=str(x[0]), text=str(x[1])) for x in datos_sql]
            else:
                clientes_opciones = [ft.dropdown.Option(text="Cliente General"), ft.dropdown.Option(text="Demo Usuario")]
        except Exception:
            clientes_opciones = [ft.dropdown.Option(text="Sin conexión")]

        horas_opciones = [ft.dropdown.Option(f"{h:02d}:00") for h in range(8, 22)]

        # 3. FORMULARIO DERECHO (Centrado)
        form_content = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, # <--- ESTO CENTRA TODO EL CONTENIDO
            spacing=20,
            controls=[
                ft.Text("Configurar Reserva", size=28, weight="bold", color="#333"),
                ft.Divider(height=10, color="transparent"),

                # -- CLIENTE --
                ft.Text("1. Selecciona el Cliente", size=14, weight="bold", color="#555"),
                ft.Container(
                    width=400, # Ancho fijo para que se vea centrado y uniforme
                    bgcolor=color_fondo_inputs, 
                    border_radius=12, 
                    padding=5,
                    border=ft.border.all(1, "#E0E0E0"),
                    content=ft.Row([
                        ft.Container(padding=10, content=ft.Icon(ft.Icons.PERSON, color=color_vino)),
                        ft.Dropdown(
                            label="Lista de Clientes", 
                            options=clientes_opciones, 
                            border_color="transparent", 
                            text_size=14,
                            content_padding=10,
                            expand=True
                        )
                    ], vertical_alignment=ft.CrossAxisAlignment.CENTER)
                ),

                ft.Divider(height=10, color="transparent"),

                # -- FECHA (Rediseñado y centrado) --
                ft.Text("2. Fecha de Reserva", size=14, weight="bold", color="#555"),
                ft.Container(
                    width=400, # Mismo ancho que cliente
                    bgcolor=color_fondo_inputs,
                    padding=10, 
                    border_radius=12,
                    border=ft.border.all(1, "#E0E0E0"),
                    content=ft.Row([
                        # Icono
                        ft.Container(
                            content=ft.Icon(ft.Icons.CALENDAR_MONTH, color="white", size=20), 
                            bgcolor=color_vino, 
                            padding=10, 
                            border_radius=8
                        ),
                        # Texto Fecha
                        ft.Column([
                            ft.Text("Fecha Seleccionada:", size=10, color="grey"), 
                            self.selected_date_text
                        ], spacing=2, expand=True),
                        # Botón para cambiar (Ícono clickable)
                        ft.IconButton(
                            icon=ft.Icons.EDIT_CALENDAR, 
                            icon_color=color_vino, 
                            tooltip="Cambiar Fecha",
                            on_click=abrir_calendario
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ),

                ft.Divider(height=10, color="transparent"),

                # -- HORARIOS --
                ft.Text("3. Definir Horario", size=14, weight="bold", color="#555"),
                ft.Row([
                    # Inicio
                    ft.Container(
                        width=180, bgcolor=color_fondo_inputs, border_radius=12, border=ft.border.all(1, "#E0E0E0"),
                        content=ft.Row([
                            ft.Container(padding=10, content=ft.Icon(ft.Icons.ACCESS_TIME_FILLED, color=color_vino, size=18)),
                            ft.Dropdown(label="Inicio", options=horas_opciones, border_color="transparent", text_size=14, expand=True)
                        ], vertical_alignment=ft.CrossAxisAlignment.CENTER)
                    ),
                    ft.Text("-", size=20, color="#ccc"),
                    # Fin
                    ft.Container(
                        width=180, bgcolor=color_fondo_inputs, border_radius=12, border=ft.border.all(1, "#E0E0E0"),
                        content=ft.Row([
                            ft.Container(padding=10, content=ft.Icon(ft.Icons.ACCESS_TIME, color=color_vino, size=18)),
                            ft.Dropdown(label="Fin", options=horas_opciones, border_color="transparent", text_size=14, expand=True)
                        ], vertical_alignment=ft.CrossAxisAlignment.CENTER)
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),

                ft.Divider(height=30, color="transparent"),

                # -- BOTÓN GUARDAR (Centrado) --
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.SAVE, color="white"),
                        ft.Text("CONFIRMAR RESERVACIÓN", weight="bold")
                    ], alignment="center", spacing=10),
                    bgcolor="#3dbf54", 
                    color="white", 
                    height=55, 
                    width=300,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=15),
                        elevation=5
                    ),
                    on_click=lambda e: print("Guardando reserva...")
                )
            ]
        )

        form_derecho = ft.Container(
            expand=True,
            padding=ft.padding.all(30),
            alignment=ft.alignment.center, # Asegura que el contenido flote en el centro
            content=form_content
        )

        # --- LAYOUT FINAL ---
        self.controls = [
            ft.Row(
                controls=[sidebar_guinda, form_derecho],
                expand=True,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
        ]

# ==========================================
# 3. MAIN
# ==========================================
def main(page: ft.Page):
    page.title = "Sistema de Reservas"
    page.window_width = 1100
    page.window_height = 800
    page.bgcolor = "white"
    
    # Configuración regional para fecha en español (opcional)
    # import locale
    # try: locale.setlocale(locale.LC_TIME, 'es_ES')
    # except: pass

    vista = VistaSalas(page)
    page.views.append(vista)
    page.go("/reservas")

if __name__ == "__main__":
    ft.app(target=main)