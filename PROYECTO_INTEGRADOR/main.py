import flet as ft
from Views import ruta
import time

def main(page: ft.Page):
    # 1. Configuración Básica
    page.title = "Reserva de Estudios"
    page.padding = 0
    page.bgcolor = ft.Colors.BLUE_GREY_50
    
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_maximized = True
    page.window_top = 0
    page.window_left = 0
    
    splash_logo = ft.Image(
        src="logo2.png", 
        width=300, 
        height=300, 
        fit=ft.ImageFit.CONTAIN
    )
    progress_ring = ft.ProgressRing(width=30, height=30, color="#FFFFFF") # Tu color rojo

    pantalla_splash = ft.Container(
        content=ft.Column(
            controls=[
                splash_logo,
                ft.Container(height=20), 
                progress_ring,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        alignment=ft.alignment.center,
        bgcolor="#992626", 
        expand=True 
    )

    page.add(pantalla_splash)
    page.update()

    time.sleep(4) 

    page.clean()
    page.update()

    def cambio_de_ruta(route):
        page.views.clear()

        try:
            nueva_vista = ruta.obtener_vista(page.route, page)
            
            nueva_vista.vertical_alignment = ft.MainAxisAlignment.CENTER
            nueva_vista.horizontal_alignment = ft.CrossAxisAlignment.CENTER
            nueva_vista.padding = 0
            nueva_vista.bgcolor = ft.Colors.BLUE_GREY_50
            
            page.views.append(nueva_vista)
            page.update()
        except Exception as e:
            print(f"Error cargando vista: {e}")

    page.on_route_change = cambio_de_ruta
    page.on_view_pop = lambda view: page.go(page.views[-1].route)

    page.go("/login")#view=ft.AppView.WEB_BROWSER

ft.app(target=main, assets_dir="assets")