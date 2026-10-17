import os
import logging
import asyncio
import uvicorn
from fastapi import FastAPI
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ⚠️ PASTE YOUR SECURE ACCREDITATION KEYS HERE:
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_SUDOKU_BOT_TOKEN_HERE")

# Raw clean path link to your repository site view
MINI_APP_URL = "https://oogway87.github.io/sudoku-game/?v=2"

api_app = FastAPI()

@api_app.get("/")
def home():
    return {"status": "Clean Sudoku Launcher is Online"}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    webapp_config = WebAppInfo(url=MINI_APP_URL)
    
    keyboard = [[
        InlineKeyboardButton(text="Play Sudoku 🎮", web_app=webapp_config)
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🧠 Welcome to the Standalone Sudoku Mini App!\n\n"
        "Tap the action button below to play a fully-featured, touch-responsive puzzle game grid right inside Telegram!",
        reply_markup=reply_markup
    )

async def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    port = int(os.environ.get("PORT", 10000))
    config = uvicorn.Config(app=api_app, host="0.0.0.0", port=port, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())