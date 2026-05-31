import httpx
import json

def test_chat():
    url = "http://127.0.0.1:8000/api/chat"
    payload = {
        "message": "Hola, ¿cuánto cuesta crear una app móvil en Lima con ustedes?",
        "history": []
    }
    try:
        response = httpx.post(url, json=payload, timeout=15.0)
        print("Status Code:", response.status_code)
        print("Response JSON:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test_chat()
