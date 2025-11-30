import flet as ft
from database import Database
from views.menu_view import MenuView
from controllers.cliente_controller import ClienteController
#Aqui ustedes tienen que importar sus controladores:)

def main(page: ft.Page):
   
    page.title = "Yourself Music Studio"
    page.bgcolor = "#F4F5F9"
    page.window_min_width = 1000
    page.window_min_height = 700

   
    try:
        db = Database()
    except Exception as e:
        page.add(ft.Text(f"Error Fatal de Conexión: {e}", color="red", size=20))
        return

    
    contenedor_principal = ft.Column(expand=True)
    
 
    btn_home = ft.IconButton(ft.Icons.HOME, tooltip="Volver al Menú", 
                             visible=False, on_click=lambda _: mostrar_menu())
    
    header_app = ft.Container(
        content=ft.Row([
            ft.Row([btn_home, ft.Text("Yourself Music Studio", weight="bold", size=18)]),
            ft.Icon(ft.Icons.ACCOUNT_CIRCLE, color="grey")
        ], alignment="spaceBetween"),
        padding=15, bgcolor="white", 
        border=ft.border.only(bottom=ft.border.BorderSide(1, "#E0E0E0"))
    )

 
    page.add(ft.Column([header_app, contenedor_principal], expand=True, spacing=0))



    def activar_boton_home(activo):
        btn_home.visible = activo
        header_app.update()

    def ir_a_clientes(e=None):
        activar_boton_home(True)
        
        controller = ClienteController(page, db, contenedor_principal)
        controller.iniciar_modulo()

    def ir_a_instrumentos(e=None):
        activar_boton_home(True)
        pass

    def ir_a_salas(e=None):
        pass

    def ir_a_reservas(e=None):
        pass

    
    def mostrar_menu(e=None):
        activar_boton_home(False)
        
        menu = MenuView(page, ir_a_clientes, ir_a_instrumentos, ir_a_salas, ir_a_reservas)
        menu.inicializar(contenedor_principal)


    mostrar_menu()

if __name__ == "__main__":
    ft.app(target=main)