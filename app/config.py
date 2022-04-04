import os
import dotenv

dotenv.load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_DB = "IB12"
MONGO_URL = os.getenv("MONGO_URL")

# webhook settings
WEBHOOK_HOST = 'https://KuricynIsAGod.pythonanywhere.com'
WEBHOOK_PATH = '/bot/{BOT_TOKEN}'
WEBHOOK_PORT = 8443
WEBHOOK_URL = f"{WEBHOOK_HOST}:{WEBHOOK_PORT}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 3001
