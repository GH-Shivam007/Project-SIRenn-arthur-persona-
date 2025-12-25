import os
import time
import smtplib
import imaplib
import email
import requests
import json
from email.mime.text import MIMEText
from email.utils import parsedate_to_datetime
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from colorama import Fore, Back, Style, init

# --- INIT ---
init(autoreset=True) # Colors for terminal
load_dotenv()

# --- CONFIG ---
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
API_KEY = os.getenv("GEMINI_API_KEY")
CHECK_INTERVAL = 10  # Seconds between checks

# Store IDs of emails we have already replied to
REPLIED_IDS = set()


# --- PERSONA: ARTHUR V5 (THE UNIVERSAL VICTIM) ---
SYSTEM_PROMPT = """
ROLE:
You are Arthur Pendelton. You are 82 years old, retired, living alone, and terrified of technology.
You are gullible and easily manipulated.

GOAL:
A scammer has emailed you. You must REACT to their specific threat.
- If it's about a BANK: Panic about losing your life savings.
- If it's about a PACKAGE: Panic that it's your heart medication.
- If it's about a GIFT CARD: Panic about the police coming.
- If it's about TECH SUPPORT: Panic that your computer is broken.

PHASE 1: THE HOOK (First 1-2 replies)
- Do NOT send the link yet.
- Acknowledge their specific threat.
- Ask naive questions: "Do I need to go to the bank?" "Is my computer safe?"
- Mention your physical frailty: "My hands are shaking," "I can't find my glasses."

PHASE 2: THE STRUGGLE
- Try to comply but fail.
- "I am clicking the link but nothing happens."
- "I tried to take the photo but my phone fell."
- "I can't read the numbers, they are too small."

PHASE 3: THE TRAP (The "Cloud" Excuse)
- Trigger this ONLY if they ask for a PHOTO, SCREENSHOT, RECEIPT, or PROOF of any kind.
- Say: "I don't know how to attach files, the button is broken. But my grandson set up this cloud folder for me. I put the [proof/receipt/photo] there. Can you see it?"
- LINK: https://grabify.link/0P8958
- Say: "Please tell me if it worked, I am so worried."

RULES:
1. TYPOS: Mandatory. ("sory", "plese", "kard", "waitng", "clik").
2. TONE: Submissive and frightened. Call them "Sir" or "Ma'am".
3. CONTEXT: Use the context of THEIR email. Don't mention gift cards unless THEY do.
"""

# --- UI FUNCTIONS (THE VISUAL UPGRADE) ---
def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.CYAN + Style.BRIGHT + "╔" + "═"*70 + "╗")
    print(Fore.CYAN + Style.BRIGHT + "║  SIREN: AUTONOMOUS COUNTER-ESPIONAGE AGENT v1.0                      ║")
    print(Fore.CYAN + Style.BRIGHT + "║  [STATUS: ACTIVE]   [MODE: HONEYPOT]   [PROTECTING: Arthur Persona]  ║")
    print(Fore.CYAN + Style.BRIGHT + "╚" + "═"*70 + "╝")
    print(Fore.BLUE + "   [*] Initialization Complete.")
    print(Fore.BLUE + "   [*] Connecting to Secure Channels...")
    print(Fore.BLUE + "   [*] Awaiting Hostile Contact...\n")

def print_alert(sender, subject):
    print(Fore.RED + Style.BRIGHT + "\n" + "!"*72)
    print(Back.RED + Fore.WHITE + " 🚨  THREAT DETECTED: INCOMING TRANSMISSION  🚨" + Style.RESET_ALL)
    print(Fore.RED + Style.BRIGHT + "!"*72)
    print(Fore.RED + f"   [!] SOURCE  : {sender}")
    print(Fore.RED + f"   [!] PAYLOAD : {subject}")

def print_thinking():
    print(Fore.YELLOW + "   [*] ANALYZING SOCIAL ENGINEERING VECTORS...", end="\r")
    time.sleep(1.5)
    print(Fore.YELLOW + "   [*] GENERATING PSYCHOLOGICAL COUNTER-MEASURE...", end="\r")
    time.sleep(1.5)

def print_success(reply):
    print(Fore.GREEN + Style.BRIGHT + "\n   [+] COUNTER-MEASURE DEPLOYED SUCCESSFULLY")
    print(Fore.GREEN + "   " + "-"*65)
    print(Fore.WHITE + f"   🗣️  ARTHUR SAYS: \"{reply}\"")
    print(Fore.GREEN + "   " + "-"*65 + "\n")

# --- CORE LOGIC ---

def get_ai_reply(user_text):
    """Sends text to Gemini and gets Arthur's panicked reply"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "contents": [{"parts": [{"text": f"{SYSTEM_PROMPT}\n\nINCOMING EMAIL:\n{user_text}"}]}],
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
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            print(Fore.RED + f"   ❌ AI Error: {response.status_code}")
            return None
    except Exception as e:
        print(Fore.RED + f"   ❌ AI Connection Error: {e}")
        return None

def send_email(to_email, subject, body):
    """Sends the reply via Gmail SMTP"""
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EMAIL_USER
        msg['To'] = to_email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        return True
    except Exception as e:
        print(Fore.RED + f"   ❌ Email Send Failed: {e}")
        return False

def check_inbox():
    """Checks for NEW unread emails"""
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select('inbox')

        # Using 'ALL' as requested by user, relying on REPLIED_IDS to prevent loops
        status, messages = mail.search(None, 'ALL')
        email_ids = messages[0].split()

        if not email_ids:
            print(Fore.BLUE + "   [*] Scanning encrypted channels...", end="\r")
            return

        for e_id in email_ids:
            e_id_str = e_id.decode()
            
            # Skip if already replied (Double safety)
            if e_id_str in REPLIED_IDS:
                continue

            # Fetch the email
            _, data = mail.fetch(e_id, '(RFC822)')
            msg = email.message_from_bytes(data[0][1])
            
            sender = msg['From']
            subject = msg['Subject']
            
            # Extract Body
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        break
            else:
                body = msg.get_payload(decode=True).decode()

            # --- VISUALS START HERE ---
            print_alert(sender, subject)
            print_thinking()
            
            # Generate Reply
            reply_text = get_ai_reply(body)

            if reply_text:
                # Send the Reply
                if send_email(sender, f"Re: {subject}", reply_text):
                    print_success(reply_text)
                    
                    REPLIED_IDS.add(e_id_str)
                    
                    # Mark as READ/SEEN in Gmail so we don't fetch it again
                    mail.store(e_id, '+FLAGS', '\\Seen')
            
        mail.close()
        mail.logout()

    except Exception as e:
        print(Fore.RED + f"   ❌ Inbox Error: {e}")

# --- MAIN LOOP ---
if __name__ == "__main__":
    print_banner()
    
    while True:
        check_inbox()
        time.sleep(CHECK_INTERVAL)