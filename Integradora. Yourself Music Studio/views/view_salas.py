import flet as ft
from Controlador.controlador_salas import Controlador
from Views.Vistas_Base import VistaBase

# Clase Vistas
class VistasSalas(VistaBase):
    def __init__(self, page: ft.Page):
        self.PURPLE = "#A11F1F"
        self.ORANGE = "#FF9F43"
        self.BG_COLOR = "#F4F5F9"
        self.page = page
        self.texto_busqueda = "" # Variable para mantener el estado de búsqueda
        
        # Configuración inicial de la página
        self.page.title = "Gestion de salas"
        self.page.bgcolor = self.BG_COLOR
        self.page.window_width = 1000
        self.page.window_height = 700
        Tabla= self.mostrar_tabla()
        super().__init__( page,"/inicio", "Inicio", 0, Tabla)


    # FUNCIÓN PARA MOSTRAR ERRORES DE VALIDACIÓN
    def mostrar_dialogo_error(self, mensaje):
        dialogo_error = ft.AlertDialog(
            title=ft.Text("Error de Validación"),
            content=ft.Text(mensaje),
            actions=[
                ft.TextButton("Aceptar", on_click=lambda e: (
                    setattr(dialogo_error, "open", False),
                    self.page.update()
                ))
            ]
        )
        self.page.dialog = dialogo_error
        dialogo_error.open = True
        self.page.update()
    
    # FUNCIÓN DE BÚSQUEDA: Se ejecuta al presionar Enter
    def buscar(self, e):
        # Actualiza la variable de búsqueda y recarga la tabla
        self.texto_busqueda = e.control.value.strip()
        self.recargar_tabla()
    
    #Ventana emergente de borrar
    def abrir_dialogo_borrar(self,id_sala, nombre):
        self.dialogo = ft.AlertDialog(
            title=ft.Text("Borrar Sala"),
            content=ft.Text(f"¿Eliminar '{nombre}'?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.page.close(self.dialogo)),
                ft.TextButton("Eliminar", style=ft.ButtonStyle(color="red"),on_click=lambda e: (
                            Controlador.eliminar(id_sala, self.page), 
                            self.page.close(self.dialogo),
                            self.recargar_tabla()))
            ],) 
        self.page.open(self.dialogo)

    #Ventana emergente de agregar
    def abrir_dialogo_agregar(self):
        self.edit_nombre = ft.TextField(label="Nombre")
        self.edit_capacidad = ft.TextField(label="Capacidad (Solo Enteros)", keyboard_type=ft.KeyboardType.NUMBER)
        
        # Handler para el botón Agregar
        def agregar_sala(e):
            nombre = self.edit_nombre.value.strip()
            capacidad = self.edit_capacidad.value.strip()

            # Validación de campos vacíos
            if not nombre or not capacidad:
                self.mostrar_dialogo_error("❌ Ambos campos (Nombre y Capacidad) son obligatorios.")
                return

            # Validación numérica (entero positivo)
            try:
                capacidad_int = int(capacidad)
                if capacidad_int <= 0:
                    self.mostrar_dialogo_error("❌ La capacidad debe ser un número entero positivo.")
                    return
            except ValueError:
                self.mostrar_dialogo_error("❌ La capacidad debe ser un número entero válido.")
                return

            # Conversión a mayúsculas
            nombre_mayusculas = nombre.upper()

            Controlador.agregar(nombre_mayusculas, capacidad_int, self.page)
            self.page.close(self.dialogo)
            self.recargar_tabla()

        self.dialogo = ft.AlertDialog(
            title=ft.Text("Agregar Sala"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.page.close(self.dialogo)),
                ft.ElevatedButton("Agregar", on_click=agregar_sala) 
            ],
            content=ft.Container(width=500,  
            height=200, 
            padding=10,
            alignment=ft.alignment.center,
            content=ft.Column(
                [self.edit_nombre, ft.Row([self.edit_capacidad,])],
                height=150, tight=True
            ),
        ))
        self.page.open(self.dialogo)

    #Ventana emergente de editar
    def abrir_dialogo_editar(self,id, nombre, capacidad): 
        self.edit_nombre = ft.TextField(label="Nombre", value=nombre)
        self.edit_capacidad = ft.TextField(label="Capacidad (Solo Enteros)", value=capacidad, keyboard_type=ft.KeyboardType.NUMBER)
        
        # Handler para el botón Actualizar
        def actualizar_sala(e):
            nombre_nuevo = self.edit_nombre.value.strip()
            capacidad_nueva = self.edit_capacidad.value.strip()

            # Validación de campos vacíos
            if not nombre_nuevo or not capacidad_nueva:
                self.mostrar_dialogo_error("❌ Ambos campos (Nombre y Capacidad) son obligatorios.")
                return
            
            # Validación numérica (entero positivo)
            try:
                capacidad_int = int(capacidad_nueva)
                if capacidad_int <= 0:
                    self.mostrar_dialogo_error("❌ La capacidad debe ser un número entero positivo.")
                    return
            except ValueError:
                self.mostrar_dialogo_error("❌ La capacidad debe ser un número entero válido.")
                return

            # Conversión a mayúsculas
            nombre_mayusculas = nombre_nuevo.upper()

            Controlador.modificar(id, nombre_mayusculas, capacidad_int, self.page)
            self.page.close(self.dialogo)
            self.recargar_tabla()

        self.dialogo = ft.AlertDialog(
            title=ft.Text("Editar Sala"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.page.close(self.dialogo)),
                ft.ElevatedButton("Actualizar", on_click=actualizar_sala) 
            ],
            content=ft.Container(width=500,
            height=200, 
            padding=10,
            alignment=ft.alignment.center,
            content=ft.Column(
                [self.edit_nombre, ft.Row([self.edit_capacidad])],
                height=150, tight=True
            ),
        ))
        self.page.open(self.dialogo)

    def mostrar_tabla(self):
        # Obtiene la lista de salas filtrada (o completa si texto_busqueda está vacío)
        lista_salas=Controlador.mostrar(self.texto_busqueda)

        # A. BARRA SUPERIOR
        buscador = ft.TextField(
            hint_text="Buscar por Nombre (presione Enter para buscar/borrar)...", 
            prefix_icon=ft.Icons.SEARCH,
            border_radius=10,
            bgcolor="white",
            border_color="transparent",
            expand=True,
            value=self.texto_busqueda,
            # SOLUCIÓN: Usamos on_submit (al presionar Enter)
            on_submit=self.buscar 
        )

        btn_agregar = ft.ElevatedButton(
            text="Agregar Nuevo",
            icon=ft.Icons.ADD,
            bgcolor="#A11F1F",
            color="white",
            height=45,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            on_click=lambda e:self.abrir_dialogo_agregar()
        )

        contenedor_header = ft.Container(
            content=ft.Row([buscador, btn_agregar], spacing=20),
            padding=20,
            bgcolor="#F9F9F9"
        )

        # B. ENCABEZADOS
        titulos = ["NOMBRE", "CAPACIDAD", "ACCIONES"]
        anchos = [2, 1, 1, ] 
        
        fila_encabezados = ft.Row(
            controls=[
                ft.Container(content=ft.Text(t, color="grey", size=12, weight="bold"), expand=a) 
                for t, a in zip(titulos, anchos)
            ]
        )

        contenedor_titulos = ft.Container(
            content=fila_encabezados,
            padding=ft.padding.symmetric(horizontal=20, vertical=15),
            bgcolor="white",
            border=ft.border.only(bottom=ft.border.BorderSide(1, "#E0E0E0"))
        )

        filas_visuales = [] 

        for fila in lista_salas:
            id_sala = fila[0]
            nombre_sala = fila[1]
            capacidad = fila[2]

            btn_edit = ft.IconButton(
                ft.Icons.EDIT,
                icon_color="#1B1A1A", 
                on_click=lambda e,i=id_sala,n=nombre_sala, c=capacidad,: self.abrir_dialogo_editar(i,n, str(c))
            )
            btn_del = ft.IconButton(ft.Icons.DELETE, icon_color="red", on_click=lambda e, i=id_sala, n=nombre_sala : self.abrir_dialogo_borrar(i,n))

            nueva_fila = ft.Column([
                ft.Row([
                    ft.Container(content=ft.Text(nombre_sala, weight="bold", size=14), expand=2),
                    ft.Container(content=ft.Text(capacidad, weight="bold"), expand=1),
                    ft.Container(content=ft.Row([btn_edit, btn_del], spacing=0), expand=1),
                ], alignment="spaceBetween"),
                ft.Divider(height=1, color="#F0F0F0") 
            ])
        
            filas_visuales.append(nueva_fila)

        # D. CONTENEDOR FINAL
        if not filas_visuales and self.texto_busqueda:
            contenido = ft.Column(
                controls=[ft.Container(ft.Text(f"No se encontraron salas para '{self.texto_busqueda}'.", color="grey"), alignment=ft.alignment.center, padding=20)],
                expand=True
            )
        else:
            contenido = ft.Column(
                controls=filas_visuales, 
                scroll=ft.ScrollMode.AUTO, 
                expand=True, )

        cuerpo_tabla = ft.Container(
            content=ft.Column([
                contenedor_titulos,      
                contenido                
            ], spacing=0, expand=True),
            bgcolor="white",
            border_radius=15,
            margin=20,
            alignment=ft.alignment.center,
            expand=True,
            shadow=ft.BoxShadow(blur_radius=10, color="#1A000000")
        )

        return ft.Column([contenedor_header, cuerpo_tabla], spacing=0, expand=True)
        #self.page.add(Tabla)

    def recargar_tabla(self):
        self.page.controls.clear()
        self.mostrar_tabla()
        self.page.update()