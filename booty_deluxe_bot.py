import asyncio
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

import os

# Set BOT_TOKEN as an environment variable (never commit tokens to GitHub)
BOT_TOKEN = os.environ["BOT_TOKEN"]

# Growing animation frames
GROW_FRAMES = [
    (
        "```\n"
        "\n\n\n\n\n"
        "▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        "```"
    ),
    (
        "```\n"
        "\n\n\n\n"
        "        🌰\n"
        "▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        "```"
    ),
    (
        "```\n"
        "\n\n\n"
        "        |\n"
        "        |\n"
        "▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        "```"
    ),
    (
        "```\n"
        "\n\n"
        "       \\|/\n"
        "        |\n"
        "        |\n"
        "▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        "```"
    ),
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
]

GROW_DELAYS = [1.0, 1.0, 0.8, 0.8, 0.7]

# The booty showcase — many different types!
BOOTIES = [
    # Classic thicc
    (
        "```\n"
        " ✨ ▓▓▓▓▓▓  ▓▓▓▓▓▓ ✨\n"
        "  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        " ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        " ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        "  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        "   ▓▓▓▓▓▓  ▓▓▓▓▓▓\n"
        "    ▓▓▓▓    ▓▓▓▓\n"
        "```\n"
        "🍑 T H I C C   C L A S S I C 🍑"
    ),
    # Bubble butt
    (
        "```\n"
        "    @@@@    @@@@\n"
        "  @@@@@@@@@@@@@@@@\n"
        " @@@@@@@@@@@@@@@@@@\n"
        "@@@@@@@@@@@@@@@@@@@@\n"
        "@@@@@@@@@@@@@@@@@@@@\n"
        " @@@@@@@@@@@@@@@@@@\n"
        "  @@@@@@    @@@@@@\n"
        "```\n"
        "🫧 B U B B L E   B U T T 🫧"
    ),
    # Pixelated peach
    (
        "```\n"
        "    ████    ████\n"
        "  ██░░████████░░██\n"
        " ██░░░░██████░░░░██\n"
        " ██░░░░██████░░░░██\n"
        "  ██░░████████░░██\n"
        "   ████    ████\n"
        "    ██      ██\n"
        "```\n"
        "🎮 P I X E L   P E A C H 🎮"
    ),
    # Heart-shaped
    (
        "```\n"
        "   ♥♥♥♥    ♥♥♥♥\n"
        "  ♥♥♥♥♥♥♥♥♥♥♥♥♥♥\n"
        " ♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥\n"
        " ♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥\n"
        "  ♥♥♥♥♥♥♥♥♥♥♥♥♥♥\n"
        "    ♥♥♥♥♥♥♥♥♥♥\n"
        "      ♥♥♥♥♥♥\n"
        "```\n"
        "❤️ H E A R T   B O O T Y ❤️"
    ),
    # Jiggly
    (
        "```\n"
        "  ~ ████  ████ ~\n"
        " ~ ██████████████ ~\n"
        "~ ████████████████ ~\n"
        "~ ████████████████ ~\n"
        " ~ ██████████████ ~\n"
        "  ~ ████  ████ ~\n"
        "   ~ ██    ██ ~\n"
        "```\n"
        "🌊 J I G G L Y   J E L L Y 🌊"
    ),
    # Tiny but mighty
    (
        "```\n"
        "\n"
        "\n"
        "      ()  ()\n"
        "     ()()()()\n"
        "      ()()()\n"
        "       ()()\n"
        "\n"
        "```\n"
        "🐜 S M O L   B O O T Y 🐜"
    ),
    # Extra wide
    (
        "```\n"
        "  ██████████  ██████████\n"
        " ████████████████████████\n"
        "██████████████████████████\n"
        "██████████████████████████\n"
        " ████████████████████████\n"
        "  ██████████  ██████████\n"
        "   ████████    ████████\n"
        "```\n"
        "🏋️ E X T R A   W I D E 🏋️"
    ),
    # Galaxy booty
    (
        "```\n"
        "   .*★*..    ..*★*.\n"
        "  ★*....*★★★*....*★\n"
        " ★*......*★★*......*★\n"
        " ★*......*★★*......*★\n"
        "  ★*....*★  ★*....*★\n"
        "   .*★*.      .*★*.\n"
        "    .*★.      .*★.\n"
        "```\n"
        "🌌 G A L A X Y   B O O T Y 🌌"
    ),
    # Robo-booty
    (
        "```\n"
        "   [####]  [####]\n"
        "  [################]\n"
        " [##################]\n"
        " [##################]\n"
        "  [################]\n"
        "   [####]  [####]\n"
        "    [##]    [##]\n"
        "```\n"
        "🤖 R O B O   B O O T Y 🤖"
    ),
    # Mega booty finale
    (
        "```\n"
        " 🔥▓▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓▓🔥\n"
        "  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        " ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        "▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        " ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        "  ▓▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓▓\n"
        "   ▓▓▓▓▓▓    ▓▓▓▓▓▓\n"
        "```\n"
        "🔥 M E G A   B O O T Y 🔥"
    ),
]

BOOTY_DELAY = 1.2  # seconds between each booty in the showcase


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

    # Phase 1: grow animation
    for i, frame in enumerate(GROW_FRAMES):
        try:
            await msg.edit_text(frame, parse_mode="Markdown")
            if GROW_DELAYS[i] > 0:
                await asyncio.sleep(GROW_DELAYS[i])
        except Exception:
            pass

    # Phase 2: cycle through the booty showcase
    for booty in BOOTIES:
        try:
            await msg.edit_text(booty, parse_mode="Markdown")
            await asyncio.sleep(BOOTY_DELAY)
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
