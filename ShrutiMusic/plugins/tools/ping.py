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
async def ping_handler(_, message: Message, __):

    start = datetime.now()

    # STEP 1: Send photo (no delete, no edit yet)
    msg = await message.reply_photo(
        photo=PING_IMG_URL,
        caption="🏓 **Checking Blaze Music...**"
    )

    # STEP 2: Collect stats
    pytg = await Nand.ping()
    uptime, cpu, ram, disk = await bot_sys_stats()
    ms = (datetime.now() - start).microseconds / 1000

    # STEP 3: Edit caption ONCE (stable)
    await msg.edit_caption(
        caption=(
            "✅ **BLAZE MUSIC ONLINE**\n\n"
            f"⚡ **Ping:** `{ms} ms`\n"
            f"🎧 **VC Ping:** `{pytg} ms`\n\n"
            f"⏱ **Uptime:** `{uptime}`\n"
            f"🖥 **CPU:** `{cpu}`\n"
            f"💾 **RAM:** `{ram}`\n"
            f"📂 **Disk:** `{disk}`\n\n"
            "━━━━━━━━━━━━━━\n"
            "🎧 **BLAZE MUSIC** 🎵\n"
            "🚀 *Powered by Blaze Bots*"
        ),
        reply_markup=supp_markup(__)
    )
