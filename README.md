━━━━━━━━━━━━━━━━━━━━

```{=html}
<h2 align="center">
```
── 「 FILE STORE PRO - BY TUNEBOTS 」 ──
```{=html}
</h2>
```
```{=html}
<p align="center">
```
Telegram File Store Bot with Force Subscribe, Auto Delete, Premium
Users, URL Shortener and many advanced features.
```{=html}
</p>
```
━━━━━━━━━━━━━━━━━━━━

# 🚀 DEPLOYMENT METHODS

### ▸ Deploy on Heroku

```{=html}
<p align="center">
```
`<a href="https://dashboard.heroku.com/new?template=https://github.com/tunebots/Filestore">`{=html}
`<img src="https://img.shields.io/badge/Deploy%20On%20Heroku-black?style=for-the-badge&logo=heroku">`{=html}
`</a>`{=html}
```{=html}
</p>
```

------------------------------------------------------------------------

# ⚡ FEATURES AND DESCRIPTION

### ›› Request Force-Sub

Users must join a private channel before accessing files. Request-based
force subscription provides better control over users joining your
channel.

### ›› Custom Force-Sub

Add one or multiple force-sub channels. You can easily manage or remove
them anytime.

### ›› Multi Admin Support

Add multiple admins using their Telegram user IDs. Admins can access bot
management commands.

### ›› Ban / Unban System

Block spam users by banning them from using the bot and unban them
whenever required.

### ›› Auto Delete Files

Automatically delete files after a set timer to avoid copyright issues
and keep the bot safe.

### ›› Content Button

Attach custom buttons to every file sent by the bot (example: Join
Channel, Website, etc).

### ›› Custom Button Settings

Customize button name and link that appear under shared files.

### ›› Hide Caption & Protect Content

Hide captions from files and protect them from being forwarded.

### ›› Custom Start & Force-Sub Media

Set custom images or media for the start message and force subscribe
messages.

### ›› Editable Bot Messages

Customize start, about, reply and force-sub messages using placeholders.

### ›› URL Shortener Support

Add your own shortener API for monetized links.

------------------------------------------------------------------------

# 📜 ADMIN AND USERS COMMANDS

  Command         Description
  --------------- -------------------------------
  /start          Start the bot
  /shortner       Manage URL shortener
  /users          View total bot users
  /broadcast      Send message to all users
  /batch          Send messages in batch
  /genlink        Generate file link
  /usage          Check link usage
  /pbroadcast     Send message to premium users
  /ban            Ban a user
  /unban          Unban a user
  /addpremium     Add premium user
  /delpremium     Remove premium user
  /premiumusers   Show premium users list
  /request        Send request
  /profile        Show user profile
  /db             Database channel config
  /adddb          Add DB channel
  /removedb       Remove DB channel

------------------------------------------------------------------------

# ⚙ VARIABLES

``` python
# Bot Instance Configuration
SESSION = "your_session_name"
TOKEN = "your_bot_token"
API_ID = your_api_id
API_HASH = "your_api_hash"
WORKERS = 5

# Database Configuration
DB_URI = "your_mongodb_uri"
DB_NAME = "your_database_name"

# Force Subscription Channels
FSUBS = [[-1001234567890, True, 10]]

# Database Channel
DB_CHANNEL = -1001234567890

# Auto Delete Timer
AUTO_DEL = 300

# Admin IDs
ADMINS = [123456789, 987654321]

# Bot Settings
DISABLE_BTN = True
PROTECT = True

# Messages
MESSAGES = {
    "START": "Start message with {first}",
    "FSUB": "Force subscribe message",
    "ABOUT": "About message"
}
```

------------------------------------------------------------------------

# 🖥 VPS / LOCAL DEPLOYMENT METHOD

### Step 1

git clone https://github.com/TuneBots/filestore

### Step 2

pip3 install -U -r requirements.txt

### Step 3

Edit config.py and add your variables.

### Step 4

python3 main.py

------------------------------------------------------------------------

# 📞 SUPPORT

Channel → https://t.me/tunebots\
Bot → https://t.me/SnapLoverXBot

------------------------------------------------------------------------

# 🤝 CREDITS

• TuneBots -- Base Project\
• SnapLover

------------------------------------------------------------------------

# 📜 LICENSE

This project is licensed under GPL v3.0 License.

You are free to use, modify and host this bot, but proper credit must be
given.
