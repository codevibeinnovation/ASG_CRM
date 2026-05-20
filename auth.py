import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID=os.getenv("CLIENT_ID")

CLIENT_SECRET=os.getenv("CLIENT_SECRET")

GOOGLE_REDIRECT_URI=os.getenv("GOOGLE_REDIRECT_URI")

SECRET_KEY=os.getenv("SECRET_KEY")

ALGORITHM=os.getenv("ALGORITHM")

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")