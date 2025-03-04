import flet as ft
#from home import HomePage

class SettingsPage:
    def __init__(self, page: ft.Page, go_back_callback):
        self.page = page
        self.page.title = "Cloudy4Win - Settings"
        self.go_back_callback = go_back_callback

        self.version = ft.Text("Version: 1.0.0", style=ft.TextThemeStyle.BODY_LARGE)
        self.update_btn = ft.ElevatedButton(
            "Check for Updates",
            icon=ft.icons.UPDATE,
            on_click=self.check_for_update
        )
        self.back_btn = ft.TextButton("Back to Home", on_click=self.go_back)

        self.page.add(
            ft.Column([
                ft.Icon(name=ft.icons.SETTINGS, size=36),
                ft.Text("Application Settings", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                ft.Divider(),
                self.version,
                self.update_btn,
                ft.Divider(),
                self.back_btn
            ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER)
        )

    def check_for_update(self, e):
        self.page.launch_url("https://example.com/update-check")

    def go_back(self, e):
        #self.page.clean()
        #HomePage(self.page)
        self.go_back_callback()
