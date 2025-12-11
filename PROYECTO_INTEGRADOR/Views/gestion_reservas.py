import flet as ft 
import sys
import os
# Ajuste de path para imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Controlador.controlador_reservas import Controlador_Reservas
from Views.Vistas_Base import VistaBase 

class VistasReservas(VistaBase):
    def __init__(self, page: ft.Page):
        self.PURPLE = "#A11F1F"
        self.BG_COLOR = "#F4F5F9"
        self.page = page
        self.page.title = "Yourself Music Studio"
        self.page.bgcolor = self.BG_COLOR
        self.page.window_width = 1000
        self.page.window_height = 700
        
        # Estado de la vista
        self.texto_busqueda = "" 
        self.orden_actual = None 
        self.dialogo = None
        
        # Inicializar base
        super().__init__(page, "/gestion_reservas", "Gestion de reservas", 2, None)
        
        # =================================================================
        # 1. COMPONENTES ESTÁTICOS (Se crean UNA sola vez)
        # =================================================================
        
        # --- BUSCADOR ---
        buscador = ft.TextField(
            hint_text="Buscar por nombre de cliente o sala...",
            prefix_icon=ft.Icons.SEARCH,
            bgcolor="white",
            expand=True,
            border_width=0.5,      
            border_color="#2B2B2B",    
            border_radius=10,
            value=self.texto_busqueda,
            color="black", 
            # Usamos lambda para actualizar variable y buscar al mismo tiempo
            on_change=lambda e: self.actualizar_busqueda(e.control.value), 
            on_submit=self.buscar
        )
        
        btn_limpiar = ft.Container(
            content=ft.IconButton(ft.Icons.REFRESH, icon_color="#2B2B2B", tooltip="Recargar", on_click=self.limpiar_busqueda),
            bgcolor="#CBD0D5", border_radius=10, height=45, alignment=ft.alignment.center
        )
        
        # Botón de Ordenar
        self.icono_orden = ft.Icon(ft.Icons.SORT_BY_ALPHA, color="#2B2B2B") # Guardamos referencia para cambiar icono
        
        btn_ordenar = ft.Container(
                content=ft.IconButton(content=self.icono_orden, tooltip="Ordenar", on_click=self.alternar_orden),
                bgcolor="#CBD0D5", border_radius=10, height=45, alignment=ft.alignment.center
        )

        btn_agregar = ft.ElevatedButton(
            text="Agregar Nuevo", icon=ft.Icons.ADD, bgcolor="#CBD0D5", color="#2B2B2B",
            height=45, expand=True, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            on_click=self.cambiar_ruta
        )

        contenedor_header = ft.Container(
            content=ft.Column([
                    ft.Row([buscador,btn_limpiar, btn_ordenar], spacing=10), 
                    ft.Row([btn_agregar], spacing=10)
                ], spacing=10), 
            padding=20, bgcolor="#F9F9F9"
        )

        # --- ENCABEZADOS DE TABLA ---
        titulos = ["Sala", "Fecha", "Nombre del cliente", "Horario", "Personas", "Acciones"]
        anchos = [2, 2, 4, 2, 1, 2] 
        
        fila_encabezados = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text(t, color="#2B2B2B", size=12, weight="bold", text_align="center"), 
                    expand=a, 
                    alignment=ft.alignment.center
                ) for t, a in zip(titulos, anchos)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        contenedor_titulos = ft.Container(
            content=fila_encabezados,
            padding=ft.padding.symmetric(horizontal=10, vertical=15),
            bgcolor="white",
            border=ft.border.only(bottom=ft.border.BorderSide(1, "#E0E0E0"))
        )

        # --- CONTENEDOR DINÁMICO (Aquí irán las filas) ---
        self.contenedor_lista_clientes = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

        marca_agua = ft.Container(
            content=ft.Icon(ft.Icons.MUSIC_NOTE_ROUNDED, size=300, opacity=0.1, color=ft.Colors.BLACK54),
            alignment=ft.alignment.center, expand=True
        )

        contenido_tabla_visible = ft.Column([
            contenedor_titulos,      
            self.contenedor_lista_clientes # Solo esto cambiaremos dinámicamente
        ], spacing=0, expand=True)

        cuerpo_tabla = ft.Container(
            content=ft.Stack([marca_agua, contenido_tabla_visible], expand=True),
            bgcolor="white", border_radius=15, margin=20, expand=True,
            shadow=ft.BoxShadow(blur_radius=10, color="#1A000000")
        )

        # --- ARMADO FINAL (Una sola vez) ---
        self.controls = [
            ft.Column([contenedor_header, cuerpo_tabla], spacing=0, expand=True)
        ]

    def did_mount(self):
        """Se ejecuta cuando la vista ya es visible"""
        self.recargar_tabla()

    # =================================================================
    # 2. LÓGICA DE ACTUALIZACIÓN (Corregida)
    # =================================================================

    def actualizar_busqueda(self, texto):
        self.texto_busqueda = texto.strip()
        self.recargar_tabla()

    def recargar_tabla(self, datos_externos=None):
        """Obtiene datos y llama a mostrar_tabla"""
        if datos_externos is not None:
            datos = datos_externos
        else:
            datos = Controlador_Reservas.mostrar(texto_busqueda=self.texto_busqueda, orden=self.orden_actual)
        
        # Solo llamamos a mostrar_tabla. NO reasignamos self.controls
        self.mostrar_tabla(datos)

    def mostrar_tabla(self, lista_clientes):
        # 1. Limpiamos la lista anterior para no duplicar
        self.contenedor_lista_clientes.controls.clear()

        # 2. Si hay búsqueda pero no resultados
        if not lista_clientes and self.texto_busqueda:
            self.contenedor_lista_clientes.controls.append(
                ft.Container(
                    ft.Text(f"No se encontraron reservaciones para '{self.texto_busqueda}'.", color="grey"), 
                    alignment=ft.alignment.center, padding=20
                )
            )

        # 3. Si hay datos
        elif lista_clientes and len(lista_clientes) > 0:
            for fila in lista_clientes:
                # Ajusta los índices según devuelva tu BD
                id_reservaciones = fila[0]
                sala = fila[1]
                fecha = fila[2]
                Horario = fila[3]
                nombre_cliente = fila[4]
                num_personas = fila[5]

                btn_edit = ft.IconButton(
                    ft.Icons.EDIT, icon_color="#1B1A1A", 
                    on_click=lambda e, idr=id_reservaciones, np=num_personas: self.abrir_dialogo_editar(idr, np)
                )
                
                btn_del = ft.IconButton(
                    ft.Icons.DELETE, icon_color="red", 
                    on_click=lambda e, s=sala, idr=id_reservaciones: self.abrir_dialogo_borrar(s, idr)
                )
                
                nueva_fila = ft.Column([
                    ft.Row([
                        ft.Container(content=ft.Text(str(sala), weight="bold", size=14, text_align="center"), expand=2, alignment=ft.alignment.center),
                        ft.Container(content=ft.Text(str(fecha), size=14, text_align="center"), expand=2, alignment=ft.alignment.center),
                        ft.Container(content=ft.Text(str(nombre_cliente),text_align="center"), expand=4, alignment=ft.alignment.center),
                        ft.Container(content=ft.Text(str(Horario), text_align="center"), expand=2, alignment=ft.alignment.center), 
                        ft.Container(content=ft.Text(str(num_personas), text_align="center"), expand=1, alignment=ft.alignment.center), 
                        
                        # Acciones
                        ft.Container(
                            content=ft.Row([btn_edit, btn_del], spacing=0, alignment=ft.MainAxisAlignment.CENTER), 
                            expand=2,
                            alignment=ft.alignment.center
                        ),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Divider(height=1, color="#F0F0F0") 
                ])
                
                # --- AQUÍ ESTABA EL ERROR: USAR .append() ---
                self.contenedor_lista_clientes.controls.append(nueva_fila) 

        else:
            # Caso tabla vacía sin búsqueda
            nueva_fila = ft.Container(
                content=ft.Text("No hay reservaciones registradas", weight="bold", size=14),
                alignment=ft.alignment.center, padding=20
            )
            self.contenedor_lista_clientes.controls.append(nueva_fila)

        # 4. Actualizamos la vista al final
        self.update()

    # =================================================================
    # 3. MÉTODOS AUXILIARES Y DIÁLOGOS
    # =================================================================

    def alternar_orden(self, e):
        if self.orden_actual is None:
            self.orden_actual = "nombre_asc"
            self.icono_orden.name = ft.Icons.SORT_BY_ALPHA_ROUNDED
        else:
            self.orden_actual = None
            self.icono_orden.name = ft.Icons.SORT_BY_ALPHA
        
        self.icono_orden.update()
        self.recargar_tabla()

    def limpiar_busqueda(self, e):
        self.texto_busqueda = ""
        self.orden_actual = None
        self.recargar_tabla()

    def buscar(self, e):
        self.recargar_tabla()
    
    def cambiar_ruta(self, e):
        self.page.go("/reservas")

    def ejecutar_borrado(self, id):
        Controlador_Reservas.desactivar(id)
        if self.dialogo:
            self.page.close(self.dialogo)
        self.recargar_tabla()
        self.mostrar_confirmacion("Reserva eliminada correctamente")

    def abrir_dialogo_borrar(self, sala, id):
        self.dialogo = ft.AlertDialog(
            title=ft.Text("Borrar Reserva"),
            content=ft.Text(f"¿Eliminar reservación de la sala '{sala}'?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.page.close(self.dialogo)),
                ft.TextButton("Eliminar", style=ft.ButtonStyle(color="red"), on_click=lambda e: self.ejecutar_borrado(id))
                ],
        )
        self.page.open(self.dialogo)

    def abrir_dialogo_editar(self, id, num_personas):
        self.edit_nump = ft.TextField(label="Numero de personas", value=str(num_personas))
        self.dialogo = ft.AlertDialog(
            title=ft.Text("Editar reservacion"),
            content=self.edit_nump,
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.page.close(self.dialogo)),
                ft.ElevatedButton("Actualizar", on_click=lambda e: self.validarcampo(id, self.edit_nump.value))
            ],
        )
        self.page.open(self.dialogo)
    
    def validarcampo(self, id, nump):
        if not nump:
            self.mostrar_alerta("El campo de Personas no puede estar vacío.")
            return
        
        if not nump.isdigit() or int(nump) <= 0:
            self.mostrar_alerta("Ingresa un número válido de personas (mayor a 0).")
            return
        
        if self.dialogo:
            self.page.close(self.dialogo)
        
        num=int(nump)
        resp = Controlador_Reservas.modificar(id, num)
        if resp:
            self.recargar_tabla()
            self.mostrar_confirmacion("Se ha modificado con éxito")

    def mostrar_confirmacion(self, mensaje):
        dialogo = ft.AlertDialog(
            icon=ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, size=50, color="green"),
            title=ft.Text("Aviso"),
            content=ft.Text(mensaje),
            actions=[
                ft.TextButton("Entendido", on_click=lambda e: self.page.close(dialogo))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.open(dialogo)
        
    def mostrar_alerta(self, mensaje):
        dialogo = ft.AlertDialog(
            title=ft.Text("Aviso"),
            content=ft.Text(mensaje),
            actions=[
                ft.TextButton("Entendido", on_click=lambda e: self.page.close(dialogo))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.open(dialogo)