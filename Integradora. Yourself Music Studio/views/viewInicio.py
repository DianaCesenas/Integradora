import flet as ft
from Views.Vistas_Base import VistaBase
total_horas=[12,1,2,3,4,5,6,7,8,9]
from datetime import datetime
# ---------------------------------------------------------
# 1. CLASE COMPONENTE: TARJETA DE SALA
# ---------------------------------------------------------
class StudioCard(ft.Container):
    def __init__(self, name, image_url, price, capacity, equipment, is_available, on_click_action):
        super().__init__()
        self.name = name
        self.is_available = is_available
        self.on_click_action = on_click_action
        
        # Estilos visuales
        self.bgcolor = "#540C0C"
        self.border_radius = 15
        self.padding = 0
        self.clip_behavior = ft.ClipBehavior.HARD_EDGE
        self.animate_scale = ft.Animation(150, ft.AnimationCurve.EASE_OUT)
        self.on_hover = self.hover_effect
        
        # Colores y Textos (Usando ft.Colors y ft.Icons correctamente para v0.28+)
        status_color = ft.Colors.GREEN_ACCENT if is_available else ft.Colors.RED_ACCENT
        status_text = "Disponible ahora" if is_available else "Ocupada hasta las 18:00"
        btn_text = "Reservar" if is_available else "Ver Horarios"
        btn_icon = ft.Icons.CALENDAR_MONTH if is_available else ft.Icons.ACCESS_TIME
        
        btn_style = ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor="#7c3aed" if is_available else "#333333",
        )

        # Construcción de la tarjeta
        self.content = ft.Column(
            spacing=0,
            controls=[
                # Imagen + Precio
                ft.Stack(
                    controls=[
                        # AQUI ESTA LA MAGIA: image_url es solo texto, ej: "/salaazul.png"
                        ft.Image(
                            src=image_url, 
                            width=float("inf"),
                            height=180,
                            fit=ft.ImageFit.COVER
                        ),
                        ft.Container(
                            content=ft.Text(f"${price}/hr", weight=ft.FontWeight.BOLD, size=12),
                            bgcolor="black",
                            padding=ft.padding.symmetric(horizontal=10, vertical=5),
                            border_radius=ft.border_radius.only(top_left=10, bottom_right=10),
                            right=0, bottom=0,
                            opacity=0.8
                        )
                    ]
                ),
                
                # Información (Texto y Botones)
                ft.Container(
                    padding=15,
                    content=ft.Column(
                        spacing=10,
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(name, size=18, weight=ft.FontWeight.BOLD),
                                    ft.Row([
                                        ft.Icon(ft.Icons.PEOPLE_OUTLINE, size=16, color="grey"),
                                        ft.Text(f"{capacity}", color="grey")
                                    ], spacing=2)
                                ]
                            ),
                            
                            ft.Row(
                                controls=[
                                    ft.Container(
                                        content=ft.Icon(icon, size=16, color="#b3b3b3"),
                                        bgcolor="#2d2d2d",
                                        padding=5,
                                        border_radius=5
                                    ) for icon in equipment
                                ],
                            ),

                            ft.Divider(color="#333333", thickness=1),

                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Row([
                                        ft.Icon(ft.Icons.CIRCLE, size=10, color=status_color),
                                        ft.Text(status_text, size=12, color=status_color)
                                    ], spacing=5),
                                    
                                    ft.ElevatedButton(
                                        text=btn_text,
                                        icon=btn_icon,
                                        style=btn_style,
                                        height=35,
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
        # 1. Creamos el contenido
        contenido_pagina = self.construir_contenido()

        # 2. Enviamos el contenido a VistaBase
        # Asegúrate de que VistaBase acepte estos argumentos en este orden
        super().__init__(page, "/salas", "Estudios", 0, contenido_pagina)

    def construir_contenido(self):
        
        # --- CORRECCIÓN AQUÍ ---
        # No creamos objetos ft.Image(). Solo pasamos las rutas como strings.
        # Flet buscará estas rutas en tu carpeta 'assets' definida en main.py
        
        db_salas = [
            {
                "name": "Sala A - The Groove", 
                "img": "/salaazul.png",  # <--- SOLO EL TEXTO
                "price": 30, 
                "cap": 5, 
                "equip": [ft.Icons.MUSIC_NOTE, ft.Icons.MIC, ft.Icons.SPEAKER], 
                "avail": True
            },
            {
                "name": "Sala B - Acoustic Heaven", 
                "img": "/salaroja.png",  # <--- SOLO EL TEXTO
                "price": 30, 
                "cap": 3, 
                "equip": [ft.Icons.PIANO, ft.Icons.MIC], 
                "avail": False
            },
            {
                "name": "Sala C - The Bunker", 
                "img": "/salanaranja.png", # <--- SOLO EL TEXTO
                "price": 30, 
                "cap": 8, 
                "equip": [ft.Icons.MUSIC_NOTE, ft.Icons.SPEAKER_GROUP, ft.Icons.ALBUM], 
                "avail": True
            },
             {
                "name": "Sala D - Podcast Studio", 
                "img": "/salablanca.png", # <--- SOLO EL TEXTO
                "price": 30, 
                "cap": 4, 
                "equip": [ft.Icons.MIC_EXTERNAL_ON, ft.Icons.HEADSET_MIC], 
                "avail": True
            },
        ]

        # Crear el Grid usando los datos
        cards_grid = ft.ResponsiveRow(
            spacing=20,
            run_spacing=20,
            controls=[
                ft.Column(
                    col={"xs": 12, "sm": 6, "md": 4, "xl": 3},
                    controls=[
                        StudioCard(
                            name=sala["name"],
                            image_url=sala["img"], # Pasamos el string a la clase
                            price=sala["price"],
                            capacity=sala["cap"],
                            equipment=sala["equip"],
                            is_available=sala["avail"],
                            on_click_action=self.reservar_sala
                        )
                    ]
                ) for sala in db_salas
            ]
        )

        # Empaquetamos todo en una Columna que será "Tabla"
        contenido = ft.Column(
            scroll=ft.ScrollMode.HIDDEN,
            controls=[
                ft.Container(
                    padding=ft.padding.only(bottom=20),
                    content=ft.Column([
                         ft.Text("Encuentra tu sonido", size=14, color="grey"),
                         ft.Divider(height=20, color="transparent"),
                    ])
                ),
                cards_grid
            ]
        )

        return contenido

    def reservar_sala(self, nombre_sala):
        self.page.snack_bar = ft.SnackBar(ft.Text(f"Seleccionaste: {nombre_sala}"))
        self.page.snack_bar.open = True
        self.page.update()

    def disponibilidad(self):
        ahora = datetime.now()
        fecha_hoy = ahora.strftime("%Y-%m-%d")
        opciones = []
        self.sin_reservas=False
        horas_procesadas=[]#Aqui guardamos las horan de inicio y termino registradas 
        self.hrs_no_disp=[]
        self.horas_disponibles=[]
        print("Errror 5")
        from Controlador.controlador_reservas import Controlador_Reservas
        horas_sala1=Controlador_Reservas.mostrarHorasDisponibles(fecha_hoy,1)#Lo que devuelve cursor.fetchall es en segundos
        if len(horas_sala1)>0:
            #Conviertimos un timedelta (los segundos) a texto 'HH:MM'
            hora_formateada = [tuple(f"{int(td.total_seconds() // 3600):02}:{int((td.total_seconds() % 3600) // 60):02}"for td in fila )for fila in horas_sala1]
        
        # Convertimos "10:00" -> 10 (Entero)
        for inicio_str, fin_str in hora_formateada:
            self.h_inicio = int(inicio_str.split(":")[0])
            self.h_fin = int(fin_str.split(":")[0])
            horas_procesadas.append((self.h_inicio, self.h_fin))
                        

        #Aqui aregamos a una lista las horas de en medio entre hora incio y hora de termino
        for inicio, fin in horas_procesadas:
            rango_ocupado = list(range(inicio, fin))
            self.hrs_no_disp.extend(rango_ocupado)

        #Aqui obtenemos las horas disponibles,recorremos el total de horas y si la hora  no se encuentra en las horas no disponibles se agrega a la lista de horas disponibles 
        for hora in total_horas:
            if (hora not in self.hrs_no_disp)and (hora!=9):
                hora_texto = f"{hora}:00"
                self.horas_disponibles.append(hora_texto)
                
        else:
            for hora in total_horas:
                if hora!=9:
                    hora_texto = f"{hora}:00"
                    self.horas_disponibles.append(hora_texto)
            for h in self.horas_disponibles:
                opciones.append(ft.dropdown.Option(h))
            self.dd_hora_inicio.options = opciones
            self.sin_reservas=True

            self.dd_hora_inicio.disabled = False
            self.dd_hora_inicio.value = None
            self.dd_hora_inicio.update()
