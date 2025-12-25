import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("❌ Error: GEMINI_API_KEY is missing.")
    exit()

def list_available_models():
    # We ask the API for the list of ALL models
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print("\n✅ CONNECTED! Here are the models you can use:\n")
            
            # Filter only for models that generate text
            valid_models = []
            for model in data.get('models', []):
                if "generateContent" in model['supportedGenerationMethods']:
                    name = model['name'].replace("models/", "")
                    print(f"👉 {name}")
                    valid_models.append(name)
            
            print("\n------------------------------------------------")
            print(f"RECOMMENDATION: Change your code to use '{valid_models[0]}'")
            print("------------------------------------------------\n")
        else:
            print(f"❌ Error listing models: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    list_available_models()