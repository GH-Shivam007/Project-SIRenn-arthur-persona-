import smtplib
import imaplib
import email
import os
from dotenv import load_dotenv

# 1. Load the credentials you just saved
load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def test_send():
    """Sends a test email to YOURSELF (the bot account)"""
    print(f"📤 Attempting to send email from {EMAIL_USER}...")
    try:
        # Connect to Gmail SMTP Server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            
            # Create a simple message
            subject = "Siren Connection Test"
            body = "If you are reading this, Python can send emails!"
            msg = f"Subject: {subject}\n\n{body}"
            
            # Send it to yourself
            server.sendmail(EMAIL_USER, EMAIL_USER, msg)
        print("✅ SUCCESS: Email sent!")
    except Exception as e:
        print(f"❌ FAILED to send: {e}")

def test_fetch():
    """Checks if we can see the email we just sent"""
    print("📥 Attempting to read inbox...")
    try:
        # Connect to Gmail IMAP Server
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select('inbox')
        
        # Search for all emails
        status, messages = mail.search(None, 'ALL')
        email_ids = messages[0].split()
        
        print(f"✅ SUCCESS: Connected! Found {len(email_ids)} emails in inbox.")
        
        if email_ids:
            # Fetch the latest one
            latest_id = email_ids[-1]
            _, data = mail.fetch(latest_id, '(RFC822)')
            msg = email.message_from_bytes(data[0][1])
            print(f"   🔎 Latest Subject: {msg['Subject']}")
            print(f"   👤 Latest Sender: {msg['From']}")
        else:
            print("   ⚠️ Inbox is empty (send an email to this account first!)")
            
        mail.close()
        mail.logout()
    except Exception as e:
        print(f"❌ FAILED to read: {e}")

if __name__ == "__main__":
    if not EMAIL_USER or not EMAIL_PASS:
        print("❌ ERROR: Could not find credentials in .env file.")
        print("   Make sure your file is named '.env' and variables are set.")
    else:
        test_send()
        print("-" * 30)
        test_fetch()