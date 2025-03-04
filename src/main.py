import flet as ft
from home import HomePage

class PinVerificationPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Cloudy4Win - Pin Verification"

        self.pin_input = ft.TextField(
            label="Enter 6-digit Pin",
            password=True,
            keyboard_type=ft.KeyboardType.NUMBER,
            width=200,
            max_length=6,
            text_align=ft.TextAlign.CENTER,
            can_reveal_password=True,
            on_change=self.check_pin_length
        )
        
        self.verify_button = ft.ElevatedButton(
            "Verify",
            on_click=self.verify_pin,
            disabled=True
        )
        self.error_text = ft.Text("", color=ft.colors.RED_ACCENT_700)
        
        self.page.add(
            ft.Column([
                ft.Icon(name=ft.icons.LOCK, size=48),
                ft.Text("Pin Verification", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                self.pin_input,
                self.error_text,
                self.verify_button
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER, spacing=20)
        )

    def check_pin_length(self, e):
        if len(self.pin_input.value) == 6:
            self.verify_button.disabled = False
        else:
            self.verify_button.disabled = True
        self.page.update()
    
    def verify_pin(self, e):
        if self.pin_input.value == "202526":
            self.page.clean()
            HomePage(self.page)
        else:
            self.error_text.value = "Incorrect PIN!"
            self.page.update()

def main(page: ft.Page):
    page.window_width = 400
    page.window_height = 500
    PinVerificationPage(page)

if __name__ == "__main__":
    ft.app(target=main)
