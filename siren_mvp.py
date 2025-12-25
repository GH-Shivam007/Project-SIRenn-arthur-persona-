import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Get the credentials
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

print(f"✅ Loaded User: {EMAIL_USER}")
# Test print to make sure it loaded (delete this line after testing!)