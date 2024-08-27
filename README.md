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
- `preprocess_chat_id` - ID of the chat for preprocessing messages prior to scenarios execution 
- `forward_from_chat_ids` - Forward from chat_ids
- `forward_to_chat_ids` - Forward to chat_ids
- `links` - Connections from source channels to destination channels
- `link_counter` - Counter of active links
- `stages` - Connections between links and scenarios
- `stage_counter` - Counter of active stages

### **Commands:**
- `!start` - Check if the userbot is alive.
- `!help` - Get this help message.
- `!stop` - Stop the userbot.
- `!add_source [chat_id_1 chat_id_2 ...]` - Add chat IDs to forward messages from.
- `!add_target [chat_id_1 chat_id_2 ...]` - Add chat IDs to forward messages to.
- `!remove_source [chat_id_1 chat_id_2 ...]` - Remove chat IDs from the list of sources.
- `!remove_target [chat_id_1 chat_id_2 ...]` - Remove chat IDs from the list of targets.
- `!list` - List chat IDs of sources and targets.
- `!link [source_chat_id] [target_chat_id]` - Connect a source channel to a destination channel.
- `!unlink [link_number]` - Disconnect a source channel from a destination channel.
- `!list_links` - List all source to destination channel connections.
- `!set_preprocess_chat [chat_id]` - Set chat for preprocessing messages prior to scenarios execution.
- `!list_scenarios` - List all scenarios.
- `!add_stage [link_number] [scenario_name]` - Add a stage to a link.
- `!remove_stage [stage_number]` - Remove a stage.
- `!list_stages` - List all stages.
