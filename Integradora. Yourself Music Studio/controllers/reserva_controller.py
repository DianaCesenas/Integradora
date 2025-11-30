import flet as ft
# from models.reserva_model import ReservaModel (Descomentar cuando lo creen)
# from views.reserva_view import ReservaView (Descomentar cuando lo creen)

class ReservasController:
    def __init__(self, page, db, contenedor):
        self.page = page
        self.db = db
        self.contenedor = contenedor
        
        # self.modelo = ReservaModel(db)
        # self.vista = ReservaView(page, self)
        
        self.inicializar()

    def inicializar(self):
        # ESTO ES TEMPORAL PARA QUE NO DE ERROR
        self.contenedor.controls.clear()
        self.contenedor.controls.append(
            ft.Column([
                ft.Text("Gestión de RESERVAS", size=30),
                ft.Text("Este módulo está en construcción", color="red")
            ], alignment=ft.MainAxisAlignment.CENTER)
        )
        self.contenedor.update()