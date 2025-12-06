# Archivo: main.py
import flet as ft
# Solo importamos el enrutador, no las vistas individuales
from Views import ruta
#gestion_reservas y MainReservas

def main(page: ft.Page):
    page.title = "Reserva de Estudios"
    page.window_visible = False 
    page.scroll = None
    page.update()

    # 2. Manda la orden de maximizar
    page.window_maximized = True
    #page.theme_mode = ft.ThemeMode.DARK
    page.update()
    def cambio_de_ruta(route):
        page.views.clear()
        nueva_vista = ruta.obtener_vista(page.route, page)
        page.views.append(nueva_vista)
        page.update()

    # Conectamos la función
    page.on_route_change = cambio_de_ruta
    page.go("/login")
    page.window_visible = True
    page.update()

ft.app(target=main,assets_dir="assets")