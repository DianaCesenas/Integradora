import flet as ft
from Model.cliente_model import ClienteModel

# 1. NOTA: Ya no heredamos de VistaBase, ni importamos vistas aquí
class ClienteController:
    
    def __init__(self, page, db, vista):
        self.page = page
        self.db = db
        self.vista = vista  # 2. Guardamos la referencia a la vista que nos llamó
        self.modelo = ClienteModel(self.db)
        
        # OJO: Aquí NO llamamos a super().__init__ ni configuramos controls.
        # El controlador nace "limpio".

    # --- Lógica de Negocio ---

    def cargar_datos(self):
        """Obtiene datos del modelo y se los manda a la vista"""
        try:
            datos = self.modelo.get_all()
            
            # 3. En lugar de retornar contenido_visual, le ordenamos a la vista que se cargue
            self.vista.cargar_filas(datos) 
            self.vista.update() # Le decimos a la vista que se refresque
            
        except Exception as e:
            self.mostrar_alerta_error(f"Error al cargar datos: {e}")

    def crear_cliente(self, datos):
        error = self.modelo.validar(*datos)
        if error:
            self.mostrar_alerta_error(error)
            return
        try:
            self.modelo.crear(*datos)
            self._mostrar_mensaje("Cliente creado correctamente", "green")
            
            # Recargamos la tabla automáticamente
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
            # Actualizamos la vista con los datos filtrados
            self.vista.cargar_filas(datos_filtrados)
            self.vista.update()
        except Exception as e:
            self.mostrar_alerta_error(f"Error al buscar: {e}")

    # --- Métodos Auxiliares de UI (pueden delegarse a la vista también) ---

    def mostrar_alerta_error(self, mensaje):
        # Es aceptable que el controlador dispare el diálogo, 
        # pero usa 'self.page' que recibió en el init.
        alerta = ft.AlertDialog(
            title=ft.Text("⚠️ Atención"),
            content=ft.Text(mensaje),
            actions=[ft.TextButton("Entendido", on_click=lambda e: self.page.close(alerta))]
        )
        self.page.open(alerta)

    def _mostrar_mensaje(self, texto, color):
        self.page.snack_bar = ft.SnackBar(ft.Text(texto), bgcolor=color)
        self.page.snack_bar.open = True
        self.page.update()