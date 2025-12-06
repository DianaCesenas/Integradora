import flet as ft
import sys
import os

# Ajuste de path para importar módulos hermanos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importamos el controlador y la VistaBase
from Controlador.controlador_reservas import Controlador_Reservas
from Views.Vistas_Base import VistaBase # Asegúrate de que la ruta sea correcta

class VistaTablaReservas(VistaBase):
    def __init__(self, page: ft.Page):
        # Configuración de colores y variables
        self.PURPLE = "#A11F1F"
        self.ORANGE = "#FF9F43"
        self.BG_COLOR = "#F4F5F9"
        self.page = page
        
        # Obtenemos datos iniciales
        datos = Controlador_Reservas.mostrar()
        self.lista_productos = datos if datos else []

        # Generamos el contenedor con toda la UI
        Tabla = self.mostrar_tabla()

        # Llamamos al constructor de la clase padre (VistaBase)
        # Nota: Ajusté la ruta a "/reservas" para que tenga sentido, pero puedes poner "/inicio" si prefieres.
        super().__init__(page, "/gestion_reservas", "Reservas", 0, Tabla)

    # --- VENTANAS EMERGENTES ---
    def abrir_dialogo_borrar(self, id):
        def confirmar_eliminar(e):
            Controlador_Reservas.desactivar(id)
            self.page.close(self.dialogo)
            self.recargar_tabla()

        self.dialogo = ft.AlertDialog(
            title=ft.Text("Borrar Reserva"),
            content=ft.Text(f"¿Eliminar reservación ID '{id}'?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.page.close(self.dialogo)),
                ft.TextButton("Eliminar", style=ft.ButtonStyle(color="red"), on_click=confirmar_eliminar)
             ],)
        self.page.open(self.dialogo)

    def abrir_dialogo_agregar(self):
        # Aquí iría tu lógica de agregar. Recuerda llamar a self.recargar_tabla() al guardar.
        print("Abrir diálogo agregar")

    def cambiar_ruta(self):
        self.page.go("/reservas")

    def abrir_dialogo_editar(self, idr, ids, f, hi, ht, p, ic):
        self.idr = idr
        #self.edit_ids = ft.TextField(label="ID_salas", value=str(ids))
        self.edit_f = ft.TextField(label="Fecha", value=str(f))
        self.edit_hi = ft.TextField(label="Hora inicio", value=str(hi))
        self.edit_hf = ft.TextField(label="Hora fin", value=str(ht))
        self.edit_np = ft.TextField(label="N° personas", value=str(p))
        #self.edit_idc = ft.TextField(label="ID cliente", value=str(ic))

        def guardar_edicion(e):
            Controlador_Reservas.modificar(
                #self.idr,
                #self.edit_ids.value,
                self.edit_f.value,
                self.edit_hi.value,
                self.edit_hf.value, 
                self.edit_np.value,
                #self.edit_idc.value
            )
            self.page.close(self.dialogo)
            self.recargar_tabla()

        self.dialogo = ft.AlertDialog(
            title=ft.Text("Editar Reserva"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.page.close(self.dialogo)),
                ft.ElevatedButton("Actualizar", on_click=guardar_edicion)
            ],
            content=ft.Container(
                width=600,
                height=400,
                padding=10,
                alignment=ft.alignment.center,
                content=ft.Column(
                    [
                        ft.Row([self.edit_f,self.edit_np]),
                        ft.Row([self.edit_hi, self.edit_hf]),
                    ],
                    height=150, tight=True
                ),
            )
        )
        self.page.open(self.dialogo)

    def mostrar_tabla(self):
        
        # -----------------------------------------------------------
        columnas_config = [
            ("ID",           1,      "c"), 
            ("ID_salas",     2,      "c"), 
            ("Fecha",        3,      "c"), 
            ("H. Inicio",    2,      "c"), 
            ("H. Fin",       2,      "c"), 
            ("Pers.",        1,      "c"), 
            ("ID Cli",       1,      "c"), 
            ("Acciones",     2,      "e"), 
        ]

        titulos = [c[0] for c in columnas_config]
        anchos =  [c[1] for c in columnas_config]
        aligns =  [c[2] for c in columnas_config]

        # -----------------------------------------------------------
        # A. BARRA SUPERIOR
        # -----------------------------------------------------------
        buscador = ft.TextField(
            hint_text="Buscar...", prefix_icon=ft.Icons.SEARCH,
            border_radius=10, bgcolor="white", border_color="transparent",
            expand=True, content_padding=10, text_size=14
        )

        btn_agregar = ft.ElevatedButton(
            text="Agregar Nuevo", icon=ft.Icons.ADD,
            bgcolor="#A11F1F", color="white", height=45,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            on_click=lambda e: self.cambiar_ruta
        )

        contenedor_header = ft.Container(
            content=ft.Row([buscador, btn_agregar], spacing=20),
            padding=20, bgcolor="#F9F9F9"
        )

        
        controles_titulos = []
        for i, titulo in enumerate(titulos):
            if aligns[i] == "c":
                alineacion = ft.alignment.center
                txt_align = ft.TextAlign.CENTER
            elif aligns[i] == "e":
                alineacion = ft.alignment.center_right
                txt_align = ft.TextAlign.RIGHT
            else:
                alineacion = ft.alignment.center_left
                txt_align = ft.TextAlign.LEFT
            
            controles_titulos.append(
                ft.Container(
                    content=ft.Text(titulo, color="#909090", size=12, weight="bold", text_align=txt_align),
                    expand=anchos[i],
                    alignment=alineacion 
                )
            )

        contenedor_titulos = ft.Container(
            content=ft.Row(controls=controles_titulos),
            padding=ft.padding.symmetric(horizontal=20, vertical=15),
            bgcolor="white",
            border=ft.border.only(bottom=ft.border.BorderSide(1, "#E0E0E0"))
        )

        
        filas_visuales = [] 

        for fila in self.lista_productos:
            try:
                id_res = fila[0]
                id_salas = fila[1]
                fecha = fila[2]
                h_i = fila[3]
                h_t = fila[4] 
                personas = fila[5] 
                id_cli = fila[6]
            except IndexError:
                continue

            btn_edit = ft.IconButton(ft.Icons.EDIT, icon_color="#1B1A1A", icon_size=18,
                on_click=lambda e, idr=id_res, ids=id_salas, f=fecha, hi=h_i, ht=h_t, p=personas, ic=id_cli: self.abrir_dialogo_editar(idr,ids,f,hi,ht,p,ic))
            
            btn_del = ft.IconButton(ft.Icons.DELETE, icon_color="#E74C3C", icon_size=18,
                on_click=lambda e, id_b=id_res: self.abrir_dialogo_borrar(id_b))

            celdas_data = [
                str(id_res), str(id_salas), str(fecha), 
                str(h_i), str(h_t), str(personas), str(id_cli)
            ]

            controles_fila = []
            
            for i, texto in enumerate(celdas_data):
                if aligns[i] == "c":
                    alineacion = ft.alignment.center
                elif aligns[i] == "e":
                    alineacion = ft.alignment.center_right
                else:
                    alineacion = ft.alignment.center_left
                
                color_texto = "black" if i == 1 else "#505050"
                weight_texto = "bold" if i == 1 else "normal"

                controles_fila.append(
                    ft.Container(
                        content=ft.Text(texto, color=color_texto, weight=weight_texto, size=13),
                        expand=anchos[i],
                        alignment=alineacion
                    )
                )

            controles_fila.append(
                ft.Container(
                    content=ft.Row([btn_edit, btn_del], spacing=0, alignment=ft.MainAxisAlignment.END), 
                    expand=anchos[7], 
                    alignment=ft.alignment.center_right
                )
            )

            nueva_fila = ft.Container(
                padding=ft.padding.symmetric(horizontal=20, vertical=12),
                content=ft.Column([
                    ft.Row(controles_fila),
                    ft.Divider(height=1, color="#F0F0F0") 
                ], spacing=5)
            )
            filas_visuales.append(nueva_fila)

        
        contenido_scroll = ft.Column(controls=filas_visuales, scroll=ft.ScrollMode.AUTO, expand=True)

        cuerpo_tabla = ft.Container(
            content=ft.Column([contenedor_titulos, contenido_scroll], spacing=0, expand=True),
            bgcolor="white",
            border_radius=15,
            margin=ft.margin.only(left=20, right=20, bottom=20),
            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.05, "black")),
            expand=True
        )

        # Empaquetamos todo en un contenedor principal para devolverlo
        contenedor_principal = ft.Container(
            content=ft.Column([contenedor_header, cuerpo_tabla], spacing=10, expand=True),
            expand=True,
            bgcolor=self.BG_COLOR
        )
        
        return contenedor_principal

    def recargar_tabla(self):
        # 1. Volvemos a pedir los datos
        nuevos_datos = Controlador_Reservas.mostrar()
        self.lista_productos = nuevos_datos if nuevos_datos else []
        
        # 2. Generamos el nuevo contenedor
        nuevo_contenedor = self.mostrar_tabla()
        
        # 3. Actualizamos los controles de la Vista (VistaBase hereda de View)
        # En Flet View, reemplazamos el contenido de 'controls'
        self.controls = [nuevo_contenedor]
        self.update()
        