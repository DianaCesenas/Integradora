import flet as ft

class ClienteView:
    def __init__(self, page, controller):
        self.page = page
        self.controller = controller
        
    
        self.COLOR_VINO = "#A11F1F"
        self.COLOR_FONDO = "#F4F5F9"
        
        
        self.columna_con_lista_clientes = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

        
        self.campo_nombre = ft.TextField(label="Nombre", expand=True)
        self.campo_apellido = ft.TextField(label="Apellido", expand=True)
        
        self.campo_telefono = ft.TextField(label="Teléfono", expand=True)
        self.campo_email = ft.TextField(label="Email", expand=True)
        
        self.campo_calle = ft.TextField(label="Calle", expand=2)
        self.campo_numero = ft.TextField(label="Número", expand=1)
        self.campo_colonia = ft.TextField(label="Colonia", expand=3)
        
       
        self.ventana_emergente = None

    
   
    

    def mostrar_formulario_agregar(self, evento):
        self.campo_nombre.value = ""
        self.campo_apellido.value = ""
        self.campo_telefono.value = ""
        self.campo_email.value = ""
        self.campo_calle.value = ""
        self.campo_numero.value = ""
        self.campo_colonia.value = ""
        
        
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
                ft.ElevatedButton("Guardar", bgcolor=self.COLOR_VINO, color="white", on_click=self.boton_guardar_click)
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
                                  on_click=lambda e: self.boton_actualizar_click(id_cli))
            ]
        )
        self.page.open(self.ventana_emergente)

    def mostrar_confirmacion_borrar(self, id_cliente, nombre_completo):
        self.ventana_emergente = ft.AlertDialog(
            title=ft.Text("Eliminar Cliente"),
            content=ft.Text(f"¿Estás seguro de que quieres borrar a '{nombre_completo}'?"),
            actions=[
                ft.TextButton("Cancelar", on_click=self.cerrar_ventana),
                ft.TextButton("Sí, Eliminar", style=ft.ButtonStyle(color="red"), 
                              on_click=lambda e: self.boton_eliminar_click(id_cliente))
            ]
        )
        self.page.open(self.ventana_emergente)

    def cerrar_ventana(self, evento):
        self.page.close(self.ventana_emergente)

   
    #Aqui se conecta con el controlador
 

    def boton_guardar_click(self, evento):
        datos = [
            self.campo_nombre.value, self.campo_apellido.value,
            self.campo_telefono.value, self.campo_email.value,
            self.campo_calle.value, self.campo_numero.value, self.campo_colonia.value
        ]
        self.cerrar_ventana(None)
        self.controller.crear_cliente(datos)

    def boton_actualizar_click(self, id_cliente):
        datos = [
            self.campo_nombre.value, self.campo_apellido.value,
            self.campo_telefono.value, self.campo_email.value,
            self.campo_calle.value, self.campo_numero.value, self.campo_colonia.value
        ]
        self.cerrar_ventana(None)
        self.controller.actualizar_cliente(id_cliente, datos)

    def boton_eliminar_click(self, id_cliente):
        self.cerrar_ventana(None)
        self.controller.eliminar_cliente(id_cliente)

    #Aqui se dibuja la pantalla :P
    

    def inicializar(self, contenedor_destino=None):
        
        destino = contenedor_destino if contenedor_destino else self.page

        #Header 
        campo_buscador = ft.TextField(
        hint_text="Buscar por nombre, apellido o teléfono...", 
        prefix_icon=ft.Icons.SEARCH, 
        border_radius=10, 
        bgcolor="white", 
        expand=True,
        on_change=lambda e: self.controller.buscar_cliente(e.control.value)
    )
        
        boton_nuevo = ft.ElevatedButton("Nuevo Cliente", icon=ft.Icons.ADD, 
                                        bgcolor=self.COLOR_VINO, color="white", height=45,
                                        on_click=self.mostrar_formulario_agregar)
        
        contenedor_header = ft.Container(
            content=ft.Row([campo_buscador, boton_nuevo]), 
            padding=20, 
            bgcolor="#F9F9F9"
        )

        # Encabezados
        lista_titulos = ["NOMBRE COMPLETO", "TELÉFONO", "EMAIL", "DIRECCIÓN (Calle, #, Col)", "ACCIONES"]
        anchos_columnas = [2, 1, 2, 2, 1] 
        
        controles_titulos = []
        for titulo, ancho in zip(lista_titulos, anchos_columnas):
            controles_titulos.append(ft.Container(content=ft.Text(titulo, weight="bold", color="grey"), expand=ancho))

        fila_encabezados = ft.Row(controls=controles_titulos)
        
        # Contenedor 
        tarjeta_tabla = ft.Container(
            content=ft.Column([
                # Títulos
                ft.Container(content=fila_encabezados, padding=20, border=ft.border.only(bottom=ft.border.BorderSide(1, "#E0E0E0"))),
                # Lista desplazable de clientes
                self.columna_con_lista_clientes
            ], spacing=0, expand=True),
            
            bgcolor="white", border_radius=15, margin=20, expand=True, shadow=ft.BoxShadow(blur_radius=5, color="#1A000000")
        )

        # Unimos todo el contenido
        contenido_total = ft.Column([contenedor_header, tarjeta_tabla], spacing=0, expand=True)
        
        
        if isinstance(destino, ft.Column): 
            
            destino.controls.clear()
            destino.controls.append(contenido_total)
            destino.update()
        else:
          
            destino.add(contenido_total)

   
    #Aqui se conecta con la bd
  

    def cargar_filas(self, lista_datos_bd):
     
        self.columna_con_lista_clientes.controls.clear()
        
        for fila in lista_datos_bd:
            
            id_bd, nom, ape, tel, mail, calle, num, col = fila
            
           
            nombre_completo = f"{nom} {ape}"
            direccion_completa = f"{calle} #{num}, {col}"

    
            boton_editar = ft.IconButton(
                icon=ft.Icons.EDIT, 
                icon_color="blue", 
                tooltip="Editar",
             
                on_click=lambda e, i=id_bd, n=nom, a=ape, t=tel, m=mail, c=calle, nu=num, co=col: 
                    self.mostrar_formulario_editar(i, n, a, t, m, c, nu, co)
            )
            
            boton_borrar = ft.IconButton(
                icon=ft.Icons.DELETE, 
                icon_color="red", 
                tooltip="Borrar",
                on_click=lambda e, i=id_bd, n=nombre_completo: self.mostrar_confirmacion_borrar(i, n)
            )

            fila_botones = ft.Row([boton_editar, boton_borrar], spacing=0, alignment=ft.MainAxisAlignment.START)

            fila_visual = ft.Column([
                ft.Row([
                    ft.Container(ft.Text(nombre_completo, weight="bold"), expand=2),
                    ft.Container(ft.Text(tel), expand=1),
                    ft.Container(ft.Text(mail), expand=2),
                    ft.Container(ft.Text(direccion_completa, size=12), expand=2),
                    ft.Container(fila_botones, expand=1)
                ], alignment="spaceBetween", vertical_alignment=ft.CrossAxisAlignment.CENTER),
                
                ft.Divider(height=1, color="#F0F0F0")
            ])
            
            self.columna_con_lista_clientes.controls.append(
                ft.Container(fila_visual, padding=ft.padding.symmetric(horizontal=20, vertical=5))
            )
        
       
        if self.page: self.page.update()