import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, ChatPreview
from pyrogram.enums.chat_type import ChatType
from pyrogram.errors import FloodWait
import pyrogram.utils as utils

from configs import Config
from helpers.forwarder import forward_message


#  Pyrogram invalid peer id bugfix
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
        text=f"Hi, **{(await client.get_me()).first_name}**!\nThis is a forwarder userbot by @Lookingforcommit",
        disable_web_page_preview=True)


async def on_stop_command(message: Message):
    if RUN["is_running"]:
        RUN["is_running"] = False
    return await message.edit("Userbot stopped!\n\nSend `!start` to start userbot again.")


async def on_help_command(message: Message):
    await message.edit(
        text=CONFIGS.HELP_TEXT,
        disable_web_page_preview=True)


async def check_chat(client: Client, chat_id: int) -> bool:
    try:
        chat = await client.get_chat(chat_id)
        if type(chat) is ChatPreview:
            return False
        return True
    except ValueError:
        return False


def get_chat_id_by_name(name: str) -> int:
    return next((chat_id for chat_id, chat_name in CONFIGS.chat_id_to_name.items() if chat_name == name), None)


async def on_add_forward_command(client: Client, message: Message):
    if len(message.text.split(" ", 1)) < 2:
        return await client.send_message(
            chat_id="me",
            text="No chat_id or name specified"
        )
    parts = message.text.split(" ")[1:]
    chat_ids = set()
    for part in parts:
        try:
            chat_id = int(part)
            chat_ids.add(chat_id)
            chat = await client.get_chat(chat_id)
            CONFIGS.chat_id_to_name[chat_id] = chat.title
        except ValueError:
            chat_id = get_chat_id_by_name(part)
            if chat_id:
                chat_ids.add(chat_id)
            else:
                await client.send_message(
                    chat_id="me",
                    text=f"Chat name `{part}` not found"
                )
    if len(chat_ids) == 0:
        return await client.send_message(
            chat_id="me",
            text="No valid chat IDs or names found"
        )
    for chat_id in chat_ids:
        if message.text.startswith("!add_target") and chat_id not in CONFIGS.forward_to_chat_ids:
            CONFIGS.forward_to_chat_ids.add(chat_id)
        elif message.text.startswith("!add_source") and chat_id not in CONFIGS.forward_from_chat_ids:
            CONFIGS.forward_from_chat_ids.add(chat_id)
        CONFIGS.dump()
    return await client.send_message(
        chat_id="me",
        text="Added successfully!"
    )


async def on_remove_forward_command(client: Client, message: Message):
    if len(message.text.split(" ", 1)) < 2:
        return await client.send_message(
            chat_id="me",
            text="No chat_id or name specified"
        )
    parts = message.text.split(" ")[1:]
    chat_ids = set()
    for part in parts:
        try:
            chat_id = int(part)
            chat_ids.add(chat_id)
        except ValueError:
            chat_id = get_chat_id_by_name(part)
            if chat_id:
                chat_ids.add(chat_id)
            else:
                await client.send_message(
                    chat_id="me",
                    text=f"Chat name `{part}` not found"
                )
    if len(chat_ids) == 0:
        return await client.send_message(
            chat_id="me",
            text="No valid chat IDs or names found"
        )
    for chat_id in chat_ids:
        if message.text.startswith("!remove_target") and chat_id in CONFIGS.forward_to_chat_ids:
            CONFIGS.forward_to_chat_ids.remove(chat_id)
        elif message.text.startswith("!remove_source") and chat_id in CONFIGS.forward_from_chat_ids:
            CONFIGS.forward_from_chat_ids.remove(chat_id)
    CONFIGS.dump()
    return await client.send_message(
        chat_id="me",
        text="Removed successfully"
    )


async def on_list_forward_command(client: Client, message: Message):
    def get_name_from_id(chat_id):
        return CONFIGS.chat_id_to_name.get(chat_id, str(chat_id))

    if message.text.startswith("!list"):
        sources = ", ".join(f"`{get_name_from_id(chat_id)}`(`{chat_id}`)" for chat_id in CONFIGS.forward_from_chat_ids)
        targets = ", ".join(f"`{get_name_from_id(chat_id)}`(`{chat_id}`)" for chat_id in CONFIGS.forward_to_chat_ids)
        response = f"**Source:**\n{sources}\n\n**Target:**\n{targets}"
        return await client.send_message(
            chat_id="me",
            text=response,
            disable_web_page_preview=True
        )


async def on_connect_from_to(client: Client, message: Message):
    parts = message.text.split(" ")
    if len(parts) < 3:
        return await client.send_message(
            chat_id="me",
            text="Usage: !link <source_channel_name> <destination_channel_name>"
        )
    source_name, dest_name = parts[1], parts[2]
    source_id = get_chat_id_by_name(source_name)
    dest_id = get_chat_id_by_name(dest_name)
    if source_id is None or dest_id is None:
        return await client.send_message(
            chat_id="me",
            text="Source or destination channel name not found"
        )
    if source_id not in CONFIGS.channel_links:
        CONFIGS.channel_links[source_id] = set()
    CONFIGS.channel_links[source_id].add(dest_id)
    CONFIGS.dump()
    return await client.send_message(
        chat_id="me",
        text=f"Connected `{source_name}` to `{dest_name}`"
    )


async def on_disconnect_from_to(client: Client, message: Message):
    parts = message.text.split(" ")
    if len(parts) < 3:
        return await client.send_message(
            chat_id="me",
            text="Usage: !unlink <source_channel_name> <destination_channel_name>"
        )
    source_name, dest_name = parts[1], parts[2]
    source_id = get_chat_id_by_name(source_name)
    dest_id = get_chat_id_by_name(dest_name)
    if source_id is None or dest_id is None:
        return await client.send_message(
            chat_id="me",
            text="Source or destination channel name not found"
        )
    if source_id in CONFIGS.channel_links and dest_id in CONFIGS.channel_links[source_id]:
        CONFIGS.channel_links[source_id].remove(dest_id)
        if len(CONFIGS.channel_links[source_id]) == 0:
            del CONFIGS.channel_links[source_id]
        CONFIGS.dump()
        return await client.send_message(
            chat_id="me",
            text=f"Disconnected `{source_name}` from `{dest_name}`"
        )
    else:
        return await client.send_message(
            chat_id="me",
            text=f"No connection found between `{source_name}` and `{dest_name}`"
        )


async def on_list_connections(client: Client, message: Message):
    connection_list = []
    for source_id, dest_ids in CONFIGS.channel_links.items():
        source_name = CONFIGS.chat_id_to_name.get(source_id, str(source_id))
        for dest_id in dest_ids:
            dest_name = CONFIGS.chat_id_to_name.get(dest_id, str(dest_id))
            connection_list.append(f"`{source_name}` -> `{dest_name}`")
    if connection_list:
        connections_text = "\n".join(connection_list)
    else:
        connections_text = "No connections found."
    return await client.send_message(
        chat_id="me",
        text=f"List of connections:\n{connections_text}",
        disable_web_page_preview=True
    )


@user.on_message(filters.command("start", prefixes="!"), group=0)
async def start(client: Client, message: Message):
    await on_start_command(client, message)


@user.on_message(filters.command("stop", prefixes="!"), group=0)
async def stop(client: Client, message: Message):
    await on_stop_command(message)


@user.on_message(filters.command("help", prefixes="!"), group=0)
async def help(client: Client, message: Message):
    await on_help_command(message)


@user.on_message(filters.command("add_target", prefixes="!"), group=0)
async def add_target(client: Client, message: Message):
    await on_add_forward_command(client, message)


@user.on_message(filters.command("add_source", prefixes="!"), group=0)
async def add_source(client: Client, message: Message):
    await on_add_forward_command(client, message)


@user.on_message(filters.command("remove_target", prefixes="!"), group=0)
async def remove_target(client: Client, message: Message):
    await on_remove_forward_command(client, message)


@user.on_message(filters.command("remove_source", prefixes="!"), group=0)
async def remove_source(client: Client, message: Message):
    await on_remove_forward_command(client, message)


@user.on_message(filters.command("list", prefixes="!"), group=0)
async def list_chats(client: Client, message: Message):
    await on_list_forward_command(client, message)


@user.on_message(filters.command("link", prefixes="!"), group=0)
async def link(client: Client, message: Message):
    await on_connect_from_to(client, message)


@user.on_message(filters.command("unlink", prefixes="!"), group=0)
async def unlink(client: Client, message: Message):
    await on_disconnect_from_to(client, message)


@user.on_message(filters.command("list_links", prefixes="!"), group=0)
async def list_links(client: Client, message: Message):
    await on_list_connections(client, message)


# Handle messages from source chats
@user.on_message(filters.chat(list(CONFIGS.forward_from_chat_ids)), group=0)
async def forward_from_chat(client: Client, message: Message):
    if not RUN["is_running"]:
        return

    # Get the message details and forward to the target chats
    await forward_message(client, message)


if __name__ == "__main__":
    user.run()
