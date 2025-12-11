import flet as ft
from Controlador.controlador_salas import Controlador
from Views.Vistas_Base import VistaBase

class VistasSalas(VistaBase):
    def __init__(self, page: ft.Page):
        self.PURPLE = "#A11F1F"
        self.BG_COLOR = "#F4F5F9"
        self.page = page
        
        # Estado
        self.texto_busqueda = "" 
        self.orden_actual = None  

        # Configuración inicial de la página
        super().__init__(page, "/salass", "Gestion de Salas", 0, None)
        # Nota: No asignamos contenido_visual en el super() porque lo armaremos manualmente en self.controls
        
        self.page.bgcolor = self.BG_COLOR

        # --- BUSCADOR ---
        self.buscador = ft.TextField(
            hint_text="Buscar sala por nombre...", 
            prefix_icon=ft.Icons.SEARCH, 
            border_radius=10, 
            bgcolor="white",
            border_width=0.5,      
            border_color="#2B2B2B",    
            expand=True,
            # Al escribir, llamamos directamente a ejecutar_busqueda
            on_change=lambda e: self.ejecutar_busqueda(e.control.value),
            on_submit=lambda e: self.ejecutar_busqueda(e.control.value)
        )

        # --- BOTÓN ORDENAR (Lo guardamos en self para cambiar su icono luego) ---
        self.icono_orden_btn = ft.IconButton(
            icon=ft.Icons.SORT_BY_ALPHA,
            icon_color="#2B2B2B",
            tooltip="Ordenar por Nombre (A-Z) / Quitar Orden",
            on_click=self.alternar_orden
        )

        # --- HEADER (Barra superior completa) ---
        btn_limpiar = ft.Container(
            content=ft.IconButton(
                ft.Icons.REFRESH, icon_color="#2B2B2B", 
                tooltip="Recargar", on_click=self.limpiar_busqueda
            ),
            bgcolor="#BBC3CB", border_radius=10, height=45
        )

        btn_ordenar_container = ft.Container(
            content=self.icono_orden_btn,
            bgcolor="#BBC3CB", border_radius=10, height=45
        )

        btn_agregar = ft.ElevatedButton(
            text="Agregar Nuevo", icon=ft.Icons.ADD,
            bgcolor="#CBD0D5", color="#2B2B2B", height=45, expand=True,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            on_click=lambda e: self.abrir_dialogo_agregar()
        )

        contenedor_header = ft.Container(
            content=ft.Column([
                ft.Row([self.buscador, btn_limpiar, btn_ordenar_container], spacing=10), 
                ft.Row([btn_agregar], spacing=10)
            ], spacing=10), 
            padding=20, bgcolor="#F9F9F9"
        )

        # --- ENCABEZADOS DE TABLA (Fijos) ---
        titulos = ["Nombre", "Capacidad", "Acciones"]
        anchos = [2, 1, 1] 
        fila_encabezados = ft.Row(
            controls=[
                ft.Container(content=ft.Text(titulos[0], color="#2B2B2B", weight="bold"), expand=anchos[0], padding=ft.padding.only(left=20)),
                ft.Container(content=ft.Text(titulos[1], color="#2B2B2B", weight="bold"), expand=anchos[1]),
                ft.Container(content=ft.Text(titulos[2], color="#2B2B2B", weight="bold"), expand=anchos[2]),
            ]
        )
        contenedor_titulos = ft.Container(
            content=fila_encabezados,
            padding=ft.padding.symmetric(horizontal=20, vertical=15),
            bgcolor="white",
            border=ft.border.only(bottom=ft.border.BorderSide(1, "#E0E0E0"))
        )

        
        self.contenedor_lista_salas = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

        # --- MARCA DE AGUA (Fondo) ---
        marca_agua = ft.Container(
            content=ft.Icon(ft.Icons.MUSIC_NOTE_ROUNDED, size=300, opacity=0.1, color=ft.Colors.BLACK54),
            alignment=ft.alignment.center, expand=True
        )

        # Usamos Stack para que la marca de agua quede fija al fondo
        contenido_tabla_visible = ft.Column([
            contenedor_titulos,      
            self.contenedor_lista_salas 
        ], spacing=0, expand=True)

        cuerpo_tabla = ft.Container(
            content=ft.Stack([marca_agua, contenido_tabla_visible], expand=True),
            bgcolor="white", border_radius=15, margin=20, expand=True,
            shadow=ft.BoxShadow(blur_radius=10, color="#1A000000")
        )

       
        self.controls = [
            ft.Column([contenedor_header, cuerpo_tabla], spacing=0, expand=True)
        ]

    def did_mount(self):
        # Carga inicial segura
        self.recargar_tabla()


    def ejecutar_busqueda(self, texto):
        self.texto_busqueda = texto.strip()
        datos = Controlador.mostrar(texto_busqueda=self.texto_busqueda, orden=self.orden_actual)
        self.llenar_tabla(datos)

    def recargar_tabla(self, datos_externos=None):
        """Función central para obtener datos y refrescar la tabla"""
        if datos_externos is not None:
            datos = datos_externos
        else:
            # Si no hay datos externos, consultamos a la BD con los filtros actuales
            datos = Controlador.mostrar(texto_busqueda=self.texto_busqueda, orden=self.orden_actual)
        
        self.llenar_tabla(datos)

    def llenar_tabla(self, lista_salas):
        """Toma una lista de datos y reconstruye SOLO las filas de la tabla"""
        
        # 1. Limpiamos el contenedor viejo
        self.contenedor_lista_salas.controls.clear()

        # 2. Si no hay resultados
        if not lista_salas and self.texto_busqueda:
            self.contenedor_lista_salas.controls.append(
                ft.Container(
                    ft.Text(f"No se encontraron salas para '{self.texto_busqueda}'.", color="grey"), 
                    alignment=ft.alignment.center, padding=20
                )
            )
            self.update()
            return

        # 3. Generamos las filas visuales
        for fila in lista_salas:
            id_sala, nombre_sala, capacidad = fila[0], fila[1], fila[2]

            btn_edit = ft.IconButton(
                ft.Icons.EDIT, icon_color="#1B1A1A", 
                on_click=lambda e, i=id_sala, n=nombre_sala, c=capacidad: self.abrir_dialogo_editar(i, n, str(c))
            )
            btn_del = ft.IconButton(
                ft.Icons.DELETE, icon_color="red", 
                on_click=lambda e, i=id_sala, n=nombre_sala: self.abrir_dialogo_borrar(i, n)
            )

            nueva_fila = ft.Column([
                ft.Row([
                    ft.Container(content=ft.Text(nombre_sala, weight="bold", size=14, color="#555555"), expand=2, padding=ft.padding.only(left=20)),
                    ft.Container(content=ft.Text(str(capacidad), weight="bold", color="#555555"), expand=1),
                    ft.Container(content=ft.Row([btn_edit, btn_del], spacing=0), expand=1),
                ], alignment="spaceBetween"),
                ft.Divider(height=1, color="#F0F0F0") 
            ])
            
            self.contenedor_lista_salas.controls.append(nueva_fila)

        self.update()

 

    def limpiar_busqueda(self, e):
        self.texto_busqueda = ""
        self.orden_actual = None
        self.buscador.value = "" # Limpiar visualmente el input
        
        # Resetear icono
        self.icono_orden_btn.icon = ft.Icons.SORT_BY_ALPHA
        self.icono_orden_btn.update()
        
        self.recargar_tabla()

    def alternar_orden(self, e):
        if self.orden_actual is None:
            self.orden_actual = "nombre_asc"
            self.icono_orden_btn.icon = ft.Icons.SORT_BY_ALPHA_ROUNDED # Icono activo
        else:
            self.orden_actual = None
            self.icono_orden_btn.icon = ft.Icons.SORT_BY_ALPHA # Icono normal
        
        self.icono_orden_btn.update() 
        self.recargar_tabla()


    def mostrar_dialogo_error(self, mensaje, dialogo_a_mantener=None):
        def on_aceptar_error(e):
            self.page.close(dialogo_error) 
            if dialogo_a_mantener:
                self.page.open(dialogo_a_mantener) 

        dialogo_error = ft.AlertDialog(
            title=ft.Text("Error de Validación"),
            content=ft.Text(mensaje),
            actions=[ft.TextButton("Aceptar", on_click=on_aceptar_error)]
        )
        
        if dialogo_a_mantener:
            self.page.close(dialogo_a_mantener)
             
        self.page.open(dialogo_error)
    
    def abrir_dialogo_borrar(self, id_sala, nombre):
        def callback_reload(e):
            self.page.close(self.dialogo)
            self.recargar_tabla()

        self.dialogo = ft.AlertDialog(
            title=ft.Text("Eliminar Sala"),
            content=ft.Text(f"¿Eliminar '{nombre}'?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.page.close(self.dialogo)),
                ft.TextButton("Eliminar", style=ft.ButtonStyle(color="red"), 
                              on_click=lambda e: Controlador.eliminar(id_sala, self.page, callback_reload))
            ]
        )
        self.page.open(self.dialogo)

    def abrir_dialogo_agregar(self):
        self.edit_nombre = ft.TextField(label="Nombre")
        self.edit_capacidad = ft.TextField(label="Capacidad", keyboard_type=ft.KeyboardType.NUMBER)
        
        def callback_reload(e):
            self.page.close(self.dialogo)
            self.recargar_tabla()

        def agregar_sala_submit(e):
            # (Tu lógica de validación original...)
            nombre = self.edit_nombre.value.strip()
            capacidad = self.edit_capacidad.value.strip()
            
            # ... validaciones simplificadas para el ejemplo ...
            if not nombre or not capacidad:
                self.mostrar_dialogo_error("Campos obligatorios", self.dialogo)
                return

            try:
                capacidad_int = int(capacidad)
            except:
                self.mostrar_dialogo_error("Capacidad debe ser número", self.dialogo)
                return
            
            Controlador.agregar(nombre.upper(), capacidad_int, self.page, callback_reload)

        self.dialogo = ft.AlertDialog(
            title=ft.Text("Agregar Sala"),
            content=ft.Container(height=150, content=ft.Column([self.edit_nombre, self.edit_capacidad])),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.page.close(self.dialogo)),
                ft.ElevatedButton("Agregar", on_click=agregar_sala_submit)
            ]
        )
        self.page.open(self.dialogo)

    def abrir_dialogo_editar(self, id, nombre, capacidad):
        self.edit_nombre = ft.TextField(label="Nombre", value=nombre)
        self.edit_capacidad = ft.TextField(label="Capacidad", value=str(capacidad), keyboard_type=ft.KeyboardType.NUMBER)
        
        def callback_reload(e):
            self.page.close(self.dialogo)
            self.recargar_tabla()

        def actualizar_sala_submit(e):
            nombre_nuevo = self.edit_nombre.value.strip()
            cap_nuevo = self.edit_capacidad.value.strip()
            
            # ... validaciones ...
            try:
                cap_int = int(cap_nuevo)
                Controlador.modificar(id, nombre_nuevo.upper(), cap_int, self.page, callback_reload)
            except:
                self.mostrar_dialogo_error("❌ Error en datos", self.dialogo)

        self.dialogo = ft.AlertDialog(
            title=ft.Text("Editar Sala"),
            content=ft.Container(height=150, content=ft.Column([self.edit_nombre, self.edit_capacidad])),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.page.close(self.dialogo)),
                ft.ElevatedButton("Actualizar", on_click=actualizar_sala_submit)
            ]
        )
        self.page.open(self.dialogo)