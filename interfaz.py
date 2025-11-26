import flet as ft
import os
import subprocess

def main(page: ft.Page):
    # -------------------- Configuración de la ventana --------------------
    page.title = "Proyecto final"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.padding = 30

    archivo_excel = None  # Guardará la ruta del archivo seleccionado

    # -------------------- Loader de evaluación --------------------
    cargando = ft.ProgressRing(visible=False)

    # -------------------- Contenedor donde se mostrarán los resultados --------------------
    resultados_container = ft.Column(
        spacing=5,
        horizontal_alignment="center"
    )

    resultados_box = ft.Container(
        content=resultados_container,
        padding=10,
        bgcolor="#F4F6F7",
        border_radius=10,
        width=350
    )

    # -------------------- Mensajes de error o información --------------------
    mensaje = ft.Text("", size=16, color="red")
    archivo = ft.Text("", size=16, color="#2c3e50", weight="bold")

    # -------------------- Función para abrir archivo en el sistema --------------------
    def abrir_archivo(e):
        if archivo_excel and os.path.exists(archivo_excel):
            try:
                if os.name == "nt":
                    os.startfile(archivo_excel)
                else:
                    subprocess.Popen(["open", archivo_excel])
            except Exception:
                mensaje.color = "red"
                mensaje.value = "⚠ No se pudo abrir el archivo"
                page.update()

    # -------------------- Función para limpiar archivo seleccionado --------------------
    def limpiar_archivo(e):
        nonlocal archivo_excel
        archivo_excel = None
        archivo.value = ""
        mensaje.value = ""
        boton_eliminar_archivo.visible = False
        page.update()

    boton_eliminar_archivo = ft.IconButton(
        icon=ft.Icons.CLOSE,
        icon_color="gray",
        tooltip="Eliminar archivo",
        visible=False,
        on_click=limpiar_archivo
    )

    click_archivo = ft.Row(
        [
            ft.Container(
                content=archivo,
                on_click=abrir_archivo,
                padding=5,
                ink=True,
                tooltip="Abrir archivo"
            ),
            boton_eliminar_archivo
        ],
        alignment="center",
    )

    # -------------------- File Picker para seleccionar Excel --------------------
    def seleccionar_archivo(e):
        file_picker.pick_files(allow_multiple=False)

    def archivo_seleccionado(e):
        nonlocal archivo_excel
        mensaje.value = ""
        page.update()

        if file_picker.result.files:
            file = file_picker.result.files[0]
            nombre = file.name.lower()

            if not (nombre.endswith(".xlsx") or nombre.endswith(".xls")):
                mensaje.color = "red"
                mensaje.value = "❌ No es un archivo tipo Excel"
                archivo_excel = None
                archivo.value = ""
                boton_eliminar_archivo.visible = False
                page.update()
                return

            archivo_excel = file.path
            archivo.value = f"📄 {file.name}"
            archivo.color = "#2980B9"
            boton_eliminar_archivo.visible = True
            page.update()

    file_picker = ft.FilePicker(on_result=archivo_seleccionado)
    page.overlay.append(file_picker)

    # -------------------- Función para evaluar las expresiones --------------------
    def evaluar_expresiones(e):
        if archivo_excel is None:
            mensaje.color = "red"
            mensaje.value = "❌ Primero selecciona un archivo Excel válido"
            resultados_container.controls.clear()
            page.update()
            return

        cargando.visible = True
        page.update()

        # ---------- AQUÍ CONECTARÁS LA PARTE DEL TOKENIZADOR / PARSER ----------
        # Ejemplo:
        # expresiones = leer_excel(archivo_excel)  # Función que lee la columna A
        # resultados = [(expr, evaluar(expr)) for expr in expresiones]
        # Por ahora usamos resultados estáticos para probar la interfaz
        resultados = [
            ("5 + 3 * 2", 11),
            ("10 + sqrt(9)", 13)
        ]

        mensaje.color = "black"
        mensaje.value = "Resultados:"

        resultados_container.controls.clear()
        for expr, valor in resultados:
            resultados_container.controls.append(
                ft.Text(f"{expr} → {valor}", size=18)
            )

        cargando.visible = False
        page.update()

    # -------------------- Botones principales --------------------
    boton_subir_archivo = ft.ElevatedButton(
        text="   Seleccionar archivo",
        color="white",
        bgcolor="#2ECC71",
        icon=ft.Icons.FILE_UPLOAD,
        on_click=seleccionar_archivo,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            padding=15
        )
    )
    
    boton_evaluar_archivo = ft.ElevatedButton(
        text="Evaluar",
        icon=ft.Icons.PLAY_ARROW,
        bgcolor="#3498DB",
        color="white",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            padding=15
        ),
        on_click=evaluar_expresiones
    )

    # -------------------- Tarjeta principal de la UI --------------------
    card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.CALCULATE, size=60, color="#2c3e50"),
                    ft.Text("SheetSolver", size=34, weight=ft.FontWeight.BOLD, color="#2c3e50"),
                    boton_subir_archivo,
                    boton_evaluar_archivo,
                    click_archivo,
                    mensaje,
                    cargando,
                    ft.Divider(),
                    resultados_box
                ],
                horizontal_alignment="center",
                spacing=20
            ),
            padding=30,
            width=450,
            border_radius=20
        )
    )

    # -------------------- Imagen decorativa --------------------
    snoopy = ft.Container(
        ft.Image(src="assets/snoopy.png", width=200),
        right=260,
        top=225
    )

    # -------------------- Añadir todos los elementos a la página --------------------
    # Esto incluye: fondo, tarjeta principal y la imagen decorativa
    page.add(
        ft.Stack(
            [
                ft.Container(expand=True, bgcolor="#D9ECFF"),  # Fondo
                ft.Container(
                    content=ft.Column(
                        [card],
                        alignment="center",
                        horizontal_alignment="center"
                    ),
                    alignment=ft.alignment.center,
                    expand=True
                ),
                snoopy  # Imagen decorativa superpuesta
            ],
            expand=True
        )
    )

# -------------------- Ejecutar la app --------------------
ft.app(target=main, assets_dir="assets")
