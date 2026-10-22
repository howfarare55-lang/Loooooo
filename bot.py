
import os
import logging

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ---------------- CONFIGURATION ----------------

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

# ---------------- MENU ----------------

def main_menu():
    keyboard = [
        [
            InlineKeyboardButton("📰 Football News", callback_data="news"),
            InlineKeyboardButton("🔮 Predictions", callback_data="predictions"),
        ],
        [
            InlineKeyboardButton("📅 Today's Matches", callback_data="matches"),
            InlineKeyboardButton("🔴 Live Scores", callback_data="scores"),
        ],
        [
            InlineKeyboardButton("🏆 League Tables", callback_data="leagues"),
            InlineKeyboardButton("ℹ️ Help", callback_data="help"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


WELCOME_MESSAGE = (
    "⚽ Welcome to Footy News Bot!\n\n"
    "Your simple football companion for news, fixtures, "
    "scores, and match analysis.\n\n"
    "👇 Choose an option below to get started."
)


# ---------------- COMMANDS ----------------

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    await update.effective_message.reply_text(
        WELCOME_MESSAGE,
        reply_markup=main_menu(),
    )


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    message = (
        "ℹ️ HOW TO USE THIS BOT\n\n"
        "/start - Open the main menu\n"
        "/menu - Show the menu again\n"
        "/news - Football news\n"
        "/matches - Today's matches\n"
        "/predictions - Match predictions\n"
        "/help - Get help\n\n"
        "Tap a menu button to explore the available features."
    )

    await update.effective_message.reply_text(
        message,
        reply_markup=main_menu(),
    )


async def menu_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    await update.effective_message.reply_text(
        "⚽ What would you like to check?",
        reply_markup=main_menu(),
    )


# ---------------- FEATURE RESPONSES ----------------

async def show_news(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    message = (
        "📰 FOOTBALL NEWS\n\n"
        "Football news will appear here when a news API "
        "is connected.\n\n"
        "The next step is to connect a real football news source "
        "for updated headlines and transfer news."
    )

    await update.effective_message.reply_text(
        message,
        reply_markup=main_menu(),
    )


async def show_matches(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    message = (
        "📅 TODAY'S MATCHES\n\n"
        "Fixtures and kickoff times will appear here after "
        "we connect a football data API.\n\n"
        "Match times should be displayed in the correct timezone."
    )

    await update.effective_message.reply_text(
        message,
        reply_markup=main_menu(),
    )


async def show_predictions(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    message = (
        "🔮 MATCH PREDICTIONS\n\n"
        "Choose a match for analysis once football data is connected.\n\n"
        "The bot can then estimate:\n"
        "⚽ Possible match outcome\n"
        "🥅 Over/under goals\n"
        "🤝 Both teams to score\n"
        "📊 Supporting statistics\n\n"
        "Predictions are estimates, not guaranteed results."
    )

    await update.effective_message.reply_text(
        message,
        reply_markup=main_menu(),
    )


async def show_scores(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    message = (
        "🔴 LIVE SCORES\n\n"
        "Live scores and match status will appear here "
        "after we connect a live football data provider."
    )

    await update.effective_message.reply_text(
        message,
        reply_markup=main_menu(),
    )


async def show_leagues(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    message = (
        "🏆 LEAGUE TABLES\n\n"
        "Choose a competition to see its standings once "
        "the football data API is connected:\n\n"
        "🇬🇧 Premier League\n"
        "🇪🇸 La Liga\n"
        "🇮🇹 Serie A\n"
        "🇩🇪 Bundesliga\n"
        "🇫🇷 Ligue 1\n"
        "🌍 UEFA Champions League"
    )

    await update.effective_message.reply_text(
        message,
        reply_markup=main_menu(),
    )


# ---------------- BUTTON HANDLER ----------------

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query

    # Acknowledge the button tap.
    await query.answer()

    actions = {
        "news": show_news,
        "matches": show_matches,
        "predictions": show_predictions,
        "scores": show_scores,
        "leagues": show_leagues,
        "help": help_command,
    }

    action = actions.get(query.data)

    if action:
        # Reuse the feature functions for button clicks.
        await action(update, context)


# ---------------- START BOT ----------------

def main():
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN is missing. Set it in your environment variables."
        )

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("news", show_news))
    app.add_handler(CommandHandler("matches", show_matches))
    app.add_handler(CommandHandler("predictions", show_predictions))

    app.add_handler(CallbackQueryHandler(button_handler))

    logger.info("Football Telegram bot is starting...")

    # Polling is suitable for a Railway worker service.
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
