# tools.py
import requests

def detect_code_language(code: str) -> str:
    
    url = "http://ai.easv.dk:8989/tools/langrecog"
    one_line = code.replace("\n", " ").replace("\r", " ")
    payload = {
        "codesnippet": one_line,
        "language": ""
    }
    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data.get("language", "Unknown")
    except Exception as e:
        print("Language detection error:", e)
        return "Unknown"

def refactor_code(code: str, style: dict) -> str:
    
    indent = style.get("indent_size", 4)
    naming = style.get("naming_convention", "snake_case")
    return f"// [Refactor] indent={indent}, naming={naming}\n{code}"
