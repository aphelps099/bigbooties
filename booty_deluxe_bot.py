import asyncio
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

import os

# Set BOT_TOKEN as an environment variable (never commit tokens to GitHub)
BOT_TOKEN = os.environ["BOT_TOKEN"]

# Animation frames - seed grows into pixelated booty
FRAMES = [
    # Frame 1: bare ground
    (
        "```\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        "```"
    ),
    # Frame 2: seed
    (
        "```\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "        🌰\n"
        "▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        "```"
    ),
    # Frame 3: sprout
    (
        "```\n"
        "\n"
        "\n"
        "\n"
        "        |\n"
        "        |\n"
        "▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        "```"
    ),
    # Frame 4: growing
    (
        "```\n"
        "\n"
        "\n"
        "       \\|/\n"
        "        |\n"
        "        |\n"
        "▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        "```"
    ),
    # Frame 5: blooming - small shape
    (
        "```\n"
        "\n"
        "      ██████\n"
        "     ████████\n"
        "      ██████\n"
        "        |\n"
        "▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        "```"
    ),
    # Frame 6: transforming
    (
        "```\n"
        "\n"
        "    ████  ████\n"
        "   ██████████████\n"
        "   ██████████████\n"
        "    ████████████\n"
        "▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        "```"
    ),
    # Frame 7: the booty emerges
    (
        "```\n"
        "    ████    ████\n"
        "  ████████████████\n"
        "  ██████████████████\n"
        "  ██████████████████\n"
        "   ████████████████\n"
        "     ████    ████\n"
        "```"
    ),
    # Frame 8: FULL BOOTY - big pixels
    (
        "```\n"
        "   ▓▓▓▓▓▓  ▓▓▓▓▓▓\n"
        "  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        " ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        " ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        "  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        "   ▓▓▓▓▓▓  ▓▓▓▓▓▓\n"
        "    ▓▓▓▓    ▓▓▓▓\n"
        "```"
    ),
    # Frame 9: sparkle finale
    (
        "```\n"
        " ✨ ▓▓▓▓▓▓  ▓▓▓▓▓▓ ✨\n"
        "  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        " ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        " ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        "  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        "   ▓▓▓▓▓▓  ▓▓▓▓▓▓\n"
        "    ▓▓▓▓    ▓▓▓▓  🍑\n"
        "```\n"
        "\n"
        "🍑 B O O T Y   D E L U X E 🍑"
    ),
]

DELAYS = [1.0, 1.0, 0.8, 0.8, 0.7, 0.7, 0.6, 0.5, 0.0]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌱 Welcome to *Booty Deluxe Bot*\n\n"
        "Send /grow to plant a seed and watch it bloom.\n\n"
        "You have been warned. 🍑",
        parse_mode="Markdown"
    )


async def grow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text(
        "```\n🌱 planting seed...\n```",
        parse_mode="Markdown"
    )
    await asyncio.sleep(1.2)

    for i, frame in enumerate(FRAMES):
        try:
            await msg.edit_text(frame, parse_mode="Markdown")
            if DELAYS[i] > 0:
                await asyncio.sleep(DELAYS[i])
        except Exception:
            pass


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("grow", grow))
    print("🍑 Booty Deluxe Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
