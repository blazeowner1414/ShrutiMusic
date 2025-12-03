from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message

from ShrutiMusic import app
from ShrutiMusic.core.call import Nand
from ShrutiMusic.utils import bot_sys_stats
from ShrutiMusic.utils.decorators.language import language
from ShrutiMusic.utils.inline import supp_markup
from config import BANNED_USERS, PING_IMG_URL


@app.on_message(filters.command(["ping", "alive"]) & ~BANNED_USERS)
@language
async def ping_com(client, message: Message, _):

    start = datetime.now()

    response = await message.reply_photo(
        photo=PING_IMG_URL,
        caption=(
            "🏓 **Pinging Blaze Music...**\n\n"
            f"🤖 {app.mention}\n"
            "⚡ Please wait..."
        ),
    )

    pytgping = await Nand.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000

    await response.edit_caption(
        caption=(
            "🏓 **PONG!** ✅\n\n"
            f"⚡ **Response:** `{resp} ms`\n"
            f"🔊 **PyTgCalls:** `{pytgping} ms`\n\n"
            f"⏱ **Uptime:** `{UP}`\n"
            f"💾 **RAM:** `{RAM}`\n"
            f"🖥 **CPU:** `{CPU}`\n"
            f"📂 **Disk:** `{DISK}`\n\n"
            "━━━━━━━━━━━━━━\n"
            "🎧 **BLAZE MUSIC** 🎵\n"
            "🚀 *Powered by Blaze Bots*"
        ),
        reply_markup=supp_markup(_),
    )
