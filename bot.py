import os
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web

# --- কনফিগারেশন ---
API_ID = 21782294 # আপনার নিজের API ID (my.telegram.org থেকে নিন)
API_HASH = "815668e1a1829e06e30761e604f6479b" # আপনার API HASH
BOT_TOKEN = "8471148381:AAF51NFj4Nrw34umdQTpMDZbojKyD0tIdgQ"
ADMIN_ID = 6856009995
# রেলওয়ে বা ভিপিএস এর লিঙ্ক (যেমন: https://your-app.railway.app)
SERVER_URL = "YOUR_SERVER_URL_HERE" 

logging.basicConfig(level=logging.INFO)

app = Client("mizan_stream_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ১. এক্সেস কন্ট্রোল (শুধুমাত্র এডমিন)
@app.on_message(filters.private & ~filters.user(ADMIN_ID))
async def restricted(client, message):
    await message.reply_text("❌ আপনি এই বটের এডমিন নন! আপনার এক্সেস নেই।")

# ২. স্টার্ট কমান্ড (বাটনসহ)
@app.on_message(filters.command("start") & filters.user(ADMIN_ID))
async def start(client, message):
    text = "👋 স্বাগতম মিজানুর রহমান!\n\nএই বটটি দিয়ে আপনি আনলিমিটেড সাইজের ভিডিওর .mp4 লিঙ্ক তৈরি করতে পারবেন।"
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Generate MP4 Link 🎥", callback_data="gen_link")]
    ])
    await message.reply_text(text, reply_markup=reply_markup)

# ৩. বাটন ক্লিক হ্যান্ডলার
@app.on_callback_query(filters.regex("gen_link"))
async def cb_handler(client, cb):
    await cb.message.reply_text("📥 যেকোনো চ্যানেল থেকে ভিডিওটি এখানে **Forward** করুন।")
    await cb.answer()

# ৪. ভিডিও রিসিভ এবং লিঙ্ক জেনারেট
@app.on_message((filters.video | filters.document) & filters.user(ADMIN_ID))
async def file_handler(client, message):
    file = message.video or message.document
    if "video" not in file.mime_type and message.document:
        return await message.reply_text("নিশ্চিত করুন এটি একটি ভিডিও ফাইল।")
    
    file_id = file.file_id
    # স্ট্রিমিং লিঙ্ক (এটি আপনার সার্ভারের পোর্টে হিট করবে)
    download_url = f"{SERVER_URL}/watch/{file_id}"
    
    await message.reply_text(
        f"✅ **লিঙ্ক তৈরি হয়েছে!**\n\n🔗 URL: `{download_url}`",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Open Video 🌐", url=download_url)]
        ])
    )

# ৫. ব্রডকাস্ট কমান্ড (ভবিষ্যতের জন্য)
@app.on_message(filters.command("broadcast") & filters.user(ADMIN_ID))
async def broadcast(client, message):
    if not message.reply_to_message:
        return await message.reply_text("কোনো মেসেজ রিপ্লাই দিয়ে /broadcast লিখুন।")
    await message.reply_text("ব্রডকাস্ট শুরু হচ্ছে... (লজিক অ্যাড করুন)")

if __name__ == "__main__":
    # নোট: প্রফেশনাল স্ট্রিমিংয়ের জন্য 'tg-file-stream' এর মতো লাইব্রেরি ব্যবহার করা হয়
    # যা বড় ফাইলকে ছোট ছোট চাঙ্কে ভাগ করে পাঠায়।
    print("Bot is starting...")
    app.run()
