import asyncio
import random
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

BOOTY_DELAY = 1.2

# Outro sequence
OUTRO_FRAMES = [
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
    (
        "```\n"
        "  ████████  ████████\n"
        " ██  ●●  ████  ●●  ██\n"
        " ██  ●●  ████  ●●  ██\n"
        "  ████████  ████████\n"
        "```\n"
        "👀 L O O K I N   G O O D 👀"
    ),
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

# --- NEW STUFF: legendary, hype, shake, streaks ---

LEGENDARY_BOOTIES = [
    (
        "```\n"
        "   💎💎💎💎    💎💎💎💎\n"
        "  💎💎💎💎💎💎💎💎💎💎💎💎\n"
        " 💎💎💎💎💎💎💎💎💎💎💎💎💎💎\n"
        " 💎💎💎💎💎💎💎💎💎💎💎💎💎💎\n"
        "  💎💎💎💎💎💎💎💎💎💎💎💎\n"
        "   💎💎💎💎    💎💎💎💎\n"
        "```\n"
        "💎 D I A M O N D   B O O T Y 💎"
    ),
    "👻 ...where did it go?\n\n(invisible booty -- only the worthy can see it)",
    (
        "```\n"
        "   $$$$$$    $$$$$$\n"
        "  $$$$$$$$$$$$$$$$$$\n"
        " $$$$$$$$$$$$$$$$$$$$\n"
        " $$$$$$$$$$$$$$$$$$$$\n"
        "  $$$$$$$$$$$$$$$$$$\n"
        "   $$$$$$    $$$$$$\n"
        "    $$$$      $$$$\n"
        "```\n"
        "💰 G O L D E N   B O O T Y 💰"
    ),
    (
        "```\n"
        "    ▓▓▓▓    ▓▓▓▓\n"
        "   ▓▓▓▓▓▓  ▓▓▓▓▓▓\n"
        "  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        " ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        " ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        "  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        "       ▓▓▓▓▓▓\n"
        "```\n"
        "🙃 U P S I D E   D O W N 🙃"
    ),
    (
        "```\n"
        "   🟥🟧🟨🟩    🟥🟧🟨🟩\n"
        "  🟥🟧🟨🟩🟦🟪🟥🟧🟨🟩🟦🟪\n"
        " 🟥🟧🟨🟩🟦🟪🟥🟧🟨🟩🟦🟪🟥🟧\n"
        " 🟥🟧🟨🟩🟦🟪🟥🟧🟨🟩🟦🟪🟥🟧\n"
        "  🟥🟧🟨🟩🟦🟪🟥🟧🟨🟩🟦🟪\n"
        "   🟥🟧🟨🟩    🟥🟧🟨🟩\n"
        "```\n"
        "🌈 R A I N B O W   B O O T Y 🌈"
    ),
]

HYPE_MESSAGES = [
    "🔊 OH LAWD HE COMIN",
    "📏 A B S O L U T E   U N I T",
    "💅 she thicc",
    "✅ certified bootylicious",
    "🚨 BOOTY ALERT 🚨",
    "📈 STONKS (booty edition)",
    "🏆 HALL OF FAME MATERIAL",
    "😤 RESPECTFULLY... SHEEEESH",
    "🧲 gravitational pull detected",
    "🗣️ TALK TO ME NICE",
    "👨‍🍳 chef's kiss",
    "🪐 that thang got its own orbit",
]

STREAK_MESSAGES = {
    2: "🍑🍑 Round 2! Back for more!",
    3: "🍑🍑🍑 Round 3! Can't stop won't stop!",
    4: "🍑🍑🍑🍑 Round 4! This is getting serious...",
    5: "🔥🔥🔥🔥🔥 Round 5!! BOOTY ADDICTION",
    7: "⚠️ Round 7!!! Are you okay??",
    10: "💀 Round 10!!! SEEK HELP (but also... yes)",
    15: "🏆 Round 15. You are a LEGEND.",
    20: "👑 Round 20. You have ascended. You ARE the booty.",
}

SHAKE_FRAMES = [
    (
        "```\n"
        "▓▓▓▓▓▓  ▓▓▓▓▓▓\n"
        " ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        "▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        "▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        " ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        "  ▓▓▓▓▓▓  ▓▓▓▓▓▓\n"
        "```\n"
        "🍑 <<< SHAKE <<<"
    ),
    (
        "```\n"
        "    ▓▓▓▓▓▓  ▓▓▓▓▓▓\n"
        "   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        "  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        "  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        "   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        "    ▓▓▓▓▓▓  ▓▓▓▓▓▓\n"
        "```\n"
        "🍑 === SHAKE ==="
    ),
    (
        "```\n"
        "        ▓▓▓▓▓▓  ▓▓▓▓▓▓\n"
        "       ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        "      ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        "      ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        "       ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n"
        "        ▓▓▓▓▓▓  ▓▓▓▓▓▓\n"
        "```\n"
        "🍑 >>> SHAKE >>>"
    ),
]

SHAKE_DELAY = 0.3

# Conversation state
WAITING_FOR_YES = 0


def _get_streak_message(streak):
    """Get the best matching streak message for the current round."""
    best = None
    for threshold in sorted(STREAK_MESSAGES.keys()):
        if streak >= threshold:
            best = STREAK_MESSAGES[threshold]
    return best


async def _play_showcase(msg, speed_factor=1.0, streak=0):
    """Play the booty showcase + outro + loading bar on an existing message."""
    # Streak announcement
    if streak >= 2:
        streak_msg = _get_streak_message(streak)
        if streak_msg:
            try:
                await msg.edit_text(streak_msg)
                await asyncio.sleep(1.5 * speed_factor)
            except Exception:
                pass

    # Shuffle booties for a fresh order every time
    shuffled = list(BOOTIES)
    random.shuffle(shuffled)

    # Booty showcase with legendary drops and hype
    for i, booty in enumerate(shuffled):
        # 15% chance to swap in a legendary
        if random.random() < 0.15:
            try:
                await msg.edit_text("⚡ L E G E N D A R Y   D R O P ⚡")
                await asyncio.sleep(0.8 * speed_factor)
            except Exception:
                pass
            booty = random.choice(LEGENDARY_BOOTIES)

        try:
            await msg.edit_text(booty, parse_mode="Markdown")
            await asyncio.sleep(BOOTY_DELAY * speed_factor)
        except Exception:
            pass

        # 30% chance to flash a hype message after a booty
        if random.random() < 0.30 and i < len(shuffled) - 1:
            try:
                hype = random.choice(HYPE_MESSAGES)
                await msg.edit_text(hype)
                await asyncio.sleep(0.8 * speed_factor)
            except Exception:
                pass

    # Outro sequence
    for frame in OUTRO_FRAMES:
        try:
            await msg.edit_text(frame, parse_mode="Markdown")
            await asyncio.sleep(OUTRO_DELAY * speed_factor)
        except Exception:
            pass

    # Loading bar animation
    for frame in LOADING_FRAMES:
        try:
            await msg.edit_text(frame, parse_mode="Markdown")
            await asyncio.sleep(LOADING_DELAY * speed_factor)
        except Exception:
            pass

    # Final prompt
    try:
        await msg.edit_text(
            "🍑 *more booty bots?*\n\nType *yes* to keep it going!",
            parse_mode="Markdown",
        )
    except Exception:
        pass


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌱 Welcome to *Booty Deluxe Bot*\n\n"
        "/grow - plant a seed and watch it bloom\n"
        "/shake - quick jiggle animation\n"
        "/random - instant random booty\n\n"
        "You have been warned. 🍑",
        parse_mode="Markdown",
    )


async def grow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text(
        "```\n🌱 planting seed...\n```",
        parse_mode="Markdown",
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
    context.user_data["streak"] = 1
    await _play_showcase(msg, speed_factor=1.0, streak=1)

    context.user_data["booty_msg"] = msg
    return WAITING_FOR_YES


async def handle_yes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    streak = context.user_data.get("streak", 0) + 1
    context.user_data["streak"] = streak
    speed_factor = max(0.3, 1.0 - 0.08 * (streak - 1))

    msg = context.user_data.get("booty_msg")
    if not msg:
        msg = await update.message.reply_text("🍑 Here we go again!")
        context.user_data["booty_msg"] = msg

    # Delete the user's "yes" to keep chat clean
    try:
        await update.message.delete()
    except Exception:
        pass

    await _play_showcase(msg, speed_factor=speed_factor, streak=streak)
    return WAITING_FOR_YES


async def handle_no(update: Update, context: ContextTypes.DEFAULT_TYPE):
    streak = context.user_data.get("streak", 1)
    if streak >= 5:
        farewell = f"🍑 {streak} rounds! You absolute legend. Stay bootylicious! 👋"
    else:
        farewell = "🍑 Until next time... stay bootylicious! 👋"
    await update.message.reply_text(farewell)
    return ConversationHandler.END


async def shake(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("🍑 initiating shake sequence...")
    await asyncio.sleep(0.5)
    for _ in range(4):
        for frame in SHAKE_FRAMES:
            try:
                await msg.edit_text(frame, parse_mode="Markdown")
                await asyncio.sleep(SHAKE_DELAY)
            except Exception:
                pass
    await msg.edit_text(
        "🍑 *SHAKE COMPLETE* 🍑\n\nBootylicious. 💅",
        parse_mode="Markdown",
    )


async def random_booty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    all_booties = BOOTIES + LEGENDARY_BOOTIES
    booty = random.choice(all_booties)
    hype = random.choice(HYPE_MESSAGES)
    await update.message.reply_text(
        f"{hype}\n\n{booty}",
        parse_mode="Markdown",
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("shake", shake))
    app.add_handler(CommandHandler("random", random_booty))

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
