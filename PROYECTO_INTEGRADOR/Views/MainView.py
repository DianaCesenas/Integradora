import flet as ft
import datetime
import sys
import os

total_horas = [12, 1, 2, 3, 4, 5, 6, 7, 8, 9]
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Controlador.controlador_reservas import Controlador_Reservas
from Views.Vistas_Base import VistaBase

#Barra guinda 
class SalaCard(ft.Container):
    def __init__(self, sala_info, on_click_callback):
        super().__init__()
        self.sala_id = sala_info[0]
        self.name_sala = sala_info[1]
        self.data=self.name_sala
        self.on_click_callback = on_click_callback
        self.is_selected = False

        self.icon_control = ft.Icon(name=ft.Icons.MEETING_ROOM, color="#2C2E2F", size=24)
        self.text_control = ft.Text(self.name_sala, color="#2C2E2F", size=11, weight="bold", text_align="center")

        self.width = 95
        self.height = 80
        self.border_radius = 12
        self.padding = 10
        self.bgcolor = "#CCD3D8"
        self.border = ft.border.all(1, "white54")
        self.animate = ft.Animation(200, ft.AnimationCurve.EASE_OUT)
        self.alignment = ft.alignment.center
        
        self.on_click = lambda e: self.on_click_callback(self)

        
        self.content = ft.Column([self.icon_control, self.text_control], alignment="center", spacing=5)

    
    def set_selected(self, selected):
        self.is_selected = selected
        color_fondo_activo = "#7B8A98" 
        color_texto_inactivo = "#7B8A98" 
        if self.name_sala=="AZUL":
            color_texto_activo = "#3598CA"
            color_texto_inactivo = "#3598CA" 
        elif self.name_sala=="ROJA":
            color_texto_activo = "#992626"
            color_texto_inactivo = "#992626" 
        elif self.name_sala=="NARANJA":
            color_texto_activo = "#D47B23"
            color_texto_inactivo = "#D47B23" 
        elif self.name_sala=="BLANCA":
            color_texto_activo = "#FFFFFF"
            color_texto_inactivo = "#FFFFFF" 

        color_fondo_inactivo = "#CCD3D8"
        color_borde_inactivo = "#E0E0E0"

        if self.is_selected:
            self.bgcolor = color_fondo_activo
            self.border = ft.border.all(2, color_fondo_activo) 
            
            self.icon_control.color = color_texto_activo
            self.text_control.color = color_texto_activo
            
            self.shadow = ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.3, "black"))

        else:
            self.bgcolor = color_fondo_inactivo
            self.border = ft.border.all(1, color_borde_inactivo)
            
            self.icon_control.color = color_texto_inactivo
            self.text_control.color = color_texto_inactivo
            
            # Quitamos la sombra cuando no está seleccionado para que se vea "plano"
            self.shadow = None

        self.update()


#Clase principal que se inicializa en ruta 
class VistaReservas(VistaBase):
    def __init__(self, page: ft.Page):
        self.page = page
        self.id_sala_seleccionada = None
        self.fecha_seleccionada = datetime.date.today()
        self.lista_tarjetas = []
        self.sala_selected=self.page.client_storage.get("sala_selected")
        print(self.sala_selected)
        Tabla = self.mostrar_tabla()

        # Mandamos los parametros a la clase padre
        super().__init__(page, "/reservas", "Configura tu reserva", 4, Tabla)
        #self.did_()

    def mostrar_tabla(self):
        color_vino = "#A11F1F"
        bg_inputs = "#F7F9FC"

        #Calendario
        self.texto_fecha = ft.Text(
            value=self.fecha_seleccionada.strftime("%Y-%m-%d")
        )

        def on_date_change(e):
            if self.date_picker.value:
                fecha_obj = self.date_picker.value
                self.fecha_seleccionada = fecha_obj.strftime("%Y-%m-%d")
                self.texto_fecha.value = self.fecha_seleccionada 
                self.texto_fecha.update()
                
                self.actualizar_horarios_ui() 

        self.date_picker = ft.DatePicker(on_change=on_date_change, first_date=datetime.date.today())
        
        self.page.overlay.append(self.date_picker)

        def abrir_calendario(e):
            self.page.open(self.date_picker)

       
        try:
            salas_data = Controlador_Reservas.mostrarSalas()
        except:
            salas_data = [("No hay registros en el sistema")] 

        # --- COLORES ---
        # Aseguramos que el color vino esté definido para usarlo abajo
        color_iconos = "#475961"#"#7A8288"#"#424242" # O el código hex de tu guinda
        bg_inputs = "#F5F5F5"

        # --- LÓGICA DE SALAS (Igual, pero vital para el flujo) ---
        def gestionar_click_sala(tarjeta_clickeada):
            self.id_sala_seleccionada = tarjeta_clickeada.sala_id
            print(tarjeta_clickeada)
            for t in self.lista_tarjetas:
                print(tarjeta_clickeada)
                t.set_selected(t == tarjeta_clickeada)
                self.actualizar_horarios_ui()
                
        self.lista_tarjetas = []
        for data in salas_data:
            self.lista_tarjetas.append(SalaCard(data, gestionar_click_sala))
        

        contenedor_salas_top = ft.Container(
            width=650,
            padding=ft.padding.all(20),
            border_radius=20,
            bgcolor="white", # Fondo limpio
            # Una sombra suave para darle jerarquía sin usar colores fuertes
            shadow=ft.BoxShadow(
                blur_radius=15, 
                color=ft.Colors.with_opacity(0.06, "black"),
                offset=ft.Offset(0, 4)
            ),
            content=ft.Column([
                ft.Row([
                    ft.Text("1. Selecciona una Sala", weight=ft.FontWeight.BOLD, size=16, color="#1A1A1A"),
                ], alignment=ft.MainAxisAlignment.START),
                
                ft.Divider(height=15, color="transparent"),
                
                ft.Row(
                    controls=self.lista_tarjetas,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    scroll=ft.ScrollMode.AUTO
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

       # --- [1] LÓGICA DE DROPDOWNS (Igual que antes) ---
        # --- [1] LÓGICA DE DROPDOWNS ---
        clientes_opciones = []
        self.id_cliente = None
        try:
            lista_clientes = Controlador_Reservas.mostrarClientes()
        except:
            lista_clientes = []
            
        if lista_clientes and len(lista_clientes) > 0:
            clientes_opciones = [ft.dropdown.Option(key=str(x[0]), text=str(x[1])) for x in lista_clientes]

        # Dropdown con altura reducida (dense=True y content_padding bajo)
        self.dd_clientes = ft.Dropdown(
            label="Cliente", 
            options=clientes_opciones, 
            on_change=self.asignar_id_cliente,
            border_color="transparent", 
            content_padding=10, # 🔥 Menos relleno interno
            text_size=13, 
            expand=True,
            dense=True 
        )

        self.dd_hora_inicio = ft.Dropdown(
            label="Inicio", options=[], disabled=True, 
            on_change=self.actualizar_horas,
            border_color="transparent", text_size=13, expand=True, dense=True, content_padding=8
        )
        
        self.dd_hora_fin = ft.Dropdown(
            label="Fin", options=[], disabled=True, 
            border_color="transparent", text_size=13, expand=True, dense=True, content_padding=8
        )

        # --- [2] COMPONENTES VISUALES ---

        # 2.1 CAJA DE CLIENTES (Separada visualmente pero en la misma fila)
        
        # Caja izquierda: Icono + Dropdown + Botón (+)
        caja_cliente_main = ft.Container(
            expand=True, 
            bgcolor=bg_inputs, 
            border_radius=10, 
            border=ft.border.all(1, "#E0E0E0"),
            padding=ft.padding.only(left=10, right=5),
            height=45, # 🔥 Forzamos altura compacta
            content=ft.Row([
                ft.Icon(ft.Icons.PERSON_SEARCH, color=color_iconos, size=18),
                self.dd_clientes,
                ft.IconButton(
                    icon=ft.Icons.PERSON_ADD, 
                    icon_color="#17313E", 
                    icon_size=20,
                    tooltip="Nuevo Cliente",
                    on_click=self.abrir_modal_nuevo_cliente,
                    style=ft.ButtonStyle(padding=0) # Quitamos padding del botón
                )
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=5)
        )

        # Input Personas (Independiente)
        self.personas = ft.TextField(
            label="Pers.", 
            hint_text="#",
            width=50, 
            height=35, # Compacto
            text_size=13, 
            content_padding=5, 
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color="transparent", 
            text_align=ft.TextAlign.CENTER,
            bgcolor="transparent"
        )

        # Caja derecha: Personas (Separada)
        caja_personas = ft.Container(
            width=90, # Ancho fijo pequeño
            height=45,
            bgcolor=bg_inputs, 
            border_radius=10, 
            border=ft.border.all(1, "#E0E0E0"),
            padding=5,
            content=ft.Row([
                ft.Icon(ft.Icons.GROUPS, color=color_iconos, size=16),
                self.personas
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=2)
        )

        # Fila superior que contiene AMBOS (Cliente | Personas)
        row_superior = ft.Row(
            controls=[caja_cliente_main, caja_personas],
            spacing=10
        )

        # 2.2 ROW DE FECHA Y HORA (Compacta)
        
        # Caja Fecha
        box_fecha = ft.Container(
            expand=2, 
            height=45,
            bgcolor=bg_inputs, padding=ft.padding.symmetric(horizontal=10), border_radius=10, border=ft.border.all(1, "#E0E0E0"),
            content=ft.Row([
                ft.Icon(ft.Icons.CALENDAR_MONTH, color=color_iconos, size=18),
                ft.Column([ft.Text("Fecha", size=9, color="#78909C"), self.texto_fecha], spacing=0, alignment="center", expand=True),
                ft.IconButton(icon=ft.Icons.EDIT_CALENDAR, icon_color=color_iconos, icon_size=16, tooltip="Cambiar", on_click=abrir_calendario)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=5)
        )

        # Función auxiliar para cajas de hora pequeñas
        def crear_box_hora(control):
            return ft.Container(
                expand=1, 
                height=45,
                bgcolor=bg_inputs, border_radius=10, border=ft.border.all(1, "#E0E0E0"),
                padding=ft.padding.only(left=5),
                content=ft.Row([
                    ft.Icon(ft.Icons.ACCESS_TIME_FILLED, color="#B0BEC5", size=16),
                    control
                ], spacing=0, vertical_alignment="center")
            )

        row_fecha_hora = ft.Row(
            controls=[
                box_fecha,
                crear_box_hora(self.dd_hora_inicio),
                crear_box_hora(self.dd_hora_fin)
            ],
            spacing=10 
        )

        # --- [3] BOTONES COMPACTOS ---
        func_guardar = lambda e: self.guardarReservacion(self.texto_fecha.value, self.id_sala_seleccionada, self.dd_clientes.value, self.dd_hora_inicio.value, self.dd_hora_fin.value, self.personas.value)

        boton_confirmar = ft.ElevatedButton(
            content=ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, color="#3B6F35", size=18), ft.Text("CONFIRMAR", weight=ft.FontWeight.BOLD, color="white", size=13)], alignment="center", spacing=5),
            bgcolor="#6A7E8F", color="white",##B8C4CE
            height=45, # Altura reducida
            expand=True,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), elevation=3,side=ft.BorderSide(width=.5, color="#3B6F35")),
            on_click=func_guardar
        )

    

        fila_botones = ft.Row([boton_confirmar], spacing=10)

        # --- [4] ESTRUCTURA FINAL ---
        columna_inputs = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=10, 
            controls=[
            ft.Row(
                controls=[
                    # 1. El Título a la izquierda
                    ft.Text("2.Configura los detalles de reserva", weight=ft.FontWeight.BOLD, size=15, color="#2B2B2B"),
                    
                    # 2. El Botón a la derecha
                    ft.TextButton(
                        "Ver todas las reservas",
                        icon=ft.Icons.CALENDAR_VIEW_DAY_ROUNDED,
                        # OJO: Cambié BLUE_GREY_50 a 400 o 700 porque el 50 es casi invisible (blanco)
                        style=ft.ButtonStyle(color=ft.Colors.BLUE_GREY_700), 
                        on_click=lambda e: self.cambiar_ruta(e) # Asegúrate de pasar el evento si tu función lo pide
                    ),
                ],
            # ESTA ES LA CLAVE: Separa los elementos a los extremos
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN, 
            vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
    
            ft.Column([
                ft.Text("Cliente y Acompañantes", size=13, color="#2C2E2F", weight="w500"),
                row_superior
            ], spacing=3),

            # Input Fecha y Hora
            ft.Column([
                ft.Text("Fecha y Horario", size=13, color="#2C2E2F", weight="w500"),
                row_fecha_hora
            ], spacing=3),
            
            ft.Divider(height=10, color="transparent"),
            fila_botones 
        ]
    )

        tarjeta_formulario = ft.Container(
            content=columna_inputs,
            padding=20,
            bgcolor="white", 
            border_radius=15,
            width=650, 
            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.04, "black"), offset=ft.Offset(0, 4)),
            border=ft.border.all(1, "#EEEEEE")
        )

        columna_principal = ft.Column(
            controls=[
                contenedor_salas_top, 
                tarjeta_formulario 
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
            alignment=ft.MainAxisAlignment.CENTER, 
            spacing=20, # Espacio entre la caja de salas y el formulario
        )

        contenedor_principal = ft.Container(
            content=columna_principal,
            bgcolor="#FAFAFA",
            padding=10, #  Padding exterior mínimo
            expand=True,
            alignment=ft.alignment.center
        )

        return contenedor_principal
    
    def gestionar_click_sala(self,tarjeta_clickeada):
        self.id_sala_seleccionada = tarjeta_clickeada.sala_id
        print(tarjeta_clickeada)
        for t in self.lista_tarjetas:
            print(tarjeta_clickeada)
            t.set_selected(t == tarjeta_clickeada)
            self.actualizar_horarios_ui()
    
    def did_mount(self):
        if self.sala_selected!=None:
            for tarjeta in self.lista_tarjetas:
                if tarjeta.data == self.sala_selected:
                    self.gestionar_click_sala(tarjeta)
                    break

    #Opcion agregar nuevo client
    def abrir_modal_nuevo_cliente(self, e):
        self.campo_nombre = ft.TextField(label="Nombre", expand=True)
        self.campo_apellido = ft.TextField(label="Apellido", expand=True)
        self.campo_telefono = ft.TextField(label="Teléfono", expand=True)
        self.campo_email = ft.TextField(label="Email", expand=True)
        self.campo_calle = ft.TextField(label="Calle", expand=2)
        self.campo_numero = ft.TextField(label="Número", expand=1)
        self.campo_colonia = ft.TextField(label="Colonia", expand=3)

        def confirmar_agregar(e):
            if not self.campo_nombre.value:
                self.mostrar_alerta("El nombre no puede estar vacío")
                return
            
            registro = Controlador_Reservas.crear_cliente(
                self.campo_nombre.value,self.campo_apellido.value,self.campo_telefono.value,self.campo_email.value,self.campo_calle.value,self.campo_numero.value,self.campo_colonia.value)
            
            nombre=registro[0][1]
            apellido=registro[0][2]
            nombre_completo=nombre+" "+apellido
            nueva_opcion = ft.dropdown.Option(text=nombre_completo, key=registro[0][0]) # Key debe ser el ID real de la BD
            self.dd_clientes.options.append(nueva_opcion)
            self.dd_clientes.update()
            
            self.page.close(dialogo)
            self.mostrar_alerta(f"Cliente '{self.campo_nombre.value}' agregado.")

        dialogo = ft.AlertDialog(
            title=ft.Text("Nuevo Cliente"),
            content=ft.Column([
                ft.Row([self.campo_nombre, self.campo_apellido]),
                ft.Row([self.campo_telefono, self.campo_email]),
                ft.Row([self.campo_calle, self.campo_numero]),
                self.campo_colonia
            ], height=300, tight=True),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.page.close(dialogo), style=ft.ButtonStyle(color=ft.Colors.GREY)),
                ft.ElevatedButton("Guardar", on_click=confirmar_agregar, bgcolor="#A11F1F", color="white")
            ],
        )
        self.page.open(dialogo)

    #Cambiar ruta del programa
    def cambiar_ruta(self, e):
        self.page.go("/gestion_reservas")

    #Asignar id del cliente cuando se seleccione una opcion del dropdown
    def asignar_id_cliente(self,e):
        self._id_cliente=self.dd_clientes.value

    #Actualizar horas de inicio disponibles  cada que se selecciona una sala o fecha difente 
    def actualizar_horarios_ui(self):
        #Si se ha selecionado una sala entonces se habilitan los dropdowns
        if self.id_sala_seleccionada!= None:
            opciones = []
            self.sin_reservas=False
            horas_procesadas=[]
            self.hrs_no_disp=[]
            self.horas_disponibles=[]
            hora_time_delta=Controlador_Reservas.mostrarHorasDisponibles(self.texto_fecha.value,self.id_sala_seleccionada)
            if len(hora_time_delta)>0:
                #Pasamos las horas a segundo(asi lo toma python)
                hora_formateada = [tuple(f"{int(td.total_seconds() // 3600):02}:{int((td.total_seconds() % 3600) // 60):02}"for td in fila )for fila in hora_time_delta]
                #Formatemaos la hora le quitamos ceros y : para convetirlos a enteros 
                for inicio_str, fin_str in hora_formateada:
                    self.h_inicio = int(inicio_str.split(":")[0])
                    self.h_fin = int(fin_str.split(":")[0])
                    horas_procesadas.append((self.h_inicio, self.h_fin))
                horas_procesadas.sort()
                #Teniendo lasd horas en num enteros ahora hacemos un simple ciclo for para obtenr las horas de en medio 
                for inicio, fin in horas_procesadas:
                    rango_ocupado = list(range(inicio, fin))
                    self.hrs_no_disp.extend(rango_ocupado)
                print(f"rango_ocupado{self.hrs_no_disp}")
                #Teniendo el rango completo de horas disponibles ahora le agregamos :00 para mejor vizualizacion del usuario 
                for hora in total_horas:
                    if (hora not in self.hrs_no_disp)and (hora!=9):
                        hora_texto = f"{hora}:00"
                        self.horas_disponibles.append(hora_texto)
                #Agreagamos las horas disponibles con formato a los dropdrowns
                for h in self.horas_disponibles:
                    opciones.append(ft.dropdown.Option(h))
                    self.dd_hora_inicio.options = opciones
                    self.dd_hora_inicio.disabled = False
                    self.dd_hora_inicio.value = None
                    self.dd_hora_inicio.update()
            #Si no hay reservaciones registradas entonces se agrega el horario completo 
            else:
                for hora in total_horas:
                    if hora!=9:
                        hora_texto = f"{hora}:00"
                        self.horas_disponibles.append(hora_texto)
                #Agreagamos las horas disponibles con formato a los dropdrowns
                for h in self.horas_disponibles:
                    opciones.append(ft.dropdown.Option(h))
                self.dd_hora_inicio.options = opciones
                self.sin_reservas=True
                #habilitamos los dropdowns
                self.dd_hora_inicio.disabled = False
                self.dd_hora_inicio.value = None
                self.dd_hora_inicio.update()
        #Si no se ha seleccionado ninguna sala no se puede seleccionar horarios 
        else:
            self.dd_hora_inicio.disabled = True
            self.dd_hora_inicio.update()

    def actualizar_horas(self,e):
        #Si no hay reservas registradas entonces se calculan las horas de termino disponibles 
        if self.sin_reservas:

            horas_actualizadas=[]
            horas_actualizadas2=[]
            opciones = []
            self.hora_fin_disp=[]
            self.horas_disponibles_ent=[]
            hi_selected=self.dd_hora_inicio.value
            #Si la hora de inicio no ha sido seleccionada se rompe la funcion
            if not hi_selected:
                return
            #Se da formato a la hora 
            for hora_formato in self.horas_disponibles:
                self.h= int(hora_formato.split(":")[0])
                self.horas_disponibles_ent.append((self.h))
            #Convertimos a entero la hora de inicio  seleccionada 
            h_inicio_select = int(hi_selected.split(":")[0])
    
            if h_inicio_select==8:
                horas_actualizadas.append(9)
            elif h_inicio_select==12:
                h_inicio_select=0
                for h in self.horas_disponibles_ent:
                    if (h>h_inicio_select)and (h!=12):
                       horas_actualizadas.append(h)
            else:
                for h in self.horas_disponibles_ent:
                    if (h>h_inicio_select)and (h!=12):
                       horas_actualizadas.append(h)
            
            for hora in horas_actualizadas:
                        hora_texto = f"{hora}:00"
                        horas_actualizadas2.append(hora_texto)
            for h in horas_actualizadas2:
                opciones.append(ft.dropdown.Option(h))
            self.dd_hora_fin.options = opciones
            self.dd_hora_fin.disabled = False
            self.dd_hora_fin.value = None
            self.dd_hora_fin.update() 
        else:
            horas_actualizadas=[]
            horas_actualizadas2=[]
            opciones = []
            self.hora_fin_disp=[]
            self.horas_disponibles_ent=[]
            self.horas_disponibles_ent.append(9)

            hi_selected=self.dd_hora_inicio.value
            if not hi_selected:
                return
            h_inicio_select = int(hi_selected.split(":")[0])
            
            hora_minima=int(min(self.hrs_no_disp))
            hora_maxima=int(max(self.hrs_no_disp))
            print(hora_maxima)
            print(hora_minima)
            diff_h_maxima=hora_maxima-h_inicio_select
            diff_h_minima=hora_minima-h_inicio_select
            print(diff_h_maxima)
            if hora_maxima==12:
                self.hrs_no_disp.remove(12)
                hora_maxima=int(max(self.hrs_no_disp))

            for hora_formato in self.horas_disponibles:
                self.h= int(hora_formato.split(":")[0])
                self.horas_disponibles_ent.append((self.h))
            
            if h_inicio_select==8:
                horas_actualizadas.append(9)
            elif h_inicio_select==12:
                if len(self.horas_disponibles_ent)>2:
                    self.horas_disponibles_ent.append(hora_minima)
                    self.horas_disponibles_ent.append(hora_maxima)
                for h in self.horas_disponibles_ent:
                    if h>0 and h!=12 and (h<=hora_minima):
                        horas_actualizadas.append(h)
            elif h_inicio_select!=8:
                if len(self.horas_disponibles_ent)>8:
                    self.horas_disponibles_ent.append(hora_minima)
                    self.horas_disponibles_ent.append(hora_maxima)
                    self.horas_disponibles_ent.sort()
                    for h in self.horas_disponibles_ent:
                        if h_inicio_select<hora_minima:
                            if (h>h_inicio_select) and (h<=hora_minima):
                                if h!=12:
                                    horas_actualizadas.append(h)
                            elif diff_h_minima==1:
                                    horas_actualizadas.append(hora_minima)
                                    break
                        elif h_inicio_select>hora_minima:
                            if (h>h_inicio_select) and (h<=hora_maxima):
                                if h!=12:
                                    horas_actualizadas.append(h)
                            elif diff_h_maxima==1:
                                    horas_actualizadas.append(hora_maxima)
                                    break
                else:
                    self.horas_disponibles_ent.append(hora_minima)
                    self.horas_disponibles_ent.sort()
                    for h in self.horas_disponibles_ent:
                        if h_inicio_select<hora_minima:
                            if (h>h_inicio_select) and (h<=hora_minima):
                                if h!=12:
                                    horas_actualizadas.append(h)
                            elif diff_h_minima==1:
                                    horas_actualizadas.append(hora_minima)
                                    break
                        elif h_inicio_select>hora_minima:
                            if (h>h_inicio_select) and (h>hora_maxima):
                                print("ggtft")
                                if h!=12:
                                    horas_actualizadas.append(h)
                            elif diff_h_maxima==1:
                                    horas_actualizadas.append(hora_maxima)
                                    break

            for hora in horas_actualizadas:
                        hora_texto = f"{hora}:00"
                        horas_actualizadas2.append(hora_texto)
            for h in horas_actualizadas2:
                opciones.append(ft.dropdown.Option(h))
            self.dd_hora_fin.options = opciones
            self.dd_hora_fin.disabled = False
            self.dd_hora_fin.value = None
            self.dd_hora_fin.update() 

    #Alerta de datos invalidos 
    def mostrar_alerta(self, mensaje):
        dialogo = ft.AlertDialog(
            title=ft.Text("Aviso"),
            content=ft.Text(mensaje),
            actions=[
                ft.TextButton("Entendido", on_click=lambda e: self.page.close(dialogo))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.open(dialogo)

  
    def guardarReservacion(self, fecha, id_sala, id_cliente, horai, horaf, p):

        if id_sala is None:
            self.mostrar_alerta("Por favor, selecciona una Sala antes de continuar.")
            return

        if not id_cliente:
            self.mostrar_alerta("Debes seleccionar un Cliente.")
            return

        if not p:
            self.mostrar_alerta("El campo de Personas no puede estar vacío.")
            return
        
        if not p.isdigit() or int(p) <= 0:
            self.mostrar_alerta("Ingresa un número válido de personas (mayor a 0).")
            return

        if not horai or not horaf:
            self.mostrar_alerta("Selecciona hora de inicio y fin.")
            return

        resp = Controlador_Reservas.agregar_view(fecha, id_sala, id_cliente, horai, horaf, p)
        
        if resp:
            self.page.client_storage.clear()

            exito_dialog = ft.AlertDialog(
                icon=ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, size=50, color="green"),
                title=ft.Text("Éxito"),
                content=ft.Text("Reservación guardada correctamente."),
                actions=[
                    ft.TextButton("OK", on_click=lambda e: self.page.close(exito_dialog))
                ],
            )
            self.page.open(exito_dialog)
