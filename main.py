from config import bot
from scraper import Scraper

@bot.message_handler(commands=['start'])
def on_start(message): 
    bot.send_message(message.chat.id, "Send command /scrape to start Scrape")

@bot.message_handler(commands=["scrape"])
def on_uri_specified(message):
    bot.send_message(message.chat.id, "Send  goldenpages category link to start scrape")
    bot.register_next_step_handler(message, on_name_specified)

def on_name_specified(message):
    bot.send_message(message.chat.id, "Send name for excel file")
    uri = message.text
    bot.register_next_step_handler(message, on_start_scrape_specified, uri)

def on_start_scrape_specified(message, uri):
    bot.send_message(message.chat.id, "Starting Scrape")
    name = message.text
    scraper = Scraper(uri=uri, name=name, chat_id=message.chat.id)
    scraper.get_data()

if __name__ == '__main__':
    bot.infinity_polling()