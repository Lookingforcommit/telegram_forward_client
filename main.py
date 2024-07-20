# (c) @AbirHasan2005
# (c) @Lookingforcommit
# (c) @synthimental

import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, ChatPreview
from pyrogram.enums.chat_type import ChatType
from pyrogram.errors import FloodWait
import pyrogram.utils as utils

from configs import Config
from helpers.forwarder import forward_message


def get_peer_type(peer_id: int) -> str:
    peer_id_str = str(peer_id)
    if not peer_id_str.startswith("-"):
        return "user"
    elif peer_id_str.startswith("-100"):
        return "channel"
    else:
        return "chat"


utils.get_peer_type = get_peer_type
RUN = {"is_running": True}
CONFIGS = Config()
user = Client(
    name='pyrogram',
    api_hash=CONFIGS.api_hash,
    api_id=CONFIGS.api_id,
    in_memory=True,
    session_string=CONFIGS.session_string
)


async def on_start_command(client: Client, message: Message):
    if not RUN["is_running"]:
        RUN["is_running"] = True
    await message.edit(
        text=f"🤖 Hi, **{(await client.get_me()).first_name}**!\nThis is a forwarder userbot by @Lookingforcommit",
        disable_web_page_preview=True)


async def on_stop_command(message: Message):
    if RUN["is_running"]:
        RUN["is_running"] = False
    return await message.edit("🤖 Userbot stopped!\n\nSend `!start` to start userbot again.")


async def on_help_command(message: Message):
    help_text = """
    🤖 This UserBot can forward messages from specific chats to linked chats.
    👨🏻‍💻 **Commands:**
    • `!start` - Check if the userbot is alive.
    • `!help` - Get this help message.
    • `!stop` - Stop the userbot.
    • `!add_source` - Add chat IDs to forward messages from.
    • `!add_target` - Add chat IDs to forward messages to.
    • `!remove_source` - Remove chat IDs from the list of sources.
    • `!remove_target` - Remove chat IDs from the list of targets.
    • `!list` - List chat IDs of sources and targets.
    • `!link` - Connect a source channel to a destination channel.
    • `!unlink` - Disconnect a source channel from a destination channel.
    • `!list_links` - List all source to destination channel connections.
    """
    await message.edit(text=help_text, disable_web_page_preview=True)


async def get_chat_name(client: Client, chat_id: int) -> str:
    try:
        chat = await client.get_chat(chat_id)
        return chat.title or chat.first_name or str(chat_id)
    except Exception:
        return str(chat_id)


async def on_add_command(client: Client, message: Message, is_source: bool):
    if len(message.text.split(" ", 1)) < 2:
        return await message.reply_text("🤖 No chat_id specified")

    chat_ids = message.text.split(" ")[1:]
    added_chats = []

    for chat_id in chat_ids:
        try:
            chat_id = int(chat_id)
            chat_name = await get_chat_name(client, chat_id)
            if is_source:
                if chat_id not in CONFIGS.forward_from_chat_ids:
                    CONFIGS.forward_from_chat_ids.add(chat_id)
                    added_chats.append(f"{chat_name}")
            else:
                if chat_id not in CONFIGS.forward_to_chat_ids:
                    CONFIGS.forward_to_chat_ids.add(chat_id)
                    added_chats.append(f"{chat_name}")
        except ValueError:
            await message.reply_text(f"🤖 Invalid chat_id: {chat_id}")

    if added_chats:
        CONFIGS.dump()
        response = "🤖 Added successfully:\n" + "\n".join([f"{name} added successfully!" for name in added_chats])
        await message.reply_text(response)
    else:
        await message.reply_text("🤖 No new chats were added.")


async def on_remove_command(client: Client, message: Message, is_source: bool):
    if len(message.text.split(" ", 1)) < 2:
        return await message.reply_text("🤖 No chat_id specified")

    chat_ids = message.text.split(" ")[1:]
    removed_chats = []

    for chat_id in chat_ids:
        try:
            chat_id = int(chat_id)
            chat_name = await get_chat_name(client, chat_id)
            if is_source:
                if chat_id in CONFIGS.forward_from_chat_ids:
                    CONFIGS.forward_from_chat_ids.remove(chat_id)
                    removed_chats.append(f"{chat_name}")
            else:
                if chat_id in CONFIGS.forward_to_chat_ids:
                    CONFIGS.forward_to_chat_ids.remove(chat_id)
                    removed_chats.append(f"{chat_name}")
        except ValueError:
            await message.reply_text(f"🤖 Invalid chat_id: {chat_id}")

    if removed_chats:
        CONFIGS.dump()
        response = "🤖 Removed successfully:\n" + "\n".join([f"{name} removed successfully!" for name in removed_chats])
        await message.reply_text(response)
    else:
        await message.reply_text("🤖 No chats were removed.")


async def on_list_command(client: Client, message: Message):
    if not CONFIGS.forward_from_chat_ids and not CONFIGS.forward_to_chat_ids:
        return await message.reply_text("🤖 No chats have been added yet.")

    response = []
    if CONFIGS.forward_from_chat_ids:
        source_list = ["🤖 Source:"]
        for chat_id in CONFIGS.forward_from_chat_ids:
            chat_name = await get_chat_name(client, chat_id)
            source_list.append(f"{chat_name}(`{chat_id}`)")
        response.extend(source_list)

    if CONFIGS.forward_to_chat_ids:
        if response:
            response.append("")
        target_list = ["🤖 Target:"]
        for chat_id in CONFIGS.forward_to_chat_ids:
            chat_name = await get_chat_name(client, chat_id)
            target_list.append(f"{chat_name}(`{chat_id}`)")
        response.extend(target_list)

    await message.reply_text("\n".join(response))



async def on_link_command(client: Client, message: Message):
    parts = message.text.split()
    if len(parts) != 3:
        return await message.reply_text("🤖 Usage: !link <source_id> <target_id>")

    try:
        source_id, target_id = map(int, parts[1:3])
    except ValueError:
        return await message.reply_text("🤖 Invalid chat IDs. Please use numeric IDs.")

    if source_id not in CONFIGS.forward_from_chat_ids:
        return await message.reply_text("🤖 Source ID is not in the list of source chats.")
    if target_id not in CONFIGS.forward_to_chat_ids:
        return await message.reply_text("🤖 Target ID is not in the list of target chats.")


    used_numbers = set()
    for links in CONFIGS.links.values():
        used_numbers.update(number for _, number in links)
    link_number = 1
    while link_number in used_numbers:
        link_number += 1

    if source_id not in CONFIGS.links:
        CONFIGS.links[source_id] = []
    CONFIGS.links[source_id].append((target_id, link_number))

    CONFIGS.link_counter = max(CONFIGS.link_counter, link_number)

    CONFIGS.dump()

    source_name = await get_chat_name(client, source_id)
    target_name = await get_chat_name(client, target_id)
    await message.reply_text(
        f"🤖 Linked: {source_name}(`{source_id}`) -> {target_name}(`{target_id}`) - Link #{link_number}")


async def on_unlink_command(client: Client, message: Message):
    parts = message.text.split()
    if len(parts) != 2:
        return await message.reply_text("🤖 Usage: !unlink <link_number>")

    try:
        link_number = int(parts[1])
    except ValueError:
        return await message.reply_text("🤖 Invalid link number. Please use a numeric value.")

    found = False
    for source_id, links in CONFIGS.links.items():
        for i, (target_id, number) in enumerate(links):
            if number == link_number:
                del CONFIGS.links[source_id][i]
                if not CONFIGS.links[source_id]:
                    del CONFIGS.links[source_id]

                CONFIGS.link_counter -= 1

                for s_id in CONFIGS.links:
                    CONFIGS.links[s_id] = [(t_id, n if n < link_number else n - 1) for t_id, n in CONFIGS.links[s_id]]

                CONFIGS.dump()
                source_name = await get_chat_name(client, source_id)
                target_name = await get_chat_name(client, target_id)
                await message.reply_text(
                    f"🤖 Unlinked: {source_name}(`{source_id}`) -> {target_name}(`{target_id}`) - Link #{link_number}")
                found = True
                break
        if found:
            break
    if not found:
        await message.reply_text("🤖 This link number does not exist.")


async def on_list_links_command(client: Client, message: Message):
    if not CONFIGS.links:
        return await message.reply_text("🤖 No active links.")

    links_list = ["🤖 List of links:"]
    for source_id, links in CONFIGS.links.items():
        source_name = await get_chat_name(client, source_id)
        for target_id, link_number in links:
            target_name = await get_chat_name(client, target_id)
            links_list.append(f"{source_name}(`{source_id}`) -> {target_name}(`{target_id}`) - Link #{link_number}")

    await message.reply_text("\n".join(links_list))


@user.on_message(filters.all, group=0)
async def main(client: Client, message: Message):
    bot_command = (message.chat is not None and message.chat.type == ChatType.PRIVATE and message.from_user.is_self
                   and message.text is not None)
    if bot_command:
        if message.text == "!start":
            await on_start_command(client, message)
        elif message.text == "!stop":
            await on_stop_command(message)
        elif message.text == "!help":
            await on_help_command(message)
        elif message.text.startswith("!add_source"):
            await on_add_command(client, message, is_source=True)
        elif message.text.startswith("!add_target"):
            await on_add_command(client, message, is_source=False)
        elif message.text.startswith("!remove_source"):
            await on_remove_command(client, message, is_source=True)
        elif message.text.startswith("!remove_target"):
            await on_remove_command(client, message, is_source=False)
        elif message.text == "!list":
            await on_list_command(client, message)
        elif message.text.startswith("!link"):
            await on_link_command(client, message)
        elif message.text.startswith("!unlink"):
            await on_unlink_command(client, message)
        elif message.text == "!list_links":
            await on_list_links_command(client, message)
    elif message.chat is not None and message.chat.id in CONFIGS.forward_from_chat_ids and RUN["is_running"]:
        if message.chat.id in CONFIGS.links:
            for target_id, _ in CONFIGS.links[message.chat.id]:
                while True:
                    try:
                        await forward_message(client, message, CONFIGS.forward_as_copy, {target_id})
                        break
                    except FloodWait as e:
                        await asyncio.sleep(e.value)


if __name__ == "__main__":
    user.run()
