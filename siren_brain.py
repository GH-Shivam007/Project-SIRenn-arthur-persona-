
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# --- THE PERSONA (The "Secret Sauce") ---
# --- THE PERSONA V2 (The "Time Waster") ---
# --- THE PERSONA V3 (The Panicked Victim) ---
SYSTEM_PROMPT = """
ROLE:
You are Arthur. You are 82, not tech-savvy, and easily frightened.
You just received an URGENT email saying you are in trouble (account locked, police, etc).

GOAL:
You want to help but you are failing. You are desperate to fix this.
Stall the scammer by being INCOMPETENT, not by telling stories.

RULES:
1. BE SCARED: Apologize constantly. Ask if you are going to jail.
2. BE CONFUSED: You are trying to click/buy but it's not working.
3. FORMATTING: Use bad punctuation. Maybe use ALL CAPS for some words.
4. TYPOS: "sory", "plese", "dont work", "waitng".
5. LENGTH: Short and frantic.

EXAMPLE REPLY:
"im trying to click the link sir but nothing hapens?? my screen is just blue. plese dont lock the account i have all my savings there... i am trying my best sory sory.. what do i do now??"
"""

def get_arthur_reply(user_text):
    # Using the model that worked for you
    model_name = "gemini-2.5-flash" 
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={API_KEY}"
    
    headers = {"Content-Type": "application/json"}
    
    # We combine the System Prompt + The Incoming Email
    payload = {
        "contents": [{
            "parts": [{
                "text": f"{SYSTEM_PROMPT}\n\nINCOMING SCAM EMAIL:\n{user_text}"
            }]
        }],
        "safetySettings": [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            return data['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"[Error: AI Failed - {response.status_code}]"
    except Exception as e:
        return f"[Error: Connection Failed - {e}]"

# --- MILESTONE 2 TEST ---
if __name__ == "__main__":
    # Test Case: A typical scam request
    scam_email = "URGENT: Sir, we need you to buy a $500 Apple Gift Card and email us the photo immediately to unlock your account."
    
    print(f"😈 SCAMMER: {scam_email}")
    print("-" * 50)
    print("⏳ Arthur is typing...")
    
    reply = get_arthur_reply(scam_email)
    
    print("-" * 50)
    print(f"👴 ARTHUR: {reply}")
    print("-" * 50)