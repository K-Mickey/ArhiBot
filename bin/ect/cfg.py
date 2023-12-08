import os
from dotenv import load_dotenv

load_dotenv()

ID_SENDER = os.getenv("ID_SENDER")
ID_ADMINS = os.getenv("ID_ADMIN").split()
BOT_TOKEN = os.getenv("BOT_TOKEN")

PATH_DB = "src/db/database.db"
PATH_STORAGE = "src/db/storage.db"

LOG_FORMATTER = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_PATH = "src/log/logging.log"
LOG_LEVEL = "WARNING"

COLUMN_KEY = "выберите рубрики"
BYE_MSG = "<b>Большое спасибо за ваше внимание и ответ!</b>\n" \
           "Если вы хотите продолжить взаимодействие, " \
          "нажимайте на меню внизу"