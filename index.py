import requests
from io import BytesIO
from queue import Queue
import json
import logging
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler, Dispatcher
from movies_scraper import search_movies, get_movie

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.getenv("TOKEN")
URL = os.getenv("URL")
bot = Bot(TOKEN)

def welcome(update, context) -> None:
    """Sends the welcome message to the user."""

    update.message.reply_text(f"Hello {update.message.from_user.first_name}, Welcome to Bard Movies.\n"
                               f"🔥 Download Your Favourite Movies For 💯 Free And 🍿 Enjoy it.")
    update.message.reply_text("👇 Enter Movie Name 👇")

def find_movie(update, context) -> None:
    """Searches for the specified movie and sends the user a list of search results."""

    query = update.message.text
    results = search_movies(query)

    if results:
        keyboards = []
        for result in results:
            keyboard = InlineKeyboardButton(result["title"], callback_data=result["id"])
            keyboards.append([keyboard])

        reply_markup = InlineKeyboardMarkup(keyboards)
        update.message.reply_text('Search Results...', reply_markup=reply_markup)
    else:
        update.message.reply_text('Sorry 🙏, No Result Found!\nCheck If You Have Misspelled The Movie Name.')

def movie_result(update, context) -> None:
    """Sends the user a photo of the movie poster and a list of download links."""

    query = update.callback_query
    movie = get_movie(query.data)

    response = requests.get(movie["img"])
    img = BytesIO(response.content)
    query.message.reply_photo(photo=img, caption=f"🎥 {movie['title']}")

    link = ""
    links = movie["links"]
    for i in links:
        link += "🎬" + i + "\n" + links[i] + "\n\n"

    if len(link) > 4095:
        for x in range(0, len(link), 4095):
            query.message.reply_text(text=link[x:x+4095])
    else:
        query.message.reply_text(text=link)

def setup():
    """Sets up the Telegram bot."""

    update_queue = Queue()
    dispatcher = Dispatcher(bot, update_queue, use_context=True)
    dispatcher.add_handler(CommandHandler('start', welcome))
    dispatcher.add_handler(MessageHandler(Filters.text, find_movie))
    dispatcher.add_handler(CallbackQueryHandler(movie_result))

    return dispatcher

app = Flask(__name__)

@app.route('/')
def index():
    """Returns a simple index page."""

    return 'Hello World!'

@app.route('/{}'.format(TOKEN), methods=['GET', 'POST'])
def respond():
    """Processes incoming Telegram updates."""

    update = Update.de_json(request.get_json(force=True), bot)
    setup().process_update(update)

    return 'ok'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    """Sets the Telegram bot's webhook."""

    s = bot.setWebhook('{URL}/{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

if __name__ == '__main__':
    app.run(debug=True)
