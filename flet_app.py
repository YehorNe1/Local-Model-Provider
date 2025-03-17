# flet_app.py
import flet as ft
import requests

API_URL = "http://127.0.0.1:8000"

def create_flet_ui(page: ft.Page):
    def generate_code_click(e):
        body = {
            "description": desc_input.value.strip(),
            "language": lang_dropdown_gen.value
        }
        try:
            r = requests.post(f"{API_URL}/generate_code", json=body, timeout=10)
            if r.status_code == 200:
                data = r.json()
                gen_output.value = data.get("code", "")
            else:
                gen_output.value = f"Error {r.status_code}: {r.text}"
        except Exception as ex:
            gen_output.value = f"Exception: {ex}"
        page.update()

    def explain_code_click(e):
        body = {"snippet": explain_input.value}
        try:
            r = requests.post(f"{API_URL}/explain_code", json=body, timeout=10)
            if r.status_code == 200:
                data = r.json()
                explain_output.value = (
                    f"Detected Language: {data.get('language','Unknown')}\n\n"
                    f"Explanation:\n{data.get('explanation','')}"
                )
            else:
                explain_output.value = f"Error {r.status_code}: {r.text}"
        except Exception as ex:
            explain_output.value = f"Exception: {ex}"
        page.update()

    def translate_code_click(e):
        body = {
            "snippet": translate_input.value,
            "target_language": lang_dropdown_trans.value
        }
        try:
            r = requests.post(f"{API_URL}/translate_code", json=body, timeout=10)
            if r.status_code == 200:
                data = r.json()
                translate_output.value = (
                    f"Original language: {data.get('original_language','Unknown')}\n\n"
                    f"Translated code:\n{data.get('translated_code','')}"
                )
            else:
                translate_output.value = f"Error {r.status_code}: {r.text}"
        except Exception as ex:
            translate_output.value = f"Exception: {ex}"
        page.update()

    def prefs_click(e):
        body = {
            "indent_size": int(indent_field.value),
            "naming_convention": naming_field.value
        }
        try:
            r = requests.post(f"{API_URL}/style_preferences", json=body, timeout=10)
            if r.status_code == 200:
                data = r.json()
                prefs_output.value = f"Saved:\n{data.get('current_prefs','')}"
            else:
                prefs_output.value = f"Error {r.status_code}: {r.text}"
        except Exception as ex:
            prefs_output.value = f"Exception: {ex}"
        page.update()

    page.title = "Code Assistant"
    page.scroll = "auto"

    # Generate Code UI
    desc_input = ft.TextField(label="Code description", multiline=True, width=600)
    lang_dropdown_gen = ft.Dropdown(
        label="Output language",
        width=300,
        options=[
            ft.dropdown.Option("Python"),
            ft.dropdown.Option("C#"),
            ft.dropdown.Option("Java"),
            ft.dropdown.Option("JavaScript"),
            ft.dropdown.Option("Go"),
        ],
        value="Python"
    )
    gen_btn = ft.ElevatedButton(text="Generate Code", on_click=generate_code_click)
    gen_output = ft.Text(value="", selectable=True)

    generate_section = ft.Column([
        ft.Text("Generate Code", style="headlineSmall"),
        desc_input,
        lang_dropdown_gen,
        gen_btn,
        gen_output
    ])

    # Explain Code UI
    explain_input = ft.TextField(label="Code to explain", multiline=True, width=600)
    explain_btn = ft.ElevatedButton(text="Explain Code", on_click=explain_code_click)
    explain_output = ft.Text(value="", selectable=True)

    explain_section = ft.Column([
        ft.Text("Explain Code", style="headlineSmall"),
        explain_input,
        explain_btn,
        explain_output
    ])

    # Translate Code UI
    translate_input = ft.TextField(label="Code to translate", multiline=True, width=600)
    lang_dropdown_trans = ft.Dropdown(
        label="Target language",
        width=300,
        options=[
            ft.dropdown.Option("Python"),
            ft.dropdown.Option("C#"),
            ft.dropdown.Option("Java"),
            ft.dropdown.Option("JavaScript"),
            ft.dropdown.Option("Go"),
        ],
        value="Python"
    )
    translate_btn = ft.ElevatedButton(text="Translate Code", on_click=translate_code_click)
    translate_output = ft.Text(value="", selectable=True)

    translate_section = ft.Column([
        ft.Text("Translate Code", style="headlineSmall"),
        translate_input,
        lang_dropdown_trans,
        translate_btn,
        translate_output
    ])

    # Style Preferences UI
    indent_field = ft.TextField(label="Indent size", value="4", width=100)
    naming_field = ft.TextField(label="Naming convention", value="snake_case", width=200)
    prefs_btn = ft.ElevatedButton(text="Save Preferences", on_click=prefs_click)
    prefs_output = ft.Text(value="", selectable=True)

    style_section = ft.Column([
        ft.Text("Style Preferences", style="headlineSmall"),
        ft.Row([indent_field, naming_field, prefs_btn]),
        prefs_output
    ])

    page.add(
        ft.Column([
            generate_section,
            ft.Divider(),
            explain_section,
            ft.Divider(),
            translate_section,
            ft.Divider(),
            style_section
        ], spacing=30)
    )