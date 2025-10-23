import flet as ft

avaliacao_enviada = 0

# ---------- Função para criar estrelas ----------
def criar_estrelas(on_change):
    stars = []
    rating = {"nota": 0}

    def on_click_star(e):
        rating["nota"] = e.control.data
        for s in stars:
            s.icon = "star" if s.data <= rating["nota"] else "star_outline"
        on_change(rating["nota"])
        e.page.update()

    for i in range(1, 6):
        star = ft.IconButton(
            icon="star_outline",
            icon_color=ft.Colors.AMBER_400,
            icon_size=50,
            data=i,
            tooltip=f"{i} estrela{'s' if i > 1 else ''}",
            on_click=on_click_star
        )
        stars.append(star)

    return stars, rating


# ---------- Tela de Feedback ----------
def feedback_view(page: ft.Page):
    global avaliacao_enviada

    page.title = "Feedback"
    page.window.width = 500
    page.window.height = 800
    page.window.min_width = 500
    page.window.min_height = 800
    page.window.max_width = 500
    page.window.max_height = 800
    page.padding = 0

    # ---------- Funções de menu ----------
    def clicou_menu(e):
        item = e.control.text.upper()
        if item == "SUPORTE":
            print("Abrir suporte...")
        elif item == "CONFIGURAÇÕES":
            print("Abrir configurações...")
        elif item == "TEMA":
            mudar_tema(None)
        elif item == "SAIR":
            print("Encerrar aplicação...")

    def voltar_home(e):
        page.go("/home")

    # ---------- Funções de avaliação ----------
    def on_rating_change(nota):
        nota_text.value = f"{nota} estrela{'s' if nota > 1 else ''}"
        page.update()

    def enviar_click(e=None):
        global avaliacao_enviada
        if rating["nota"] == 0:
            snack = ft.SnackBar(
                content=ft.Text("⚠️ Selecione uma avaliação!", color="white"),
                bgcolor=ft.Colors.RED_600,
                open=True,
                duration=3000
            )
        else:
            avaliacao_enviada = rating["nota"]
            snack = ft.SnackBar(
                content=ft.Text(
                    f"✅ Avaliação {rating['nota']} estrela{'s' if rating['nota'] > 1 else ''} enviada!",
                    color="white"
                ),
                bgcolor=ft.Colors.GREEN_600,
                open=True,
                duration=3000
            )
            comentario.value = ""
            rating["nota"] = 0
            for s in stars:
                s.icon = "star_outline"
            nota_text.value = ""
        page.snack_bar = snack
        page.snack_bar.open = True
        page.update()

    # ---------- Tema ----------
    def mudar_tema(e=None):
        page.theme_mode = (
            ft.ThemeMode.LIGHT
            if page.theme_mode == ft.ThemeMode.DARK
            else ft.ThemeMode.DARK
        )
        aplicar_tema()

    def aplicar_tema():
        if page.theme_mode == ft.ThemeMode.DARK:
            page.bgcolor = ft.Colors.BLUE_500
            texto_avaliacao.color = ft.Colors.WHITE
            nota_text.color = ft.Colors.AMBER_400
        else:
            page.bgcolor = ft.Colors.BLUE_100
            texto_avaliacao.color = ft.Colors.BLACK
            nota_text.color = ft.Colors.AMBER_800
        page.update()

    # ---------- Elementos ----------
    nota_text = ft.Text("", size=18, weight="bold", color=ft.Colors.AMBER_400)
    texto_avaliacao = ft.Text("Como você avalia nosso App?", size=22, weight="bold")

    stars, rating = criar_estrelas(on_rating_change)

    estrela_row = ft.Row(
        controls=stars,
        alignment=ft.MainAxisAlignment.CENTER
    )

    comentario = ft.TextField(
        label="Conte-nos sua experiência (opcional)",
        multiline=True,
        min_lines=3,
        max_lines=5,
        width=360
    )

    conteudo = ft.Column(
        [
            texto_avaliacao,
            estrela_row,
            nota_text,
            comentario,
            ft.ElevatedButton(
                "Enviar",
                icon="send",
                on_click=enviar_click,
                bgcolor=ft.Colors.BLUE_600,
                color=ft.Colors.WHITE,
                width=180,
                height=50
            ),
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )

    # ---------- Cor do AppBar ----------
    card_color = ft.Colors.BLUE_700 if page.theme_mode == ft.ThemeMode.DARK else ft.Colors.BLUE_300

    # ---------- Retorno da View ----------
    return ft.View(
        route="/feedback",
        controls=[
            ft.AppBar(
                title=ft.Text("Feedback", size=20, weight=ft.FontWeight.BOLD, color="white"),
                bgcolor=card_color,
                center_title=True,
                leading=ft.IconButton(
                    ft.Icons.ARROW_BACK,
                    icon_color="white",
                    tooltip="Voltar",
                    on_click=voltar_home,
                ),
                actions=[
                    ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem(text="TEMA", icon="WB_SUNNY_OUTLINED", on_click=mudar_tema),
                            ft.PopupMenuItem(text="ACESSIBILIDADE", icon="ACCESSIBILITY", on_click=clicou_menu),
                            ft.PopupMenuItem(text="CONFIGURAÇÕES", icon="SETTINGS_OUTLINED", on_click=clicou_menu),
                            ft.PopupMenuItem(text="SUPORTE", icon="HELP_OUTLINE_ROUNDED", on_click=clicou_menu),
                            ft.PopupMenuItem(),
                            ft.PopupMenuItem(text="SAIR", icon="CLOSE_ROUNDED", on_click=clicou_menu),
                        ]
                    ),
                ],
            ),
            ft.Container(
                content=conteudo,
                expand=True,
                alignment=ft.alignment.center,  # centraliza vertical e horizontalmente
                padding=20,
            ),
        ],
    )


# ---------- Função principal ----------
def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.views.append(feedback_view(page))
    page.update()


    return ft.View(
    route="/feedback",
    controls=[       ft.Container(
            content=feedback_view,
            alignment=ft.alignment.center,
            expand=True,
        )],
    vertical_alignment="center",
    horizontal_alignment="center",
        )
