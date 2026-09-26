import os
import logging
import feedparser
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging to easily debug on Railway
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = os.getenv("TELEGRAM_TOKEN")

FEEDS = {
    "football": "http://feeds.bbci.co.uk/sport/football/rss.xml",
    "sports": "http://feeds.bbci.co.uk/sport/rss.xml"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚽ Welcome to the Sport News Bot!\n\n"
        "Commands:\n"
        "/football - Latest Football News\n"
        "/sports - Top Sports News"
    )

async def get_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command = update.message.text.replace("/", "").lower()
    feed_url = FEEDS.get(command, FEEDS["football"])
    
    parsed_feed = feedparser.parse(feed_url)
    entries = parsed_feed.entries[:5]

    if not entries:
        await update.message.reply_text("Unable to fetch news at this moment.")
        return

    response = f"📰 Latest {command.capitalize()} News:\n\n"
    for item in entries:
        response += f"• {item.title}\n{item.link}\n\n"

    await update.message.reply_text(response, disable_web_page_preview=True)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send /football or /sports to get the latest sports news!")

if __name__ == "__main__":
    if not TOKEN:
        raise ValueError("TELEGRAM_TOKEN environment variable is not set!")

    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("football", get_news))
    app.add_handler(CommandHandler("sports", get_news))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Bot starting polling...")
    app.run_polling()
