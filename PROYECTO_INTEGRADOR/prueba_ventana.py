import flet as ft
import time

def main(page: ft.Page):
    # Imprimimos la versión para confirmar que el upgrade funcionó
    print(f"Versión de Flet detectada: {ft.version}")

    page.bgcolor = ft.Colors.BLUE
    
    # Intento 1: Maximizar directo
    page.window_maximized = True
    page.update()

    page.add(ft.Text("¿Estoy maximizada?", size=50, color="white"))

    # Intento 2: Forzar después de 1 segundo
    time.sleep(1)
    page.window_maximized = True
    page.update()

if __name__ == "__main__":
    # Importante: Cambiamos el puerto/nombre para engañar a la caché
    ft.app(target=main)