import flet as ft
from FtpClient.ftpclient import *
def main(page: ft.Page):
    # Function to show the files page with the list of files
    def show_files_page(items):
        page.clean()
        page.title = "Files"
        file_list = ft.ListView(width=400, height=300)  # A list view to display files and directories
        for name, item_type in items:
            file_list.controls.append(ft.Text(f"{name} ({item_type})"))  # Create ListTile for each item
        back_button = ft.ElevatedButton("Back", on_click=show_main_page)
        page.add(
            ft.Column(
                [
                    file_list,
                    ft.Row([back_button], alignment=ft.MainAxisAlignment.CENTER),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        page.update()

    # Function to show the main page
    def show_main_page(event=None):
        page.clean()
        page.title = "Flet FTP Client"
        page.add(
            ft.Column(
                [
                    ft.Row([host_input], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([port_input], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([user_input], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([password_input], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([connect_button], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([status_text], alignment=ft.MainAxisAlignment.CENTER),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        page.update()

    # Function to handle FTP connection
    def connect_to_ftp(event):
        try:
            # Retrieve values from input fields
            host = host_input.value.strip()
            port = port_input.value.strip()
            user = user_input.value.strip()
            password = password_input.value.strip()

            # Check if any fields are empty
            if not host or not port or not user or not password:
                status_text.value = "All fields are required."
                status_text.color = "red"
                page.update()
                return

            # Convert port to integer and check if it's valid
            if not port.isdigit() or not (1 <= int(port) <= 65535):
                status_text.value = "Port must be a number between 1 and 65535."
                status_text.color = "red"
                page.update()
                return

            # Attempt to connect
            ftp = connect_to_host(host, user, password, int(port))
            if ftp:
                status_text.value = "Connected"
                status_text.color = "green"
                files = retrieve_files_and_dirs(ftp)  # Retrieve files after successful connection
                print(files)
                show_files_page(files)  # Navigate to the Files page with the list of files
            else:
                status_text.value = "Problem connecting to host"
                status_text.color = "red"

        except Exception as ex:
            status_text.value = f"Error: {ex}"
            status_text.color = "red"
        page.update()

    # Inputs and components for the main page
    host_input = ft.TextField(label="FTP Host", autofocus=True, width=300)
    port_input = ft.TextField(label="Port", value="21", width=300)  # Default FTP port is 21
    user_input = ft.TextField(label="Username", width=300)
    password_input = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)
    connect_button = ft.ElevatedButton("Connect", on_click=connect_to_ftp)
    status_text = ft.Text(value="Not connected", size=16, color="red")

    # Start by showing the main page
    show_main_page()

ft.app(main)