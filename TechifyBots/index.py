from pyrogram import Client, filters
from vars import *
from Database.maindb import mdb
from pyrogram.types import Message
from pyrogram.types import *

# Replace with your own values
DATABASE_CHANNEL_ID = -1002537222219
DATABASE_CHANNEL_LOG = -1003026887447
FREE_VIDEO_DURATION = 60  # example: free up to 60 seconds

@Client.on_message(filters.chat(DATABASE_CHANNEL_ID))
async def save_message(client: Client, message: Message):
    try:
        msg_id = message.id
        media_type = "Text"
        extra_info = ""

        # Detect media type and set extra info
        if message.video:
            media_type = "Video"
            duration = message.video.duration
            is_premium = duration > FREE_VIDEO_DURATION
            extra_info = f"⏱️ {duration}s | 💎 Premium: {is_premium}"
            await mdb.save_video_id(msg_id, duration, is_premium)

        elif message.photo:
            media_type = "Photo"
            await mdb.save_post_id(msg_id, message.caption or "", media_type)

        elif message.document:
            media_type = "Document"
            await mdb.save_post_id(msg_id, message.caption or "", media_type)

        elif message.audio:
            media_type = "Audio"
            await mdb.save_post_id(msg_id, message.caption or "", media_type)

        elif message.voice:
            media_type = "Voice"
            await mdb.save_post_id(msg_id, message.caption or "", media_type)

        elif message.sticker:
            media_type = "Sticker"
            await mdb.save_post_id(msg_id, "", media_type)

        elif message.animation:
            media_type = "GIF"
            await mdb.save_post_id(msg_id, message.caption or "", media_type)

        else:
            # Pure text message
            await mdb.save_post_id(msg_id, message.text or "", media_type)

        # Log message
        log_text = (
            f"**✅ Saved**\n"
            f"🆔 ID: `{msg_id}`\n"
            f"📄 Type: {media_type}\n"
            f"{extra_info if extra_info else f'📝 Content: {message.text or message.caption or \"No text\"}'}"
        )
        await client.send_message(chat_id=DATABASE_CHANNEL_LOG, text=log_text)

    except Exception as e:
        print(f"Error: {str(e)}")


