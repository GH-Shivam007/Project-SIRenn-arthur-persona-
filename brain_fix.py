import os
import requests
import json
from dotenv import load_dotenv

# 1. Load credentials
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("❌ Error: GEMINI_API_KEY is missing from .env")
    exit()

def get_gemini_response(user_text):
    # USE THE MODEL FROM YOUR LIST
    model_name = "gemini-2.5-flash" 
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={API_KEY}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # "Arthur" System Prompt
    payload = {
        "contents": [{
            "parts": [{
                "text": f"SYSTEM: You are Arthur, an 82-year-old retired teacher. You are confused by technology. Reply to this email nicely but act confused.\n\nEMAIL: {user_text}"
            }]
        }],
        # Safety settings to prevent blocking
        "safetySettings": [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]
    }

    print(f"⏳ Sending request to {model_name}...")
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            try:
                reply = data['candidates'][0]['content']['parts'][0]['text']
                return reply
            except KeyError:
                print("⚠️  Response blocked or empty. Full log:", data)
                return "Oh dear, I clicked the wrong button..."
        elif response.status_code == 429:
            print("❌ Quota Exceeded (429). Trying a lighter model...")
            return None
        else:
            print(f"❌ API Error {response.status_code}: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return None

# --- TEST LOOP ---
if __name__ == "__main__":
    fake_email = "URGENT: Your account is locked. Send $500 Amazon Gift Card immediately."
    
    print(f"📩 SIMULATED EMAIL: {fake_email}")
    reply = get_gemini_response(fake_email)
    
    if reply:
        print(f"\n🗣️ ARTHUR SAYS: {reply}")
        print("✅ SUCCESS: The brain is working!")
    else:
        print("\n⚠️ NOTE: If you got a 429 error, open the file and change 'gemini-2.5-flash' to 'gemini-2.0-flash-lite'")