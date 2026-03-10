import os
import logging
from logging.handlers import RotatingFileHandler

# Bot Configuration
LOG_FILE_NAME = "bot.log"
PORT = '5010'
OWNER_ID = 6891095964

MSG_EFFECT = 5046509860389126442

SHORT_URL = "arolinks.com" # shortner url 
SHORT_API = "2bd6b41b022d08c3d13cbe229497092a5c30cc7e" 
SHORT_URL_2 = os.environ.get("SHORT_URL_2", "")
SHORT_API_2 = os.environ.get("SHORT_API_2", "")
SHORT_TUT = "https://t.me/HowToDownloadSnap/2"
VERIFY_COOLDOWN = int(os.environ.get("VERIFY_COOLDOWN", "180"))
VERIFY_REDIRECT_DELAY = int(os.environ.get("VERIFY_REDIRECT_DELAY", "5"))
VERIFY_LOG_CHANNEL = int(os.environ.get("VERIFY_LOG_CHANNEL", "0"))
VERIFY_ACCESS_TIME_ENABLED = os.environ.get("VERIFY_ACCESS_TIME_ENABLED", "False").lower() == "true"
VERIFY_ACCESS_HOURS = int(os.environ.get("VERIFY_ACCESS_HOURS", "1"))
SERVICE_URL = os.environ.get("SERVICE_URL", "")

# Bot Configuration
SESSION = "GetBestKurkureBot"
TOKEN = os.environ.get("TOKEN", "")
API_ID = os.environ.get("API_ID", "")
API_HASH = os.environ.get("API_HASH", "")
WORKERS = 5

DB_URI = os.environ.get("DB_URI", "")
DB_NAME = "yato"

FSUBS = [[-1003759386278, True, 10]] # Force Subscription Channels [channel_id, request_enabled, timer_in_minutes]
# Database Channel (Primary)
DB_CHANNEL = -1003591916255   # just put channel id dont add ""
# Multiple Database Channels (can be set via bot settings)
# DB_CHANNELS = {
#     "-1002595092736": {"name": "Primary DB", "is_primary": True, "is_active": True},
#     "-1001234567890": {"name": "Secondary DB", "is_primary": False, "is_active": True}
# }
# Auto Delete Timer (seconds)
AUTO_DEL = 300
# Admin IDs
ADMINS = [6891095964]
# Bot Settings
DISABLE_BTN = True
PROTECT = True

# Messages Configuration
MESSAGES = {
    "START": "<b>›› ʜᴇʏ!!, {first} ~ <blockquote>ʟᴏᴠᴇ ᴘᴏʀɴʜᴡᴀ? ɪ ᴀᴍ ᴍᴀᴅᴇ ᴛᴏ ʜᴇʟᴘ ʏᴏᴜ ᴛᴏ ғɪɴᴅ ᴡʜᴀᴛ ʏᴏᴜ aʀᴇ ʟᴏᴏᴋɪɴɢ ꜰᴏʀ.</blockquote></b>",
    "FSUB": "<b><blockquote>›› ʜᴇʏ ×</blockquote>\n  ʏᴏᴜʀ ғɪʟᴇ ɪs ʀᴇᴀᴅʏ ‼️ ʟᴏᴏᴋs ʟɪᴋᴇ ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ sᴜʙsᴄʀɪʙᴇᴅ ᴛᴏ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs ʏᴇᴛ, sᴜʙsᴄʀɪʙᴇ ɴᴏᴡ ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ғɪʟᴇs</b>",
    "ABOUT": "<b>›› ғᴏʀ ᴍᴏʀᴇ: @TuneBots \n <blockquote expandable>›› ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ: <a href='https://t.me/Snap_Lover8'>Cʟɪᴄᴋ ʜᴇʀᴇ</a> \n›› Nᴇᴡs Rᴏᴏᴍ: <a href='https://t.me/+NbpXnldC3AI2NTU1'>Cʟɪᴄᴋ ʜᴇʀᴇ</a> \n›› sɴᴀᴘ ʟᴏᴠᴇʀ: <a href='https://t.me/+5000jEnshVVmYzg1'>Cʟɪᴄᴋ ʜᴇʀᴇ</a> \n›› Dɪsᴋᴡᴀʟᴀ: <a href='https://t.me/+GHL_Gg64eBZlMTVl'>Cʟɪᴄᴋ ʜᴇʀᴇ</a> \n›› Tᴇʀᴀʙᴏx: <a href='https://t.me/+VoZbnEAO9CxhZWE1'>Cʟɪᴄᴋ ʜᴇʀᴇ</a> \n›› ᴅᴇᴠᴇʟᴏᴘᴇʀ: @SnapLoverXBot</b></blockquote>",
    "REPLY": "<b>For More Join - @Snap_Lover8</b>",
    "SHORT_MSG": "<b>📊 ʜᴇʏ bro, \n\n‼️ ɢᴇᴛ ᴀʟʟ ꜰɪʟᴇꜱ ɪɴ ᴀ ꜱɪɴɢʟᴇ ʟɪɴᴋ ‼️\n\n ⌯ ʏᴏᴜʀ ʟɪɴᴋ ɪꜱ ʀᴇᴀᴅʏ, ᴋɪɴᴅʟʏ ᴄʟɪᴄᴋ ᴏɴ ᴏᴘᴇɴ ʟɪɴᴋ ʙᴜᴛᴛᴏɴ..</b>",
    "START_PHOTO": "https://i.ibb.co/YBtKqn2H/photo-2026-03-05-12-16-54-7613744424618557456.jpg",
    "FSUB_PHOTO": "https://i.ibb.co/mVgCc1Ck/photo-2026-03-05-12-16-43-7613744373078949904.jpg",
    "SHORT_PIC": "https://i.ibb.co/VWLXFYjG/photo-2026-03-05-12-12-09-7613743200552878096.jpg",
    "VERIFY_WARN_PHOTO": "https://i.ibb.co/JwPmt4vf/photo-2026-03-05-12-18-13-7613744759626006548.jpg",
    "VERIFY_WARN_MSG": "<b>🎉 Cᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴs Yᴏᴜ Fᴜᴄᴋᴇᴅ Uᴘ.\n\n Bʏᴘᴀss ᴅᴇᴛᴇᴄᴛᴇᴅ. Tʜɪs ɪs ʏᴏᴜʀ {attempt} ᴀᴛᴛᴇᴍᴘᴛ, ʏᴏᴜ ᴡɪʟʟ ʙᴇ ʙᴀɴ ᴏɴ ᴛʜᴇ ɴᴇxᴛ ᴀᴛᴛᴇᴍᴘᴛ.\n\n Usᴇ Yᴏᴜʀ Nᴇᴡ Lɪɴᴋ Tᴏ Gᴇᴛ Fɪʟᴇs.</b>",
    "CHANNEL_LINK_PHOTO": "https://i.ibb.co/G4K04d7y/photo-2026-03-05-12-11-41-7613743080293793808.jpg",
    "CHANNEL_LINK_MSG": "<b>📢 Channel access link ready for <i>{channel_name}</i>.\n⏳ This join-request link will expire in {expire_minutes} minutes.\n👇 Tap button below to join.</b>",
    "REFER_PHOTO": "https://i.ibb.co/Jww1k4v9/photo-2026-03-06-12-59-37-7614126517794111492.jpg",
    "REFER_MSG": "<b>🎁 Refer & Earn Program!\nInvite your friends and after successful join, both of you get 1 day premium.</b>\n\n🔗 {invite_link}",
    "DEFAULT_PROFILE_PIC": "https://i.ibb.co/SDMHjm76/photo-2026-03-06-12-48-22-7614123618691186708.jpg",
    "SHORT": "https://i.ibb.co/RGsH1m4T/photo-2026-03-05-12-10-50-7613742856955494416.jpg"
}

def LOGGER(name: str, client_name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    formatter = logging.Formatter(
        f"[%(asctime)s - %(levelname)s] - {client_name} - %(name)s - %(message)s",
        datefmt='%d-%b-%y %H:%M:%S'
    )
    file_handler = RotatingFileHandler(LOG_FILE_NAME, maxBytes=50_000_000, backupCount=10)
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
