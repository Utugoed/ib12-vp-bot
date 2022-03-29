import os
import dotenv

dotenv.load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_DB = "IB12"
MONGO_URL = os.getenv("MONGO_URL")
