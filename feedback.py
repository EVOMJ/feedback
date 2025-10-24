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

    # Cria um snack_bar inicial vazio
    page.snack_bar = ft.SnackBar(content=ft.Text(""), open=False)

    # ---------- Funções de menu ----------
    def clicou_menu(e):
        item = e.control.text.upper()
        if item == "SUPORTE":
            print("Abrir suporte...")
        elif item == "CONFIGURAÇÕES":
            print("Abrir configurações...")
        elif item == "TEMA":
            mudar_tema(None)
        elif item == "FEEDBACK":
            print("Abrir feedback...")
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
            # ⚠️ Erro: nenhuma avaliação
            page.snack_bar = ft.SnackBar(
                content=ft.Row([
                    ft.Icon(name="error_outline", color="white"),
                    ft.Text("Selecione uma avaliação antes de enviar!", color="white")
                ]),
                bgcolor=ft.Colors.RED_600,
                duration=3000,
                behavior=ft.SnackBarBehavior.FLOATING,
                open=True
            )
        else:
            # ✅ Sucesso
            avaliacao_enviada = rating["nota"]
            page.snack_bar = ft.SnackBar(
                content=ft.Row([
                    ft.Icon(name="check_circle_outline", color="white"),
                    ft.Text("Sua mensagem foi enviada com sucesso!", color="white")
                ]),
                bgcolor=ft.Colors.GREEN_600,
                duration=3000,
                behavior=ft.SnackBarBehavior.FLOATING,
                open=True
            )
            comentario.value = ""
            rating["nota"] = 0
            for s in stars:
                s.icon = "star_outline"
            nota_text.value = ""

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
            texto_avaliacaoo.color = ft.Colors.WHITE70
            nota_text.color = ft.Colors.AMBER_400
        else:
            page.bgcolor = ft.Colors.BLUE_100
            texto_avaliacao.color = ft.Colors.BLACK
            texto_avaliacaoo.color = ft.Colors.BLACK54
            nota_text.color = ft.Colors.AMBER_800
        page.update()

    # ---------- Elementos ----------
    logo = ft.Image(
        src="LOGO.jpg.png",  
        width=210,
        height=180,
        fit=ft.ImageFit.CONTAIN
    )

    texto_avaliacaoo = ft.Text(
        "O feedback do aluno serve para avaliar como foi seu dia em aula, identificar se está tudo bem e receber sugestões que possam contribuir para as atividades em sala. Dessa forma, busca-se promover uma maior aproximação entre aluno e professor, fortalecendo a harmonia no ensino.",
        size=13,
        weight="bold",
        text_align=ft.TextAlign.JUSTIFY,
        opacity=1.,
        width=400,
    )

    texto_avaliacao = ft.Text(
        "Como você avalia o App ",
        size=19,
        weight="bold",
        text_align=ft.TextAlign.CENTER,
    )

    nota_text = ft.Text(
        "",
        size=14,
        weight="bold",
        color=ft.Colors.AMBER_400,
        opacity=0.20,
    )

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
            logo,  # <-- Logo adicionada no topo
            texto_avaliacaoo,
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
                            ft.PopupMenuItem(text="FEEDBACK", icon="FEEDBACK", on_click=clicou_menu),
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
                alignment=ft.alignment.center,
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
