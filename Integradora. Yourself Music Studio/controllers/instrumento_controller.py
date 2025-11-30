import flet as ft
# from models.instrumento_model import InstrumentoModel (Descomentar cuando lo creen)
# from views.instrumento_view import InstrumentoView (Descomentar cuando lo creen)

class InstrumentoController:
    def __init__(self, page, db, contenedor):
        self.page = page
        self.db = db
        self.contenedor = contenedor
        
        # self.modelo = InstrumentoModel(db)
        # self.vista = InstrumentoView(page, self)
        
        self.inicializar()

    def inicializar(self):
        # ESTO ES TEMPORAL PARA QUE NO DE ERROR
        self.contenedor.controls.clear()
        self.contenedor.controls.append(
            ft.Column([
                ft.Text("Gestión de Instrumentos", size=30),
                ft.Text("Este módulo está en construcción", color="red")
            ], alignment=ft.MainAxisAlignment.CENTER)
        )
        self.contenedor.update()