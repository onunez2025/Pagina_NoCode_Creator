import httpx
import os
from dotenv import load_dotenv

load_dotenv()

def list_models():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("No API Key found.")
        return
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    try:
        response = httpx.get(url, timeout=15.0)
        print("Status Code:", response.status_code)
        if response.status_code == 200:
            data = response.json()
            print("Available models:")
            for model in data.get('models', []):
                print(f"- {model['name']} (supported methods: {model.get('supportedGenerationMethods', [])})")
        else:
            print("Error:", response.text)
    except Exception as e:
        print("Exception:", e)

if __name__ == "__main__":
    list_models()
