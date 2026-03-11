import asyncio
import time
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, ContextTypes,
    ConversationHandler, MessageHandler, filters,
)

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

# Outro sequence after the showcase
OUTRO_FRAMES = [
    # Big thumbs up
    (
        "```\n"
        "        ██\n"
        "       ██\n"
        "      ██\n"
        "  ██████████\n"
        "  ██████████\n"
        "  ██████████\n"
        "  ██████████\n"
        "```\n"
        "👍 N I C E 👍"
    ),
    # Big cartoon eyes
    (
        "```\n"
        "  ████████  ████████\n"
        " ██  ●●  ████  ●●  ██\n"
        " ██  ●●  ████  ●●  ██\n"
        "  ████████  ████████\n"
        "```\n"
        "👀 L O O K I N   G O O D 👀"
    ),
    # Another thumbs up
    (
        "```\n"
        "    ██          ██\n"
        "   ██          ██\n"
        "  ██          ██\n"
        " ████████  ████████\n"
        " ████████  ████████\n"
        " ████████  ████████\n"
        " ████████  ████████\n"
        "```\n"
        "👍👍 D O U B L E   N I C E 👍👍"
    ),
]

OUTRO_DELAY = 1.3

# Loading bar frames
LOADING_FRAMES = [
    "```\n[░░░░░░░░░░░░░░░░░░░░]\n```\n⏳ loading booties...",
    "```\n[████░░░░░░░░░░░░░░░░]\n```\n⏳ loading booties...",
    "```\n[████████░░░░░░░░░░░░]\n```\n⏳ loading booties...",
    "```\n[████████████░░░░░░░░]\n```\n⏳ loading booties...",
    "```\n[████████████████░░░░]\n```\n⏳ loading booties...",
    "```\n[████████████████████]\n```\n⏳ loading booties...",
]

LOADING_DELAY = 0.4

# Conversation state
WAITING_FOR_YES = 0


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌱 Welcome to *Booty Deluxe Bot*\n\n"
        "Send /grow to plant a seed and watch it bloom.\n\n"
        "You have been warned. 🍑",
        parse_mode="Markdown"
    )


async def _play_showcase(msg):
    """Play the booty showcase + outro + loading bar on an existing message."""
    # Booty showcase
    for booty in BOOTIES:
        try:
            await msg.edit_text(booty, parse_mode="Markdown")
            await asyncio.sleep(BOOTY_DELAY)
        except Exception:
            pass

    # Outro sequence
    for frame in OUTRO_FRAMES:
        try:
            await msg.edit_text(frame, parse_mode="Markdown")
            await asyncio.sleep(OUTRO_DELAY)
        except Exception:
            pass

    # Loading bar animation
    for frame in LOADING_FRAMES:
        try:
            await msg.edit_text(frame, parse_mode="Markdown")
            await asyncio.sleep(LOADING_DELAY)
        except Exception:
            pass

    # Final prompt
    try:
        await msg.edit_text("🍑 *more booty bots?*\n\nType *yes* to keep it going!", parse_mode="Markdown")
    except Exception:
        pass


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

    # Phase 2 + 3: showcase + outro + "more booty bots?"
    await _play_showcase(msg)

    # Store the message so we can reuse it on "yes"
    context.user_data["booty_msg"] = msg
    return WAITING_FOR_YES


async def handle_yes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = context.user_data.get("booty_msg")
    if not msg:
        msg = await update.message.reply_text("🍑 Here we go again!")
        context.user_data["booty_msg"] = msg

    # Delete the user's "yes" to keep chat clean
    try:
        await update.message.delete()
    except Exception:
        pass

    await _play_showcase(msg)
    return WAITING_FOR_YES


async def handle_no(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🍑 Until next time... stay bootylicious! 👋"
    )
    return ConversationHandler.END


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("grow", grow)],
        states={
            WAITING_FOR_YES: [
                MessageHandler(filters.Regex(r"(?i)^yes"), handle_yes),
            ],
        },
        fallbacks=[MessageHandler(filters.ALL, handle_no)],
    )
    app.add_handler(conv_handler)

    print("🍑 Booty Deluxe Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
