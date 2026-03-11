import requests
import random
import string
from config import SHORT_URL, SHORT_API, SHORT_URL_2, SHORT_API_2, MESSAGES
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
from pyrogram.errors.pyromod import ListenerTimeout
from helper.helper_func import force_sub

# ✅ In-memory cache
shortened_urls_cache = {}

def generate_random_alphanumeric():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(8))


def pick_shortener(client):
    primary = (getattr(client, 'short_url', SHORT_URL), getattr(client, 'short_api', SHORT_API))
    secondary = (getattr(client, 'short_url_2', SHORT_URL_2), getattr(client, 'short_api_2', SHORT_API_2))
    providers = [primary]
    if secondary[0] and secondary[1]:
        providers.append(secondary)
    return random.choice(providers)


def get_short(url, client):

    # Check if shortner is enabled
    shortner_enabled = getattr(client, 'shortner_enabled', True)
    if not shortner_enabled:
        return url  # Return original URL if shortner is disabled

    short_url, short_api = pick_shortener(client)
    cache_key = f"{short_url}|{url}"

    if cache_key in shortened_urls_cache:
        return shortened_urls_cache[cache_key]

    try:
        alias = generate_random_alphanumeric()
        api_url = f"https://{short_url}/api?api={short_api}&url={url}&alias={alias}"
        response = requests.get(api_url, timeout=10)
        rjson = response.json()

        if rjson.get("status") == "success" and response.status_code == 200:
            short_link = rjson.get("shortenedUrl", url)
            shortened_urls_cache[cache_key] = short_link
            return short_link
    except Exception as e:
        print(f"[Shortener Error] {e}")

    return url  # fallback

#===============================================================#

@Client.on_message(filters.command('shortner') & filters.private)
async def shortner_command(client: Client, message: Message):
    await shortner_panel(client, message)

#===============================================================#

async def shortner_panel(client, query_or_message):
    # Get current shortner settings
    short_url = getattr(client, 'short_url', SHORT_URL)
    short_api = getattr(client, 'short_api', SHORT_API)
    short_url_2 = getattr(client, 'short_url_2', SHORT_URL_2)
    tutorial_link = getattr(client, 'tutorial_link', "https://t.me/HowToDownloadSnap/2")
    shortner_enabled = getattr(client, 'shortner_enabled', True)
    verify_cooldown = int(getattr(client, 'verify_cooldown', 30))
    verify_access_time_enabled = bool(getattr(client, 'verify_access_time_enabled', False))
    verify_access_hours = int(getattr(client, 'verify_access_hours', 1))
    
    # Check if shortner is working (only if enabled)
    if shortner_enabled:
        try:
            test_response = requests.get(f"https://{short_url}/api?api={short_api}&url=https://google.com&alias=test", timeout=5)
            status = "✓ ᴡᴏʀᴋɪɴɢ" if test_response.status_code == 200 else "✗ ɴᴏᴛ ᴡᴏʀᴋɪɴɢ"
        except:
            status = "✗ ɴᴏᴛ ᴡᴏʀᴋɪɴɢ"
    else:
        status = "✗ ᴅɪsᴀʙʟᴇᴅ"
    
    enabled_text = "✓ ᴇɴᴀʙʟᴇᴅ" if shortner_enabled else "✗ ᴅɪsᴀʙʟᴇᴅ"
    toggle_text = "✗ ᴏғғ" if shortner_enabled else "✓ ᴏɴ"
    
    msg = f"""<blockquote>✦ 𝗦𝗛𝗢𝗥𝗧𝗡𝗘𝗥 𝗦𝗘𝗧𝗧𝗜𝗡𝗚𝗦</blockquote>
**<u>ᴄᴜʀʀᴇɴᴛ ꜱᴇᴛᴛɪɴɢꜱ:</u>**
<blockquote>›› **ꜱʜᴏʀᴛɴᴇʀ ꜱᴛᴀᴛᴜꜱ:** {enabled_text}
›› **ꜱʜᴏʀᴛɴᴇʀ ᴜʀʟ:** `{short_url}`
›› **ꜱʜᴏʀᴛɴᴇʀ ᴀᴘɪ:** `{short_api}`</blockquote> 
<blockquote>›› **ᴛᴜᴛᴏʀɪᴀʟ ʟɪɴᴋ:** `{tutorial_link}`
›› **ᴠᴇʀɪꜰʏ ᴛɪᴍᴇʀ (s):** `{verify_cooldown}`
›› **2ɴᴅ ꜱʜᴏʀᴛɴᴇʀ:** `{short_url_2 or 'ɴᴏᴛ sᴇᴛ'}`
›› **ᴛɪᴍᴇ ᴠᴇʀɪꜰʏ:** `{'ON' if verify_access_time_enabled else 'OFF'}`
›› **ᴀᴄᴄᴇss ᴡɪɴᴅᴏᴡ (ʜ):** `{verify_access_hours}`
›› **ᴀᴘɪ ꜱᴛᴀᴛᴜꜱ:** {status}</blockquote>

<blockquote>**≡ ᴜꜱᴇ ᴛʜᴇ ʙᴜᴛᴛᴏɴꜱ ʙᴇʟᴏᴡ ᴛᴏ ᴄᴏɴꜰɪɢᴜʀᴇ ʏᴏᴜʀ ꜱʜᴏʀᴛɴᴇʀ ꜱᴇᴛᴛɪɴɢꜱ!**</blockquote>"""
    
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(f'• {toggle_text} ꜱʜᴏʀᴛɴᴇʀ •', 'toggle_shortner'), InlineKeyboardButton('• ᴀᴅᴅ ꜱʜᴏʀᴛɴᴇʀ •', 'add_shortner')],
        [InlineKeyboardButton('• ꜱᴇᴛ ᴛᴜᴛᴏʀɪᴀʟ ʟɪɴᴋ •', 'set_tutorial_link')],
        [InlineKeyboardButton('• ꜱᴇᴛ ᴠᴇʀɪꜰʏ ᴛɪᴍᴇʀ •', 'set_verify_cooldown')],
        [InlineKeyboardButton('• ᴀᴅᴅ 2ɴᴅ ꜱʜᴏʀᴛɴᴇʀ •', 'add_second_shortner')],
        [InlineKeyboardButton('• ᴛᴏɢɢʟᴇ ᴛɪᴍᴇ ᴠᴇʀɪꜰʏ •', 'toggle_verify_access_time')],
        [InlineKeyboardButton('• ꜱᴇᴛ ᴀᴄᴄᴇss ᴡɪɴᴅᴏᴡ •', 'set_verify_access_hours')],
        [InlineKeyboardButton('• ᴛᴇꜱᴛ ꜱʜᴏʀᴛɴᴇʀ •', 'test_shortner')],
        [InlineKeyboardButton('◂ ʙᴀᴄᴋ ᴛᴏ ꜱᴇᴛᴛɪɴɢꜱ', 'settings')] if hasattr(query_or_message, 'message') else []
    ])
    
    image_url = MESSAGES.get("SHORT", "https://telegra.ph/file/8aaf4df8c138c6685dcee-05d3b183d4978ec347.jpg")
    
    if hasattr(query_or_message, 'message'):
        await query_or_message.message.edit_media(
            media=InputMediaPhoto(media=image_url, caption=msg),
            reply_markup=reply_markup
        )
    else:
        await query_or_message.reply_photo(photo=image_url, caption=msg, reply_markup=reply_markup)


#===============================================================#

@Client.on_callback_query(filters.regex("^shortner$"))
async def shortner_callback(client, query):
    if not query.from_user.id in client.admins:
        return await query.answer('❌ ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ!', show_alert=True)
    await query.answer()
    await shortner_panel(client, query)

#===============================================================#

@Client.on_callback_query(filters.regex("^toggle_shortner$"))
async def toggle_shortner(client: Client, query: CallbackQuery):
    if not query.from_user.id in client.admins:
        return await query.answer('❌ ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ!', show_alert=True)
    # Toggle the shortner status
    current_status = getattr(client, 'shortner_enabled', True)
    new_status = not current_status
    client.shortner_enabled = new_status
    
    # Save to database
    await client.mongodb.set_shortner_status(new_status)
    
    status_text = "ᴇɴᴀʙʟᴇᴅ" if new_status else "ᴅɪsᴀʙʟᴇᴅ"
    await query.answer(f"✓ ꜱʜᴏʀᴛɴᴇʀ {status_text}!")
    
    # Refresh the panel
    await shortner_panel(client, query)

#===============================================================#

@Client.on_callback_query(filters.regex("^add_shortner$"))
async def add_shortner(client: Client, query: CallbackQuery):
    if not query.from_user.id in client.admins:
        return await query.answer('❌ ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ!', show_alert=True)
    
    await query.answer()
        
    current_url = getattr(client, 'short_url', SHORT_URL)
    current_api = getattr(client, 'short_api', SHORT_API)
    
    msg = f"""<blockquote>**ꜱᴇᴛ ꜱʜᴏʀᴛɴᴇʀ ꜱᴇᴛᴛɪɴɢꜱ:**</blockquote>
**ᴄᴜʀʀᴇɴᴛ ꜱᴇᴛᴛɪɴɢꜱ:**
• **ᴜʀʟ:** `{current_url}`
• **ᴀᴘɪ:** `{current_api[:20]}...`

__<blockquote>**≡ ꜱᴇɴᴅ ɴᴇᴡ ꜱʜᴏʀᴛɴᴇʀ ᴜʀʟ ᴀɴᴅ ᴀᴘɪ ɪɴ ᴛʜɪꜱ ꜰᴏʀᴍᴀᴛ ɪɴ ᴛʜᴇ ɴᴇxᴛ 60 ꜱᴇᴄᴏɴᴅꜱ!**</blockquote>__

**ꜰᴏʀᴍᴀᴛ:** `ᴜʀʟ ᴀᴘɪ`
**ᴇxᴀᴍᴘʟᴇ:** `inshorturl.com 9435894656863495834957348`"""
    
    await query.message.edit_text(msg)
    try:
        res = await client.listen(user_id=query.from_user.id, filters=filters.text, timeout=60)
        response_text = res.text.strip()
        
        # Parse the response: url api
        parts = response_text.split()
        if len(parts) >= 2:
            new_url = parts[0].replace('https://', '').replace('http://', '').replace('/', '')
            new_api = ' '.join(parts[1:])  # Join remaining parts as API key
            
            if new_url and '.' in new_url and new_api and len(new_api) > 10:
                # Update both settings
                client.short_url = new_url
                client.short_api = new_api
                
                # Save to database
                await client.mongodb.update_shortner_setting('short_url', new_url)
                await client.mongodb.update_shortner_setting('short_api', new_api)
                
                await query.message.edit_text(f"**✓ ꜱʜᴏʀᴛɴᴇʀ ꜱᴇᴛᴛɪɴɢꜱ ᴜᴘᴅᴀᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!**\n\n**ɴᴇᴡ ᴜʀʟ:** `{new_url}`\n**ɴᴇᴡ ᴀᴘɪ:** `{new_api[:20]}...`", 
                                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'shortner')]]))
            else:
                await query.message.edit_text("**✗ ɪɴᴠᴀʟɪᴅ ꜰᴏʀᴍᴀᴛ! ᴘʟᴇᴀꜱᴇ ᴄʜᴇᴄᴋ ᴜʀʟ ᴀɴᴅ ᴀᴘɪ ᴋᴇʏ.**", 
                                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'shortner')]]))
        else:
            await query.message.edit_text("**✗ ɪɴᴠᴀʟɪᴅ ꜰᴏʀᴍᴀᴛ! ᴘʟᴇᴀꜱᴇ ᴜꜱᴇ: `ᴜʀʟ ᴀᴘɪ`**", 
                                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'shortner')]]))
    except ListenerTimeout:
        await query.message.edit_text("**⏰ ᴛɪᴍᴇᴏᴜᴛ! ᴛʀʏ ᴀɢᴀɪɴ.**", 
                                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'shortner')]]))

#===============================================================#

@Client.on_callback_query(filters.regex("^set_tutorial_link$"))
async def set_tutorial_link(client: Client, query: CallbackQuery):
    if not query.from_user.id in client.admins:
        return await query.answer('❌ ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ!', show_alert=True)
    
    await query.answer()
        
    current_tutorial = getattr(client, 'tutorial_link', "https://t.me/How_to_Download_7x/26")
    msg = f"""<blockquote>**ꜱᴇᴛ ᴛᴜᴛᴏʀɪᴀʟ ʟɪɴᴋ:**</blockquote>
**ᴄᴜʀʀᴇɴᴛ ᴛᴜᴛᴏʀɪᴀʟ:** `{current_tutorial}`

__ꜱᴇɴᴅ ᴛʜᴇ ɴᴇᴡ ᴛᴜᴛᴏʀɪᴀʟ ʟɪɴᴋ ɪɴ ᴛʜᴇ ɴᴇxᴛ 60 ꜱᴇᴄᴏɴᴅꜱ!__
**ᴇxᴀᴍᴘʟᴇ:** `https://t.me/How_to_Download_7x/26`"""
    
    await query.message.edit_text(msg)
    try:
        res = await client.listen(user_id=query.from_user.id, filters=filters.text, timeout=60)
        new_tutorial = res.text.strip()
        
        if new_tutorial and (new_tutorial.startswith('https://') or new_tutorial.startswith('http://')):
            client.tutorial_link = new_tutorial
            # Save to database
            await client.mongodb.update_shortner_setting('tutorial_link', new_tutorial)
            await query.message.edit_text(f"**✓ ᴛᴜᴛᴏʀɪᴀʟ ʟɪɴᴋ ᴜᴘᴅᴀᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!**", 
                                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'shortner')]]))
        else:
            await query.message.edit_text("**✗ ɪɴᴠᴀʟɪᴅ ʟɪɴᴋ ꜰᴏʀᴍᴀᴛ! ᴍᴜꜱᴛ ꜱᴛᴀʀᴛ ᴡɪᴛʜ https:// ᴏʀ http://**", 
                                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'shortner')]]))
    except ListenerTimeout:
        await query.message.edit_text("**⏰ ᴛɪᴍᴇᴏᴜᴛ! ᴛʀʏ ᴀɢᴀɪɴ.**", 
                                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'shortner')]]))

#===============================================================#



#===============================================================#

@Client.on_callback_query(filters.regex("^set_verify_cooldown$"))
async def set_verify_cooldown(client: Client, query: CallbackQuery):
    if not query.from_user.id in client.admins:
        return await query.answer('❌ ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ!', show_alert=True)

    await query.answer()
    current = int(getattr(client, 'verify_cooldown', 30))
    await query.message.edit_text(
        f"**Send verify cooldown in seconds (5-600).\nCurrent:** `{current}`"
    )

    try:
        res = await client.listen(user_id=query.from_user.id, filters=filters.text, timeout=60)
        value = int(res.text.strip())
        if value < 5 or value > 600:
            return await query.message.edit_text(
                "**❌ Invalid value! Use 5 to 600 seconds.**",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'shortner')]])
            )

        client.verify_cooldown = value
        await client.mongodb.update_shortner_setting('verify_cooldown', value)
        await query.message.edit_text(
            f"**✅ Verify cooldown updated to `{value}` seconds.**",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'shortner')]])
        )
    except (ValueError, ListenerTimeout):
        await query.message.edit_text(
            "**⏰ Timeout or invalid number. Try again.**",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'shortner')]])
        )



@Client.on_callback_query(filters.regex("^add_second_shortner$"))
async def add_second_shortner(client: Client, query: CallbackQuery):
    if not query.from_user.id in client.admins:
        return await query.answer('❌ ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ!', show_alert=True)

    await query.answer()
    current_url = getattr(client, 'short_url_2', SHORT_URL_2) or 'ɴᴏᴛ ꜱᴇᴛ'
    msg = f"""<blockquote>**ꜱᴇᴛ 2ɴᴅ ꜱʜᴏʀᴛɴᴇʀ:**</blockquote>
**ᴄᴜʀʀᴇɴᴛ 2ɴᴅ ᴜʀʟ:** `{current_url}`

__ꜱᴇɴᴅ: ᴜʀʟ ᴀᴘɪ ɪɴ 60 ꜱᴇᴄᴏɴᴅꜱ__
**ᴇxᴀᴍᴘʟᴇ:** `inshorturl.com api_key_here`"""
    await query.message.edit_text(msg)

    try:
        res = await client.listen(user_id=query.from_user.id, filters=filters.text, timeout=60)
        parts = res.text.strip().split()
        if len(parts) < 2:
            raise ValueError('invalid')

        new_url = parts[0].replace('https://', '').replace('http://', '').replace('/', '')
        new_api = ' '.join(parts[1:])
        if not new_url or '.' not in new_url or len(new_api) < 10:
            raise ValueError('invalid')

        client.short_url_2 = new_url
        client.short_api_2 = new_api
        await client.mongodb.update_shortner_setting('short_url_2', new_url)
        await client.mongodb.update_shortner_setting('short_api_2', new_api)
        await query.message.edit_text("**✅ 2ɴᴅ ꜱʜᴏʀᴛɴᴇʀ ᴜᴘᴅᴀᴛᴇᴅ!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'shortner')]]))
    except (ListenerTimeout, ValueError):
        await query.message.edit_text("**⏰ Timeout or invalid format.**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'shortner')]]))


@Client.on_callback_query(filters.regex("^toggle_verify_access_time$"))
async def toggle_verify_access_time(client: Client, query: CallbackQuery):
    if not query.from_user.id in client.admins:
        return await query.answer('❌ ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ!', show_alert=True)

    await query.answer()
    current = bool(getattr(client, 'verify_access_time_enabled', False))
    client.verify_access_time_enabled = not current
    await client.mongodb.update_shortner_setting('verify_access_time_enabled', client.verify_access_time_enabled)
    await query.message.edit_text(
        f"**✅ Time based verify is now {'ON' if client.verify_access_time_enabled else 'OFF'}.**",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'shortner')]])
    )


@Client.on_callback_query(filters.regex("^set_verify_access_hours$"))
async def set_verify_access_hours(client: Client, query: CallbackQuery):
    if not query.from_user.id in client.admins:
        return await query.answer('❌ ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ!', show_alert=True)

    await query.answer()
    current = int(getattr(client, 'verify_access_hours', 1))
    await query.message.edit_text(f"**Send access window hours (1-24).\nCurrent:** `{current}`")
    try:
        res = await client.listen(user_id=query.from_user.id, filters=filters.text, timeout=60)
        value = int(res.text.strip())
        if value < 1 or value > 24:
            raise ValueError('invalid')

        client.verify_access_hours = value
        await client.mongodb.update_shortner_setting('verify_access_hours', value)
        await query.message.edit_text(
            f"**✅ Verify access window updated to `{value}` hour(s).**",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'shortner')]])
        )
    except (ValueError, ListenerTimeout):
        await query.message.edit_text(
            "**⏰ Timeout or invalid number. Use 1 to 24.**",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'shortner')]])
        )

@Client.on_callback_query(filters.regex("^test_shortner$"))
async def test_shortner(client: Client, query: CallbackQuery):
    if not query.from_user.id in client.admins:
        return await query.answer('❌ ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ!', show_alert=True)
    
    await query.answer()
        
    await query.message.edit_text("**🔄 ᴛᴇꜱᴛɪɴɢ ꜱʜᴏʀᴛɴᴇʀ...**")
    
    short_url = getattr(client, 'short_url', SHORT_URL)
    short_api = getattr(client, 'short_api', SHORT_API)
    
    try:
        test_url = "https://google.com"
        alias = generate_random_alphanumeric()
        api_url = f"https://{short_url}/api?api={short_api}&url={test_url}&alias={alias}"
        
        response = requests.get(api_url, timeout=10)
        rjson = response.json()
        
        if rjson.get("status") == "success" and response.status_code == 200:
            short_link = rjson.get("shortenedUrl", "")
            msg = f"""**✅ ꜱʜᴏʀᴛɴᴇʀ ᴛᴇꜱᴛ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ!**

**ᴛᴇꜱᴛ ᴜʀʟ:** `{test_url}`
**ꜱʜᴏʀᴛ ᴜʀʟ:** `{short_link}`
**ʀᴇꜱᴘᴏɴꜱᴇ:** `{rjson.get('status', 'Unknown')}`"""
        else:
            msg = f"""**❌ ꜱʜᴏʀᴛɴᴇʀ ᴛᴇꜱᴛ ꜰᴀɪʟᴇᴅ!**

**ᴇʀʀᴏʀ:** `{rjson.get('message', 'Unknown error')}`
**ꜱᴛᴀᴛᴜꜱ ᴄᴏᴅᴇ:** `{response.status_code}`"""
            
    except Exception as e:
        msg = f"**❌ ꜱʜᴏʀᴛɴᴇʀ ᴛᴇꜱᴛ ꜰᴀɪʟᴇᴅ!**\n\n**ᴇʀʀᴏʀ:** `{str(e)}`"
    
    await query.message.edit_text(msg, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'shortner')]]))


