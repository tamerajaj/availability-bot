"""
Telegram bot to check and change availability of two people.
"""

import logging

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import (Application,    CommandHandler,    ContextTypes,    MessageHandler,    filters,    PicklePersistence,)

import os

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! Type /help for a list of available instructions.",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_message = """
    Available commands are:
    /check : check status
    /t_busy : T is busy
    /t_avail : T is available 
    /m_busy : M is busy
    /m_avail : M is available 
    """
    await update.message.reply_text(help_message)


async def check_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Check the status."""
    bot_data = context.bot_data
    t_status = "available" if bot_data.get("t_status", False) else "busy"
    m_status = "available" if bot_data.get("m_status", False) else "busy"
    status_text = f"T status: {t_status}\nM status: {m_status}"
    await update.message.reply_text(status_text)


async def t_status_available(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Set T status as available.
    """
    bot_data = context.bot_data
    bot_data["t_status"] = True
    await update.message.reply_text("T is now available.")


async def m_status_available(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Set M status as available."""
    bot_data = context.bot_data
    bot_data["m_status"] = True
    await update.message.reply_text("M is now available.")


async def t_status_busy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Set T status as busy."""
    bot_data = context.bot_data
    bot_data["t_status"] = False
    await update.message.reply_text("T is now busy.")


async def m_status_busy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Set M status as busy."""
    bot_data = context.bot_data
    bot_data["m_status"] = False
    await update.message.reply_text("M is now busy.")


def main() -> None:
    """Start the bot."""
    # Create the PicklePersistence instance and pass the file name
    persistence = PicklePersistence(filepath="/data/data.pkl")
    # Create the Application and pass it your bot's token.
    assert (
        bot_token := os.environ.get("TOKEN")
    ), "Please, set environment var TOKEN with your bot token"
    application = (
        Application.builder().token(bot_token).persistence(persistence).build()
    )

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("t_avail", t_status_available))
    application.add_handler(CommandHandler("m_avail", m_status_available))
    application.add_handler(CommandHandler("t_busy", t_status_busy))
    application.add_handler(CommandHandler("m_busy", m_status_busy))
    application.add_handler(CommandHandler("check", check_status))
    # on non command i.e. message - send the /help message on Telegram
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, help_command)
    )

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
