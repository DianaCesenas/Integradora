import flet as ft
from Controlador.cliente_controller import ClienteController
from Views.Vistas_Base import VistaBase # Asegúrate de que este import sea correcto

class ClienteView(VistaBase):
    def __init__(self, page, db):
        # 1. Configuración básica
        self.page = page
        self.db = db
        self.COLOR_VINO = "#A11F1F"
        self.COLOR_FONDO = "#F4F5F9"
        self._inicializar_campos_formulario()
        
        self.columna_con_lista_clientes = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        self.controller = ClienteController(page, db, self)
        contenido_visual = self._construir_interfaz()
        super().__init__(self.page, "/gestion_clientes", "Gestionar clientes", 1, contenido_visual) 
        self.controls = [contenido_visual]


    def did_mount(self):
        self.controller.cargar_datos()
    
    def buscar(self, e):
        self.recargar_tabla()
    
    # FUNCIÓN DE LIMPIEZA/RECARGA
    def limpiar_busqueda(self, e):
        self.texto_busqueda = ""  # Resetea la variable de búsqueda
        self.orden_actual = None  # Resetea el orden
        self.recargar_tabla()

    def _inicializar_campos_formulario(self):
        """Define los TextFields para no ensuciar el __init__"""
        self.campo_nombre = ft.TextField(label="Nombre", expand=True)
        self.campo_apellido = ft.TextField(label="Apellido", expand=True)
        self.campo_telefono = ft.TextField(label="Teléfono", expand=True)
        self.campo_email = ft.TextField(label="Email", expand=True)
        self.campo_calle = ft.TextField(label="Calle", expand=2)
        self.campo_numero = ft.TextField(label="Número", expand=1)
        self.campo_colonia = ft.TextField(label="Colonia", expand=3)
        self.ventana_emergente = None
        self.texto_busqueda = "" 
        self.orden_actual = None  

    def _construir_interfaz(self):
        """Crea el layout principal: Header + Tabla"""
        
        campo_buscador = ft.TextField(
            hint_text="Buscar por nombre, apellido o teléfono...", 
            prefix_icon=ft.Icons.SEARCH, 
            border_radius=10,
            border_width=0.5,      
            border_color="#2B2B2B",    
            bgcolor="white", 
            expand=True,
            on_change=lambda e: self.controller.buscar_cliente(e.control.value)            
        
        )
        
        btn_limpiar = ft.Container(
            content=ft.IconButton(
                ft.Icons.REFRESH,
                icon_color="#2B2B2B",
                tooltip="Recargar y Mostrar todas las salas",
                on_click=self.limpiar_busqueda 
            ),
            bgcolor="#BBC3CB", 
            border_radius=10,
            height=45,
            alignment=ft.alignment.center
        )

        def alternar_orden(e):
            # Cambia el estado: Si es None, pasa a ordenar; si está ordenado, vuelve a None.
            if self.orden_actual is None:
                self.orden_actual = "nombre_asc"
            else:
                self.orden_actual = None
            self.recargar_tabla()

        # 4. Botón de Ordenar (Ícono de rayitas o clasificación)
        icono_orden = ft.Icons.SORT_BY_ALPHA 
        if self.orden_actual == "nombre_asc":
            icono_orden = ft.Icons.SORT_BY_ALPHA_ROUNDED # Ícono para indicar que está activo (ordenado A-Z)

        btn_ordenar = ft.Container(
            content=ft.IconButton(
                icono_orden, 
                icon_color="#2B2B2B",
                tooltip="Ordenar por Nombre (A-Z) / Quitar Orden",
                on_click=alternar_orden
            ),
            bgcolor="#BBC3CB",#A11F1F", 
            border_radius=10,
            height=45,
            alignment=ft.alignment.center
            )

        # 5. Botón Agregar
        btn_agregar = ft.ElevatedButton(
            text="Agregar Nuevo",
            icon=ft.Icons.ADD,
            bgcolor="#CBD0D5", #"#8ACCFF"#A6BFD1,"#B1BFC9",#B4BBC0
            color="#2B2B2B",
            height=45,
            expand=True,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            on_click=lambda e:self.mostrar_formulario_agregar()
        )

        
        contenedor_header = ft.Container(
            content=ft.Column( 
                [
                    # 🔑 INCLUSIÓN: Se añade btn_ordenar a la barra de búsqueda
                    ft.Row([campo_buscador, btn_limpiar, btn_ordenar], spacing=10), 
                    ft.Row([btn_agregar], spacing=10)
                ],
                spacing=10
            ), 
            padding=20,
            bgcolor="#F9F9F9"
        )

        lista_titulos = ["Nombre completo ", "Teléfono", "Email", "Dirección (Calle, #, Col)", "Aciones"]
        anchos_columnas = [2, 1, 2, 2, 1] 
        
        controles_titulos = []
        for titulo, ancho in zip(lista_titulos, anchos_columnas):
            controles_titulos.append(ft.Container(content=ft.Text(titulo, weight="bold", color="#2B2B2B"), expand=ancho))

        fila_encabezados = ft.Row(controls=controles_titulos)
        
        tarjeta_tabla = ft.Container(
            content=ft.Column([
                ft.Container(content=fila_encabezados, padding=20, border=ft.border.only(bottom=ft.border.BorderSide(1, "#E0E0E0"))),
                self.columna_con_lista_clientes 
            ], spacing=0, expand=True),
            
            bgcolor="white", border_radius=15, margin=20, expand=True, shadow=ft.BoxShadow(blur_radius=5, color="#1A000000")
        )

        return ft.Column([contenedor_header, tarjeta_tabla], spacing=0, expand=True)



    def cargar_filas(self, lista_datos_bd):
        """Recibe una lista de datos (tuplas) y dibuja las filas"""
        self.columna_con_lista_clientes.controls.clear()
        
        for fila in lista_datos_bd:
            id_bd, nom, ape, tel, mail, calle, num, col = fila
            
            nombre_completo = f"{nom} {ape}"
            direccion_completa = f"{calle} #{num}, {col}"

            boton_editar = ft.IconButton(
                icon=ft.Icons.EDIT, icon_color="blue", tooltip="Editar",
                on_click=lambda e, i=id_bd, n=nom, a=ape, t=tel, m=mail, c=calle, nu=num, co=col: 
                    self.mostrar_formulario_editar(i, n, a, t, m, c, nu, co)
            )
            
            boton_borrar = ft.IconButton(
                icon=ft.Icons.DELETE, icon_color="red", tooltip="Borrar",
                on_click=lambda e, i=id_bd, n=nombre_completo: self.mostrar_confirmacion_borrar(i, n)
            )

            fila_visual = ft.Column([
                ft.Row([
                    ft.Container(ft.Text(nombre_completo, weight="bold"), expand=2),
                    ft.Container(ft.Text(tel), expand=1),
                    ft.Container(ft.Text(mail), expand=2),
                    ft.Container(ft.Text(direccion_completa, size=12), expand=2),
                    ft.Container(ft.Row([boton_editar, boton_borrar], spacing=0), expand=1)
                ], alignment="spaceBetween", vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Divider(height=1, color="#F0F0F0")
            ])
            
            self.columna_con_lista_clientes.controls.append(
                ft.Container(fila_visual, padding=ft.padding.symmetric(horizontal=20, vertical=5))
            )
        
        self.update()


    
    def mostrar_formulario_agregar(self):
        for campo in [self.campo_nombre, self.campo_apellido, self.campo_telefono, 
                      self.campo_email, self.campo_calle, self.campo_numero, self.campo_colonia]:
            campo.value = ""
        
        self.ventana_emergente = ft.AlertDialog(
            title=ft.Text("Nuevo Cliente"),
            content=ft.Column([
                ft.Row([self.campo_nombre, self.campo_apellido]),
                ft.Row([self.campo_telefono, self.campo_email]),
                ft.Row([self.campo_calle, self.campo_numero]),
                self.campo_colonia
            ], height=300, tight=True),
            actions=[
                ft.TextButton("Cancelar", on_click=self.cerrar_ventana),
                ft.ElevatedButton("Guardar", bgcolor=self.COLOR_VINO, color="white", on_click=self._evento_guardar)
            ]
        )
        self.page.open(self.ventana_emergente)

    def mostrar_formulario_editar(self, id_cli, nom, ape, tel, mail, calle, num, col):
        self.campo_nombre.value = nom
        self.campo_apellido.value = ape
        self.campo_telefono.value = tel
        self.campo_email.value = mail
        self.campo_calle.value = calle
        self.campo_numero.value = num
        self.campo_colonia.value = col

        self.ventana_emergente = ft.AlertDialog(
            title=ft.Text("Editar Cliente"),
            content=ft.Column([
                ft.Row([self.campo_nombre, self.campo_apellido]),
                ft.Row([self.campo_telefono, self.campo_email]),
                ft.Row([self.campo_calle, self.campo_numero]),
                self.campo_colonia
            ], height=300, tight=True),
            actions=[
                ft.TextButton("Cancelar", on_click=self.cerrar_ventana),
                ft.ElevatedButton("Actualizar", bgcolor=self.COLOR_VINO, color="white", 
                                  on_click=lambda e: self._evento_actualizar(id_cli))
            ]
        )
        self.page.open(self.ventana_emergente)

    def mostrar_confirmacion_borrar(self, id_cliente, nombre):
        self.ventana_emergente = ft.AlertDialog(
            title=ft.Text("Eliminar Cliente"),
            content=ft.Text(f"¿Borrar a '{nombre}'?"),
            actions=[
                ft.TextButton("Cancelar", on_click=self.cerrar_ventana),
                ft.TextButton("Sí, Eliminar", style=ft.ButtonStyle(color="red"), 
                              on_click=lambda e: self._evento_eliminar(id_cliente))
            ]
        )
        self.page.open(self.ventana_emergente)

    def cerrar_ventana(self, e):
        self.page.close(self.ventana_emergente)


   
    def _recolectar_datos_formulario(self):
        return [
            self.campo_nombre.value, self.campo_apellido.value,
            self.campo_telefono.value, self.campo_email.value,
            self.campo_calle.value, self.campo_numero.value, self.campo_colonia.value
        ]

    def _evento_guardar(self, e):
        datos = self._recolectar_datos_formulario()
        self.cerrar_ventana(None)
        self.controller.crear_cliente(datos)

    def _evento_actualizar(self, id_cliente):
        datos = self._recolectar_datos_formulario()
        self.cerrar_ventana(None)
        self.controller.actualizar_cliente(id_cliente, datos)

    def _evento_eliminar(self, id_cliente):
        self.cerrar_ventana(None)
        self.controller.eliminar_cliente(id_cliente)