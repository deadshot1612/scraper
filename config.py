import os
import telebot
from dotenv import load_dotenv


from pathlib import Path


BASE_DIR = Path(__file__).parent
env_file = BASE_DIR/'.env'

if env_file.exists():
    load_dotenv(env_file)

bot = telebot.TeleBot(token=os.environ['TOKEN'])