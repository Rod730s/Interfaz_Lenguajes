import flet as ft

def main(page: ft.Page):

    page.title = "Evaluador de Expresiones"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.padding = 30

    archivo_excel = None
    resultados_container = ft.Column(
        spacing=5,
        horizontal_alignment="center"
    )

    def seleccionar_archivo(e):
        file_picker.pick_files(allow_multiple=False)

    def archivo_seleccionado(e):
        nonlocal archivo_excel
        if file_picker.result.files:
            archivo_excel = file_picker.result.files[0].path
            page.snack_bar = ft.SnackBar(ft.Text("Archivo seleccionado"))
            page.snack_bar.open = True
            page.update()

    def evaluar_expresiones(e):
        if archivo_excel is None:
            page.snack_bar = ft.SnackBar(ft.Text("Primero selecciona un archivo"))
            page.snack_bar.open = True
            page.update()
            return

        # Datos de prueba
        resultados = [
            ("5 + 3 * 2", 11),
            ("10 + sqrt(9)", 13)
        ]

        resultados_container.controls.clear()

        for expr, valor in resultados:
            resultados_container.controls.append(
                ft.Text(f"{expr} → {valor}", size=18)
            )

        page.update()

    file_picker = ft.FilePicker(on_result=archivo_seleccionado)
    page.overlay.append(file_picker)

    boton_verde = ft.ElevatedButton(
        text="   Seleccionar archivo",
        color="white",
        bgcolor="#2ECC71",  # Verde más bonito
        icon=ft.Icons.FILE_UPLOAD,
        on_click=seleccionar_archivo,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            padding=15
        )
    )
    
    boton_azul = ft.ElevatedButton(
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

    # -------- CARD --------
    card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.CALCULATE, size=60, color="#2c3e50"),
                    ft.Text("Evaluador de expresiones", size=30, weight="bold"),
                    boton_verde,
                    boton_azul,
                    ft.Divider(),
                    resultados_container
                ],
                horizontal_alignment="center",
                spacing=20
            ),
            padding=30,
            width=450,
            height=400
        )
    )

    page.add(
    ft.Stack(
        [
            # Fondo
            ft.Container(
                expand=True,
                bgcolor="#D9ECFF"
            ),

            # Card centrada
            ft.Container(
                content=ft.Column(
                    [card],
                    alignment="center",
                    horizontal_alignment="center"
                ),
                alignment=ft.alignment.center,
                expand=True
            ),

            # Snoopy recargado del lado derecho del card
            ft.Container(
                ft.Image(
                    src="assets/snoopy.png",
                    width=200,     # ajusta tamaño
                ),
                right=260,    # 🔥 controla qué tan pegado al card
                top=225      # 🔥 controla altura exactamente
            )
        ],
        expand=True
    )
)








...
ft.app(target=main, assets_dir="assets")

