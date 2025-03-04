import flet as ft
from r2 import R2Manager

class MediaPreview:
    def __init__(self, page: ft.Page, filename: str, go_back_callback, file_details):
        self.page = page
        self.page.title = f"Preview - {filename}"
        self.go_back_callback = go_back_callback
        self.r2 = R2Manager()
        self.filename = filename
        self.file_details = file_details

        # Get presigned URL and open in browser
        presigned_url = self.r2.get_presigned_url(filename)
        if presigned_url:
            self.page.launch_url(presigned_url)
            self.page.snack_bar = ft.SnackBar(
                ft.Text(f"Opening {filename} in browser"),
                open=True
            )
        else:
            self.page.snack_bar = ft.SnackBar(
                ft.Text("Failed to generate preview URL", color=ft.colors.RED_ACCENT_700),
                open=True
            )
        
        # Go back to home page
        self.go_back_callback()

    def go_back(self, e):
        self.go_back_callback()
