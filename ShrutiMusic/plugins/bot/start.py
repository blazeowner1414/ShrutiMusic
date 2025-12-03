import time
import random

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

import config
from ShrutiMusic import app
from ShrutiMusic.misc import _boot_
from ShrutiMusic.utils.database import add_served_user, add_served_chat
from ShrutiMusic.utils.decorators.language import LanguageStart
from ShrutiMusic.utils.formatters import get_readable_time
from ShrutiMusic.utils.inline import start_panel
from config import BANNED_USERS


# ================== RANDOM START IMAGES ================== #

START_IMAGES = [
    "https://t.me/blaze_photo_shop/3",
    "https://t.me/blaze_photo_shop/2",
]

def rand_img():
    return random.choice(START_IMAGES)


# ================== PRIVATE START ================== #

@app.on_message(filters.command("start") & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_private(_, message: Message, __):

    await add_served_user(message.from_user.id)

    caption = (
        "╭─〔 🔥 **BLAZE MUSIC** 🔥 〕─╮\n\n"
        f"👋 **Hey {message.from_user.first_name}**\n\n"
        "🎧 Music Bot for Telegram VC\n"
        "🚀 Low Lag • High Quality\n"
        "⚡ 24×7 Online\n\n"
        "╰──────────────╯"
    )

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "➕ ADD ME TO GROUP",
                    url=f"https://t.me/{app.username}?startgroup=true",
                )
            ],
            [
                InlineKeyboardButton("📖 Help & Commands", callback_data="help_menu"),
            ],
            [
                InlineKeyboardButton("💬 Support", url=config.SUPPORT_GROUP),
                InlineKeyboardButton("📢 Updates", url=config.SUPPORT_CHANNEL),
            ],
        ]
    )

    # MAIN WELCOME PHOTO
    await message.reply_photo(
        photo=rand_img(),
        caption=caption,
        reply_markup=buttons,
    )

    # ✅ SHONA STYLE STATUS MESSAGES
    await message.reply_text("🔔 **DING DONG.....🌹**")
    await message.reply_text("✅ **BOT STARTED.....zzZ**")
    await message.reply_text("🚀 **STARTING.....🔥**")


# ================== GROUP START ================== #

@app.on_message(filters.command("start") & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_group(_, message: Message, __):

    uptime = int(time.time() - _boot_)

    await message.reply_photo(
        photo=rand_img(),
        caption=(
            "✅ **BLAZE MUSIC ACTIVE**\n\n"
            f"⏱ **Uptime:** `{get_readable_time(uptime)}`\n\n"
            "🎶 Use `/play song name` to start music"
        ),
        reply_markup=InlineKeyboardMarkup(start_panel(__)),
    )

    await add_served_chat(message.chat.id)


# ================== BOT ADDED IN GROUP ================== #

@app.on_message(filters.new_chat_members)
async def bot_added(_, message: Message):
    for member in message.new_chat_members:
        if member.id == app.id:
            if message.chat.type != ChatType.SUPERGROUP:
                await message.reply_text("❌ Please add me in a supergroup.")
                return await app.leave_chat(message.chat.id)

            await message.reply_photo(
                photo=rand_img(),
                caption=(
                    "🎉 **THANKS FOR ADDING BLAZE MUSIC** 🎉\n\n"
                    "👉 Use `/play song name`"
                ),
            )

            await add_served_chat(message.chat.id)
