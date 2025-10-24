import flet as ft

# ---------- PÁGINA DE CONFIGURAÇÕES ----------
def configuracoes_view(page: ft.Page):
    def alternar_tema(e):
        page.theme_mode = (
            ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        )
        aplicar_tema()

    def aplicar_tema():
        if page.theme_mode == ft.ThemeMode.DARK:
            page.bgcolor = ft.Colors.BLUE_GREY_900
            titulo.color = ft.Colors.WHITE
        else:
            page.bgcolor = ft.Colors.BLUE_100
            titulo.color = ft.Colors.BLACK
        page.update()

    def resetar_configuracoes(e):
        switch_notificacoes.value = True
        switch_sons.value = False
        page.open(
            ft.SnackBar(
                content=ft.Text("Configurações restauradas com sucesso!", color="white"),
                bgcolor=ft.Colors.GREEN_600,
                duration=2000
            )
        )
        page.update()

    def abrir_saida(e):
        page.go("/saida")

    card_color = ft.Colors.BLUE_700 if page.theme_mode == ft.ThemeMode.DARK else ft.Colors.BLUE_300

    app_bar = ft.AppBar(
        title=ft.Text("Configurações", size=20, weight="bold", color="white"),
        bgcolor=card_color,
        center_title=True,
    )
    
    titulo = ft.Text("Preferências do App", size=22, weight="bold")

    switch_notificacoes = ft.Switch(
        label="Notificações",
        value=True,
        on_change=lambda e: print(f"Notificações {'ativadas' if e.control.value else 'desativadas'}"),
    )

    switch_sons = ft.Switch(
        label="Sons do aplicativo",
        value=False,
        on_change=lambda e: print(f"Sons {'ativados' if e.control.value else 'desativados'}"),
    )

    btn_resetar = ft.ElevatedButton(
        "Restaurar Padrões",
        icon=ft.Icons.SETTINGS_BACKUP_RESTORE,
        on_click=resetar_configuracoes,
        bgcolor=ft.Colors.RED_600,
        color=ft.Colors.WHITE,
        width=200,
    )

    btn_saida = ft.ElevatedButton(
        "Solicitar Saída do Curso",
        icon=ft.Icons.LOGOUT,
        bgcolor=ft.Colors.BLUE_600,
        color=ft.Colors.WHITE,
        width=250,
        on_click=abrir_saida,
    )

    conteudo = ft.Column(
        [
            titulo,
            ft.Divider(),
            switch_notificacoes,
            switch_sons,
            ft.Divider(),
            btn_resetar,
            btn_saida,
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.View(
        route="/config",
        controls=[
            app_bar,
            ft.Container(
                content=conteudo,
                expand=True,
                alignment=ft.alignment.center,
                padding=20,
            ),
        ],
    )


# ---------- PÁGINA DE SOLICITAÇÃO DE SAÍDA ----------
def saida_view(page: ft.Page):
    def voltar_config(e):
        page.go("/config")

    def confirmar_saida(e):
        etapa1.visible = False
        etapa2.visible = True
        page.update()

    def enviar_saida(e):
        if campo_justificativa.value.strip():
            page.open(
                ft.SnackBar(
                    content=ft.Text("Solicitação enviada com sucesso!", color="white"),
                    bgcolor=ft.Colors.GREEN_600,
                    duration=2000
                )
            )
            campo_justificativa.value = ""
        else:
            page.open(
                ft.SnackBar(
                    content=ft.Text("Por favor, escreva o motivo antes de enviar.", color="white"),
                    bgcolor=ft.Colors.RED_600,
                    duration=2000
                )
            )
        page.update()

    card_color = ft.Colors.BLUE_700 if page.theme_mode == ft.ThemeMode.DARK else ft.Colors.BLUE_300

    app_bar = ft.AppBar(
        title=ft.Text("Solicitação de Saída", size=20, weight="bold", color="white"),
        bgcolor=card_color,
        center_title=True,
        leading=ft.IconButton(
            ft.Icons.ARROW_BACK,
            icon_color="white",
            tooltip="Voltar",
            on_click=voltar_config,
        ),
    )

    # ---------- Etapa 1 ----------
    texto_titulo = ft.Text(
        "Solicitação de Saída do Curso",
        size=22,
        weight="bold",
        text_align=ft.TextAlign.CENTER,
        color=ft.Colors.WHITE
    )

    texto_info = ft.Text(
        "Este processo possui duas etapas: confirmação e justificativa.",
        size=15,
        text_align=ft.TextAlign.CENTER,
        color=ft.Colors.WHITE70,
        width=400
    )

    btn_continuar = ft.ElevatedButton(
        "Continuar",
        icon=ft.Icons.ARROW_FORWARD,
        bgcolor=ft.Colors.BLUE_600,
        color=ft.Colors.WHITE,
        width=200,
        height=50,
        on_click=confirmar_saida
    )

    etapa1 = ft.Column(
        [texto_titulo, ft.Divider(), texto_info, btn_continuar],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        visible=True,
    )

    # ---------- Etapa 2 ----------
    texto_justificativa = ft.Text(
        "Por favor, escreva o motivo da sua saída:",
        size=18,
        weight="bold",
        color=ft.Colors.WHITE
    )

    campo_justificativa = ft.TextField(
        label="Escreva sua saída aqui...",
        multiline=True,
        min_lines=4,
        max_lines=8,
        width=360,
    )

    btn_voltar = ft.ElevatedButton(
        "Voltar",
        icon=ft.Icons.ARROW_BACK,
        bgcolor=ft.Colors.GREY_700,
        color=ft.Colors.WHITE,
        width=160,
        on_click=voltar_config
    )

    btn_enviar = ft.ElevatedButton(
        "Enviar Solicitação",
        icon=ft.Icons.SEND,
        bgcolor=ft.Colors.BLUE_600,
        color=ft.Colors.WHITE,
        width=200,
        on_click=enviar_saida
    )

    etapa2 = ft.Column(
        [
            texto_justificativa,
            campo_justificativa,
            ft.Row([btn_voltar, btn_enviar], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        visible=False,
    )

    return ft.View(
        route="/saida",
        controls=[
            app_bar,
            ft.Container(
                content=ft.Column(
                    [etapa1, etapa2],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True
                ),
                expand=True,
                alignment=ft.alignment.center,
                padding=20,
            ),
        ],
    )


# ---------- APP PRINCIPAL ----------
def main(page: ft.Page):
    # ---------- CONFIGURAÇÕES DE TELA FIXA ----------
    page.window.width = 500
    page.window.height = 800
    page.window.min_width = 500
    page.window.min_height = 800
    page.window.max_width = 500
    page.window.max_height = 800
    page.padding = 0

    page.theme_mode = ft.ThemeMode.DARK

    def mudar_rota(route):
        page.views.clear()
        if page.route == "/saida":
            page.views.append(saida_view(page))
        else:
            page.views.append(configuracoes_view(page))
        page.update()

    page.on_route_change = mudar_rota
    page.go("/config")

ft.app(target=main)
