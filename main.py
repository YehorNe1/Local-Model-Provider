# main.py
import threading
import uvicorn
import flet as ft

from api_app import app
from flet_app import create_flet_ui

def start_api():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

def main_flet(page: ft.Page):
    page.title = "Code Assistant"
    create_flet_ui(page)

if __name__ == "__main__":
    # Start FastAPI in background
    server_thread = threading.Thread(target=start_api, daemon=True)
    server_thread.start()

    # Launch Flet UI
    ft.app(target=main_flet)