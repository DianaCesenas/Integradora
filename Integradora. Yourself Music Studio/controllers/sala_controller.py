import flet as ft
# from models.salas_model import SalaModel (Descomentar cuando lo creen)
# from views.salas_view import SalaView (Descomentar cuando lo creen)

class SalaController:
    def __init__(self, page, db, contenedor):
        self.page = page
        self.db = db
        self.contenedor = contenedor
        
        # self.modelo = SalaModel(db)
        # self.vista = SalaView(page, self)
        
        self.inicializar()

    def inicializar(self):
        # ESTO ES TEMPORAL PARA QUE NO DE ERROR
        self.contenedor.controls.clear()
        self.contenedor.controls.append(
            ft.Column([
                ft.Text("Gestión de Salas", size=30),
                ft.Text("Este módulo está en construcción", color="red")
            ], alignment=ft.MainAxisAlignment.CENTER)
        )
        self.contenedor.update()