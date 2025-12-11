import flet as ft
from Views.Vistas_Base import VistaBase

class StudioCard(ft.Container):
    def __init__(self, name,desc, image_url, capacity, is_available, reserved_hours, on_click_action):
        super().__init__()
        self.name = name
        self.on_click_action = on_click_action
        self.width = 280
        # --- CAMBIO 1: Fondo Blanco y Sombra Suave ---
        self.bgcolor = "#FFFFFF" 
        self.border_radius = 15
        self.padding = 0
        self.clip_behavior = ft.ClipBehavior.HARD_EDGE
        self.animate_scale = ft.Animation(150, ft.AnimationCurve.EASE_OUT)
        self.on_hover = self.hover_effect
        # Sombra sutil para separar la tarjeta blanca del fondo gris de la página
        self.shadow = ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.1, "black"))
        
        # Lógica de colores (Usando ft.Colors en mayúscula)
        status_color = ft.Colors.GREEN if is_available else ft.Colors.TRANSPARENT
        status_text = "Disponible todo el dia" if is_available else ""
        
        btn_text = "Reservar" if is_available else "Ver horas disponibles"
    
        reservas_ui = []
        if reserved_hours:
            # Texto gris medio para el subtítulo
            reservas_ui.append(ft.Text("Reservas de hoy:", size=10, color="#2B2B2B", weight=ft.FontWeight.BOLD))
            
            fila_horas = ft.Row(scroll=ft.ScrollMode.HIDDEN, spacing=5)
            for hora in reserved_hours:
                # Diseño de cada "Chip" de hora
                chip = ft.Container(
                    content=ft.Row([
                        ft.Container(width=3, height=12, bgcolor="#F59E0B", border_radius=2), 
                        ft.Text(hora, size=11, weight=ft.FontWeight.W_500, color="#333333")
                    ], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                    
                    # --- CAMBIO 3: Fondo del chip Gris Muy Claro ---
                    bgcolor="#F5F5F5", 
                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                    border_radius=6,
                    border=ft.border.all(1, "#E0E0E0") # Borde sutil
                )
                fila_horas.controls.append(chip)
            reservas_ui.append(fila_horas)
            reservas_ui.append(ft.Divider(color="#E0E0E0", thickness=1))
        else:
            reservas_ui.append(ft.Container(height=10)) 

        # --- CONSTRUCCIÓN DE LA TARJETA ---
        self.content = ft.Column(
            spacing=0,
            controls=[
                # 1. IMAGEN + PRECIO
                ft.Stack(
                    controls=[
                        ft.Image(
                            src=image_url, 
                            width=float("inf"),
                            height=150, 
                            fit=ft.ImageFit.COVER,
                        )
                    ]
                ),
                
                # 2. INFORMACIÓN
                ft.Container(
                    padding=15,
                    content=ft.Column(
                        spacing=8,
                        controls=[
                            # A. TÍTULO Y CAPACIDAD
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    # --- CAMBIO 4: Texto Gris Oscuro para el Título (Legibilidad) ---
                                    ft.Text(desc, size=16, weight=ft.FontWeight.BOLD, color="#2B2B2B"),
                                    
                                    ft.Row([
                                        ft.Icon(ft.Icons.PEOPLE_OUTLINE, size=16, color=ft.Colors.GREY),
                                        ft.Text(f"{capacity}", color=ft.Colors.GREY)
                                    ], spacing=2)
                                ]
                            ),

                            # B. HORAS RESERVADAS
                            *reservas_ui, 
                            
                            # D. ESTADO Y BOTÓN
                            ft.Container(height=5),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Row([
                                        ft.Icon(ft.Icons.CIRCLE, size=8, color=status_color),
                                        # Texto de estado gris medio
                                        ft.Text(status_text, size=11, color="#2B2B2B") 
                                    ], spacing=5),
                                    
                                    ft.ElevatedButton(
                                        text=btn_text,
                                        style=ft.ButtonStyle(
                                           color=ft.Colors.WHITE,
                                                bgcolor={
                                                    ft.ControlState.DEFAULT: "#212121",  # Cambiado aquí
                                                    ft.ControlState.HOVERED: "#333333",  # Y aquí
                                                },
                                                shape=ft.RoundedRectangleBorder(radius=6)
                                        ),
                                        height=30,
                                        on_click=lambda e: self.on_click_action(self.name)
                                    )
                                ]
                            )
                        ]
                    )
                )
            ]
        )

    def hover_effect(self, e):
        self.scale = 1.02 if e.data == "true" else 1.0
        self.update()


# ---------------------------------------------------------
# 2. CLASE VISTA: PANTALLA DE SALAS
# ---------------------------------------------------------
class SalasView(VistaBase):
    def __init__(self, page: ft.Page):
        
        datos_usuario =page.session.get("usuario_data")        
        if datos_usuario:
            self.nombre_usuario = datos_usuario["nombre"]
        contenido=self.construir_contenido()
        super().__init__(page, "/salas", "Inicio", 0, self.construir_contenido())
        page.window_resizable = True

    def construir_contenido(self):
        from Controlador.controlador_reservas import Controlador_Reservas
        # --- SALA 1 ---
        datosSala1 = Controlador_Reservas.datos_inicio1()
        cap1 = 0
        horarios1 = []
        if datosSala1:
            cap1 = datosSala1[0][0] 
            for fila in datosSala1:
                hora = fila[1] 
                if hora: 
                    horarios1.append(hora)
        available1 = len(horarios1) == 0 

        datosSala2 = Controlador_Reservas.datos_inicio2()
        cap2 = 0
        horarios2 = []
        
        if datosSala2:
            cap2 = datosSala2[0][0]
            for fila in datosSala2:
                hora = fila[1]
                if hora:
                    horarios2.append(hora)
        
        available2 = len(horarios2) == 0

        datosSala3 = Controlador_Reservas.datos_inicio3()
        cap3 = 0
        horarios3 = []
        
        if datosSala3:
            cap3 = datosSala3[0][0]
            for fila in datosSala3:
                hora = fila[1]
                if hora:
                    horarios3.append(hora)
        
        available3 = len(horarios3) == 0

        datosSala4 = Controlador_Reservas.datos_inicio4()
        cap4 = 0
        horarios4 = []
        
        if datosSala4:
            cap4 = datosSala4[0][0]
            for fila in datosSala4:
                hora = fila[1]
                if hora:
                    horarios4.append(hora)
        
        available4 = len(horarios4) == 0

        

        db_salas = [
            {
                "name": "AZUL", 
                "desc":"Sala Azul",
                "img": "/salaazul.png", 
                "cap": cap1, 
                "avail": available1,
                "reserved": horarios1 
            },
            {
                "name": "ROJA ", 
                "desc":"Sala Roja",
                "img": "/salaroja.png", 
                "cap": cap2, 
                "avail": available2,
                "reserved": horarios2
            },
            {
                "name": "NARANJA", 
                "desc":"Sala naranja",
                "img": "/salanaranja.png", 
                "cap": cap3, 
                "avail": available3,
                "reserved": horarios3 
            },
            {
                "name": "BLANCA", 
                "desc":"Sala blanca",
                "img": "/salablanca.png", 
                "cap": cap4, 
                "avail": available4,
                "reserved": horarios4
            },
        ]

        # Crear el Grid
        cards_grid = ft.Row(
            spacing=30,      # Espacio horizontal entre tarjetas
            run_spacing=30,  # Espacio vertical entre filas
            alignment=ft.MainAxisAlignment.CENTER, # Centra el bloque de tarjetas
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                StudioCard(
                    name=sala["name"],
                    desc=sala["desc"],
                    image_url=sala["img"],
                    capacity=sala["cap"],
                    is_available=sala["avail"],
                    reserved_hours=sala["reserved"], 
                    on_click_action=self.reservar_sala
                ) for sala in db_salas
            ]
        )
        # Envolvemos la columna en un Container para poder darle margen (padding)
        contenido = ft.Container(
            # 1. AQUÍ SÍ FUNCIONA EL PADDING
            padding=ft.padding.symmetric(horizontal=30, vertical=20), 
            
            # 2. La columna pasa a ser el contenido de este contenedor
            content=ft.Column(
                        scroll=ft.ScrollMode.AUTO, 
                        controls=[
                            ft.Container(
                                padding=ft.padding.only(bottom=15),
                                content=ft.Column([
                                    ft.Text(f"Bienvenid@ {self.nombre_usuario}", size=14, weight=ft.FontWeight.BOLD, color="black", text_align=ft.TextAlign.CENTER),
                                    ft.Divider(height=20, color="transparent"),
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                            ),
                            
                            # Aquí va tu fila de tarjetas
                            cards_grid 
                        ],
                        spacing=10, 
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                )

        return contenido

    def reservar_sala(self, nombre_sala):
        self.page.client_storage.set("sala_selected", nombre_sala)
        self.page.go("/reservas")
