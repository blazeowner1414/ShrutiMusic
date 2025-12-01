import time

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from py_yt import VideosSearch

import config
from ShrutiMusic import app
from ShrutiMusic.misc import _boot_
from ShrutiMusic.plugins.sudo.sudoers import sudoers_list
from ShrutiMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from ShrutiMusic.utils import bot_sys_stats
from ShrutiMusic.utils.decorators.language import LanguageStart
from ShrutiMusic.utils.formatters import get_readable_time
from ShrutiMusic.utils.inline import help_pannel_page1, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string


# ================== PRIVATE START ================== #

@app.on_message(filters.command("start") & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):

    await add_served_user(message.from_user.id)

    text = (
        "━━━━━━━━━━━━━━━━━━━\n"
        "🔥 **WELCOME TO BLAZE MUSIC** 🔥\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        "🎧 **Your Premium Telegram Music Bot**\n\n"
        "✅ High Quality Music\n"
        "✅ Lag-Free Streaming\n"
        "✅ Works in Voice Chats\n"
        "✅ 24×7 Uptime\n\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "💡 *Add me in your group & start playing music!*"
    )

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "➕ Add Me To Group",
                    url=f"https://t.me/{app.username}?startgroup=true",
                )
            ],
            [
                InlineKeyboardButton("📢 Updates", url=config.SUPPORT_GROUP),
                InlineKeyboardButton("💬 Support", url=config.SUPPORT_GROUP),
            ],
        ]
    )

    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=text,
        reply_markup=buttons,
    )

    if await is_on_off(2):
        await app.send_message(
            config.LOG_GROUP_ID,
            f"{message.from_user.mention} started the bot\nID: {message.from_user.id}",
        )


# ================== GROUP START ================== #

@app.on_message(filters.command("start") & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):

    uptime = int(time.time() - _boot_)

    text = (
        "🔥 **BLAZE MUSIC ACTIVATED** 🔥\n\n"
        f"⏱ **Uptime:** {get_readable_time(uptime)}\n\n"
        "🎶 Use `/play song name` to start music!"
    )

    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=text,
        reply_markup=InlineKeyboardMarkup(start_panel(_)),
    )
    await add_served_chat(message.chat.id)


# ================== BOT JOIN WELCOME ================== #

@app.on_message(filters.new_chat_members)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        if member.id == app.id:

            if message.chat.type != ChatType.SUPERGROUP:
                await message.reply_text("❌ Please add me in a supergroup.")
                return await app.leave_chat(message.chat.id)

            text = (
                "🎉 **THANKS FOR ADDING BLAZE MUSIC!** 🎉\n\n"
                "🎧 High Quality Group Music\n"
                "⚡ Fast & Smooth Streaming\n\n"
                "👉 Type `/play song name` to begin!"
            )

            await message.reply_photo(
                photo=config.START_IMG_URL,
                caption=text,
                reply_markup=InlineKeyboardMarkup(start_panel(get_string(await get_lang(message.chat.id)))),
            )

            await add_served_chat(message.chat.id)
