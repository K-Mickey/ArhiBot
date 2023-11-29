import os
from dotenv import load_dotenv

load_dotenv()

ID_SENDER = os.getenv("ID_SENDER")
ID_ADMINS = os.getenv("ID_ADMIN").split()
BOT_TOKEN = os.getenv("BOT_TOKEN")

PATH_DB = "src/db/database.db"
