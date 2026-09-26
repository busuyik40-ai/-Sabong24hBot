import os
import feedparser
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Telegram Bot Token from environment variable
TOKEN = os.getenv("TELEGRAM_TOKEN")

# RSS Feeds for Sports & Football News (No API Keys Required)
FEEDS = {
    "football": "http://feeds.bbci.co.uk/sport/football/rss.xml",
    "sports": "http://feeds.bbci.co.uk/sport/rss.xml"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚽ Welcome to the Sports News Bot!\n\n"
        "Commands:\n"
        "/football - Latest Football Headlines\n"
        "/sports - Top Sports News"
    )

async def get_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command = update.message.text.replace("/", "").lower()
    feed_url = FEEDS.get(command)
    
    if not feed_url:
        return

    parsed_feed = feedparser.parse(feed_url)
    entries = parsed_feed.entries[:5]  # Get top 5 news stories

    if not entries:
        await update.message.reply_text("No news found at the moment.")
        return

    response = f"📰 **Latest {command.capitalize()} News:**\n\n"
    for item in entries:
        response += f"• [{item.title}]({item.link})\n"

    await update.message.reply_text(response, parse_mode="Markdown", disable_web_page_preview=True)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("football", get_news))
    app.add_handler(CommandHandler("sports", get_news))
    
    print("Bot is running...")
    app.run_polling()
