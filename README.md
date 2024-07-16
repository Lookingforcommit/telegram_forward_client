# Forward-Client
This is Telegram Messages Forwarder bot.

Use this at your own risk. I will not be responsible for any kind of issue while using this! Better use a different Telegram Account instead of using Main Telegram Account.

### Features:
- Forward From Chat To Chat.
    - Can Forward from Multiple Chats to Multiple Chats :)
    - Automatically forward new messages From Chat To Chat.
- Userbot
- Simple & User-friendly

### Configs:
- `API_ID` - Get from my.telegram.org
- `API_HASH` - Get from my.telegram.org
- `STRING_SESSION` - Get this from [@StringSessionGen_Bot](https://t.me/StringSessionGen_Bot)
- `FORWARD_FILTERS` - Filters can be `text`, `video`, `document`, `gif`, `sticker`, `photo`, `audio`, `poll`, `forwarded`. Separate with Space.
- `FORWARD_TO_CHAT_ID` - Forward To Chat IDs. Separate with Space.
- `FORWARD_FROM_CHAT_ID` - Forward From Chat IDs. Separate with Space.
- `FORWARD_AS_COPY` - Forward Messages as Copy or with Forward Tag. Value should be `True`/`False`.
- `BLOCKED_EXTENSIONS` - Don't Forward those Media Messages which contains Blocked Extensions. Example: `mp4 mkv mp3 zip rar`. Separate with Space.
- `MINIMUM_FILE_SIZE` - Minimum File Size for Media Message to be able to Forward. Should be in Bytes.
- `BLOCK_FILES_WITHOUT_EXTENSIONS` - Value can be `True`/`False`. If `True` those files which doesn't have file extension will not be Forwarded.

### **Commands:**
- `!start` - Check Bot Alive or Not.
- `!help` - Get this Message.
- `!stop` - Stop Kanger & Restart Service.
