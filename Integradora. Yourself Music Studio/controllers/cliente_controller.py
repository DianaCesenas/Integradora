import flet as ft
from models.cliente_model import ClienteModel
from views.cliente_view import ClienteView

class ClienteController:
    def __init__(self, page, db, contenedor_principal):
        self.page = page
        self.db = db
        self.contenedor = contenedor_principal 
        
        
        self.modelo = ClienteModel(self.db)
        self.vista = ClienteView(page, self) 

    def iniciar_modulo(self):
        """Este método se llama desde el Main para mostrar la pantalla"""
        
        self.contenedor.controls.clear()
        
        
        self.contenedor.controls.append(ft.Column([
        ]))
        
        
        self.vista.inicializar(self.contenedor)
        
        self.contenedor.update()
        
    
        self.cargar_datos()

    #CRUD 

    def cargar_datos(self):
        datos = self.modelo.get_all()
        self.vista.cargar_filas(datos)

    def crear_cliente(self, datos):
        error = self.modelo.validar(*datos)
        if error:
            self.mostrar_alerta_error(error)
            return
        try:
            self.modelo.crear(*datos)
            self._mostrar_mensaje("Cliente creado correctamente", "green")
            self.cargar_datos()
        except Exception as e:
            self.mostrar_alerta_error(f"Error BD: {e}")

    def actualizar_cliente(self, id_cliente, datos):
        error = self.modelo.validar(*datos)
        if error:
            self.mostrar_alerta_error(error)
            return
        try:
            self.modelo.actualizar(id_cliente, *datos)
            self._mostrar_mensaje("Cliente actualizado", "blue")
            self.cargar_datos()
        except Exception as e:
            self.mostrar_alerta_error(f"Error al actualizar: {e}")

    def eliminar_cliente(self, id_cliente):
        try:
            self.modelo.eliminar(id_cliente)
            self._mostrar_mensaje("Cliente eliminado", "orange")
            self.cargar_datos()
        except Exception as e:
            self.mostrar_alerta_error(f"Error al eliminar: {e}")

    

    def buscar_cliente(self, texto):
        if not texto:
            self.cargar_datos()
            return

       
        try:
            datos_filtrados = self.modelo.buscar(texto)
           
            self.vista.cargar_filas(datos_filtrados)
        except Exception as e:
            self.mostrar_alerta_error(f"Error al buscar: {e}")

    

    def mostrar_alerta_error(self, mensaje):
        self.alerta = ft.AlertDialog(
            title=ft.Text("⚠️ Atención"),
            content=ft.Text(mensaje),
            actions=[ft.TextButton("Entendido", on_click=lambda e: self.page.close(self.alerta))]
        )
        self.page.open(self.alerta)

    def _mostrar_mensaje(self, texto, color):
        self.page.snack_bar = ft.SnackBar(ft.Text(texto), bgcolor=color)
        self.page.snack_bar.open = True
        self.page.update()