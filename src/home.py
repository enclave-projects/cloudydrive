import flet as ft
from settings import SettingsPage
from r2 import R2Manager
import pyperclip
import os
import time
import threading

class HomePage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Cloudy4Win - Dashboard"
        self.r2 = R2Manager()
        self.selected_files = []  # For bulk actions
        self.file_details = {}

        self.page.appbar = ft.AppBar(
            title=ft.Text("My Cloud Storage"),
            actions=[
                ft.IconButton(ft.icons.SETTINGS, on_click=self.open_settings)
            ]
        )

        # File list display
        self.file_list = ft.ListView(expand=True, on_scroll_interval=0.1)
        self.refresh_file_list()
        self.upload_progress = ft.ProgressBar(width=400, visible=False, expand=False)
        self.upload_progress_value = ft.Text(value="Uploading... ", size=12, visible=False)

        # Upload controls
        self.upload_button = ft.ElevatedButton(
            "Upload File",
            icon=ft.icons.UPLOAD_FILE,
            on_click=self.pick_files
        )
        self.file_picker = ft.FilePicker(on_result=self.on_file_picked)
        self.page.overlay.append(self.file_picker)

        #bulk action
        self.bulk_delete_button = ft.ElevatedButton("Delete Selected", icon=ft.icons.DELETE, on_click=self.bulk_delete, visible=False)
        self.bulk_download_button = ft.ElevatedButton("Download Selected", icon=ft.icons.DOWNLOAD, on_click=self.bulk_download, visible=False)
        self.bulk_row = ft.Row(controls=[self.bulk_delete_button, self.bulk_download_button], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER, visible=False)

        # sorting control
        self.sort_dropdown = ft.Dropdown(
            label="Sort By",
            options=[
                ft.dropdown.Option("Name"),
                ft.dropdown.Option("Size"),
                ft.dropdown.Option("Date"),
            ],
            value="Name",
            on_change=self.sort_files,
            width=150
        )

        # filtering control
        self.filter_textfield = ft.TextField(
            label="Search File",
            hint_text="Enter filename",
            on_change=self.filter_files,
            width=250
        )

        self.page.add(
            ft.Column([
                ft.Row([
                    self.sort_dropdown,
                    self.filter_textfield
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                self.bulk_row,
                ft.Row([self.upload_button], alignment=ft.MainAxisAlignment.END),
                self.upload_progress_value,
                self.upload_progress,
                ft.Divider(),
                ft.Text("Your Files", style=ft.TextThemeStyle.HEADLINE_SMALL),
                self.file_list
            ], spacing=20, expand=True)
        )
        self.page.on_drop = self.on_drop

    def pick_files(self, e):
        self.file_picker.pick_files(allow_multiple=True)

    def on_file_picked(self, e: ft.FilePickerResultEvent):
        if e.files is not None and len(e.files) > 0:
            files = e.files
            for file in files:
                self.upload_file(file.name, file.path)

    def upload_file(self, filename, filepath):
        # Show progress bar and text
        self.upload_progress.visible = True
        self.upload_progress_value.visible = True
        self.page.update()
        
        def upload_thread(filename, filepath):
            try:
                file_size = os.path.getsize(filepath)
                
                # Simulate progress (replace with actual progress from R2)
                for i in range(0, 101, 10):  # Simulate 10 steps of progress
                    time.sleep(0.2)  # Simulate some work
                    self.upload_progress.value = i / 100.0
                    self.upload_progress_value.value = f"Uploading... {i}%"
                    self.page.update()

                # Upload to R2
                self.r2.upload_file(filename, filepath)

                self.page.snack_bar = ft.SnackBar(
                    ft.Text(f"Uploaded {filename} to R2"),
                    open=True
                )
                self.page.update()

            except Exception as e:
                print(f"Error uploading file: {e}")

            finally:
                # Hide progress bar and text
                self.upload_progress.value = 0
                self.upload_progress.visible = False
                self.upload_progress_value.visible = False
                self.page.update()
                # Update the list view
                self.add_file_to_list(filename)
                self.refresh_file_list()
                self.page.update()

        # Create and start the upload thread
        thread = threading.Thread(target=upload_thread, args=(filename, filepath))
        thread.daemon = True
        thread.start()

    def refresh_file_list(self):
        self.file_list.controls.clear()
        files = self.r2.list_files()
        for file in files:
            self.add_file_to_list(file)
        self.page.update()

    def add_file_to_list(self, filename):
        file_size, file_type = self.r2.get_file_details(filename)
        self.file_details[filename] = {"size": file_size, "type": file_type}
        
        # Replace ListTile with a custom Row layout for better visibility
        new_file = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.icons.INSERT_DRIVE_FILE, color=ft.colors.BLUE),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    filename,
                                    size=18,
                                    color=ft.colors.WHITE,
                                    weight=ft.FontWeight.W_500,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                ),
                                ft.Text(
                                    f"{file_type}, {file_size}",
                                    size=14,
                                    color=ft.colors.WHITE70,
                                    italic=True,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                ),
                            ],
                            spacing=5,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        expand=True,
                        padding=ft.padding.only(left=15),
                    ),
                    ft.Row(
                        [
                            ft.Checkbox(
                                value=False,
                                on_change=lambda e, file=filename: self.on_file_checked(e, file),
                            ),
                            ft.PopupMenuButton(
                                items=[
                                    ft.PopupMenuItem(
                                        icon=ft.icons.DELETE,
                                        text="Delete",
                                        on_click=lambda e, file=filename: self.delete_file(file),
                                    ),
                                    ft.PopupMenuItem(
                                        icon=ft.icons.EDIT,
                                        text="Rename",
                                        on_click=lambda e, file=filename: self.rename_file_dialog(file),
                                    ),
                                    ft.PopupMenuItem(
                                        icon=ft.icons.SHARE,
                                        text="Share",
                                        on_click=lambda e, file=filename: self.share_file(file),
                                    ),
                                    ft.PopupMenuItem(
                                        icon=ft.icons.DOWNLOAD,
                                        text="Download",
                                        on_click=lambda e, file=filename: self.download_file(file),
                                    ),
                                    ft.PopupMenuItem(
                                        icon=ft.icons.PREVIEW,
                                        text="Preview",
                                        on_click=lambda e, file=filename: self.preview_file(file),
                                    ),
                                ]
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=10,
            padding=ft.padding.all(10),
            margin=ft.margin.only(bottom=5),
            width=800,
            ink=True,  # Add ripple effect on click
            bgcolor=ft.colors.SURFACE_VARIANT,
        )
        self.file_list.controls.append(new_file)

    def copy_url_to_clipboard(self, url):
        if url:
            pyperclip.copy(url)
            print(f"Copied URL to clipboard: {url}")
        else:
            print("Failed to generate or copy URL.")

    def share_file(self, filename):
        presigned_url = self.r2.get_presigned_url(filename)
        if presigned_url:
            self.copy_url_to_clipboard(presigned_url)
        else:
            print("Failed to generate presigned url.")

    def delete_file(self, filename):
        self.r2.delete_file(filename)
        self.refresh_file_list()
        self.page.update()

    def download_file(self, filename):
        presigned_url = self.r2.get_presigned_url(filename)
        if presigned_url:
            self.page.launch_url(presigned_url)
            self.page.snack_bar = ft.SnackBar(
                ft.Text(f"Downloading {filename}"),
                open=True
            )
            self.page.update()
        else:
            print(f"Failed to download the {filename}")
    
    def bulk_download(self, e):
        if not self.selected_files:
            print("No files selected for download.")
            return

        for filename in self.selected_files:
            self.download_file(filename)

    def preview_file(self, filename):
        from preview import MediaPreview
        MediaPreview(self.page, filename, self.go_back_to_home, self.file_details.get(filename))

    def open_settings(self, e):
        self.page.clean()
        SettingsPage(self.page, self.go_back_to_home)

    def go_back_to_home(self):
        self.page.clean()
        HomePage(self.page)
    
    def rename_file_dialog(self, filename):
        rename_dialog = ft.AlertDialog(
            title=ft.Text(f"Rename '{filename}'"),
            content=ft.TextField(label="New name", value=filename),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: self.close_rename_dialog(rename_dialog)),
                ft.TextButton("Rename", on_click=lambda e: self.rename_file(filename, rename_dialog))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = rename_dialog
        rename_dialog.open = True
        self.page.update()

    def close_rename_dialog(self, dialog):
        dialog.open = False
        self.page.update()

    def rename_file(self, old_filename, dialog):
        new_filename = dialog.content.value
        self.r2.rename_file(old_filename, new_filename)
        self.close_rename_dialog(dialog)
        self.refresh_file_list()
        self.page.update()
    
    def on_file_checked(self, e, filename):
        """Handles the checkbox change event for selecting files."""
        if e.control.value:
            self.selected_files.append(filename)
        else:
            self.selected_files.remove(filename)
        
        if self.selected_files:
            self.bulk_row.visible = True
            self.bulk_delete_button.visible = True
            self.bulk_download_button.visible = True
        else:
            self.bulk_row.visible = False
            self.bulk_delete_button.visible = False
            self.bulk_download_button.visible = False
        self.page.update()

    def bulk_delete(self, e):
        """Deletes all selected files."""
        for filename in self.selected_files:
            self.delete_file(filename)
        self.selected_files.clear()
        self.bulk_row.visible = False
        self.bulk_delete_button.visible = False
        self.bulk_download_button.visible = False
        self.page.update()
    
    def sort_files(self, e):
        sort_by = self.sort_dropdown.value
        self.file_list.controls.sort(key=lambda item: self.get_sort_key(item, sort_by))
        self.file_list.update()

    def get_sort_key(self, item, sort_by):
        if sort_by == "Name":
            return item.title.value.lower()
        elif sort_by == "Size":
            filename = item.title.value
            return self.file_details.get(filename, {}).get("size", 0)
        elif sort_by == "Date":
            # add date to the file_details
            return item.subtitle.value

    def filter_files(self, e):
        filter_text = self.filter_textfield.value.lower()
        self.file_list.controls = [
            item
            for item in self.file_list.controls
            if filter_text in item.title.value.lower()
        ]
        self.file_list.update()
        
    def on_drop(self, e):
        for file in e.files:
            self.upload_file(file.name, file.path)
        self.page.update()
