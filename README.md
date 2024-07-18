# telegram_forward_client
This is a Telegram messages forwarder bot.

### Features:
- Forward from chat to chat.
    - Can forward from multiple chats to multiple chats
    - Automatically forward new messages from chat to chat.
- Userbot
- Simple & user-friendly

### Configs:
- `api_id` - Get from my.telegram.org
- `api_hash` - Get from my.telegram.org
- `session_string` - Bot saves your session string after first authorization, or you can enter it by yourself
- `forward_to_chat_ids` - Forward to chat_ids
- `forward_from_chat_ids` - Forward from chat_ids
- `forward_as_copy` - Forward Messages as Copy or with forward tag. Boolean value

### **Commands:**
- `!start` - Check if bot is alive or not.
- `!help` - Get this message.
- `!stop` - Stop the bot.
- `!add_forward_to_chat` - Add chat_ids to forward messages to. Separate with space.
- `!add_forward_from_chat` - Add chat_ids to forward messages from. Separate with space.
- `!remove_forward_to_chat` - Remove chat_ids to forward messages to. Separate with space.
- `!remove_forward_from_chat` - Remove chat_ids to forward messages from. Separate with space.
- `!list_forward_to_chat` - List chat_ids of the chats you are forwarding messages to. Separate with space.
- `!list_forward_from_chat` - List chat_ids of the chats you are forwarding messages from. Separate with space.
