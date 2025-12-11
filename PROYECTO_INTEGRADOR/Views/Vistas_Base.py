import flet as ft
#from Controlador import controlador

#La clase vistaBase hereda de ft.View porque trabajaremops con rutas para navegar entre las diferentes vistas 
#Basicamente esto hace que en lugar de ser una page con botones y elemntos sueltos sea una hoja contenedora
class VistaBase(ft.View):
    COLOR = "#A11F1F"
    BG_COLOR = "#F4F5F9"
    def __init__(self,page, ruta, titulo, indice_drawer, contenido_vista):
        #Como heredamos de view, automaticamente tiene el parametro de route aqui solo renombramos que route es ruta 
        super().__init__(route=ruta)
        self.page=page
        self.page.title = "Studio Yourself Music"
        self.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.bgcolor = self.BG_COLOR
        self.padding = 20
        #Creamos la barra superior  
        #self.appbar=ft.AppBar(title=ft.Text(titulo),bgcolor=self.COLOR,color="#FFFFFF") 
        self.appbar = ft.AppBar(title=ft.Text(titulo),
          center_title=False,
          actions=[
               ft.Container(
                    content=ft.Image(
                         src="logo2.png", 
                         fit=ft.ImageFit.COVER,
                    ),
                    height=75, # Tamaño de la imagen
                    border_radius=ft.border_radius.all(8), # Redondeo
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                    margin=ft.margin.only(right=15), 
               ),
          ],
          color="#FFFFFF",
          bgcolor="#992626", # Tu color rojo
          )
               #Creamos el menmu latera y lo renombramos 
        self.drawer=self.crearMenuLateral(indice_drawer)
        #Agregamos el contenido que resulto de las otras vistas a la pagina principal que es view 
        self.controls=[contenido_vista]
        #self.page.on_route_change=self.cambiar_vista
        #self.page.go("/")

     #Si hay cambio de ruta o de que se muestra cuando se cambia de opcion en el menu lateral se cambia aqui
    
        
    #El menu lateral se maneja por indices y como manejaremos con rutas estamos incdicandon que cuando haya cmabio de indice 
    #se vaya a la ruta de inicio y con  la funcion cambiar vista le decimos qeu cuando este en esa ruta se ejecuten las clases donde estan las demas vistas 
    def navegacionDeMenuLateral(self, e):
          """Traduce el click del drawer a una Ruta URL"""
          indice = e.control.selected_index
          if indice == 0:
               self.page.go("/inicio")
          elif indice == 1:
               self.page.go("/gestion_clientes")
          elif indice == 2:
               self.page.go("/gestion_reservas")
          elif indice == 3:
               self.page.go("/salass")
          elif indice == 4:
               self.page.go("/reservas")
          elif indice == 5:
               self.page.go("/perfil")
            
            
    #Crear menu lateral
    def crearMenuLateral(self,indice_seleccionado):
          return ft.NavigationDrawer(
               selected_index=indice_seleccionado,
               on_change=self.navegacionDeMenuLateral,
               controls=[
               ft.NavigationDrawerDestination(
                    icon=ft.Icons.HOME_OUTLINED,
                    selected_icon=ft.Icons.HOME,
                    label="Inicio"),#Indice 0
               ft.NavigationDrawerDestination(
                    icon=ft.Icons.PEOPLE_OUTLINED,
                    selected_icon=ft.Icons.PEOPLE,
                    label="Gestion de clientes"
               ),
               ft.NavigationDrawerDestination(
                    icon=ft.Icons.DATE_RANGE_OUTLINED,
                    selected_icon=ft.Icons.DATE_RANGE,
                    label="Gestion de reservas"
               ),
               ft.NavigationDrawerDestination(
                    icon=ft.Icons.MEETING_ROOM_OUTLINED,
                    selected_icon=ft.Icons.MEETING_ROOM,
                    label="Gestion de salas"
               ),
               ft.Divider(),
               ft.NavigationDrawerDestination(
                    icon=ft.Icons.ACCOUNT_BOX_OUTLINED,
                    selected_icon=ft.Icons.ACCOUNT_BOX,
                    label="Reservas"
               ),
               ft.Divider(),
               ft.NavigationDrawerDestination(
                    icon=ft.Icons.ACCOUNT_BOX_OUTLINED,
                    selected_icon=ft.Icons.ACCOUNT_BOX,
                    label="Perfil de usuario"
               ),

               ],
            )
    

