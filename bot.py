import os
import logging
import asyncio
import uvicorn
from fastapi import FastAPI
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

# Turn on logging to track launch actions
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ⚠️ PASTE YOUR NEW SUDOKU BOT TOKEN HERE:
BOT_TOKEN = "8987066592:AAE-efiINGLWXyFhaZ_dF1vGEmF2LZGhTWc"

# ⚠️ PASTE YOUR SECURE GITHUB PAGES LINK HERE:
MINI_APP_URL = "https://oogway87.github.io/sudoku-game/"

# FastAPI setup to handle Render's web port requirement easily
api_app = FastAPI()

@api_app.get("/")
def home():
    return {"status": "Sudoku Launching Bot is Online"}

# Command Handler: Sends the Mini App access button to the player
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # WebAppInfo binds your live website url link to a special Telegram internal protocol handler
    webapp_config = WebAppInfo(url=MINI_APP_URL)
    
    # Create an elegant inline keyboard attachment link block
    keyboard = [[
        InlineKeyboardButton(text="Play Sudoku 🎮", web_app=webapp_config)
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🧠 Welcome to the Sudoku Mini App Game!\n\n"
        "Tap the button below to open the game in full-screen mode right inside Telegram. Let's play!",
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
