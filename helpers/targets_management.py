from typing import Set
from pyrogram import Client
from pyrogram.types import Message

from helpers.utilities import get_chat_name
from configs import Config


async def add_source_target(client: Client, message: Message, configs: Config, ids_set: Set[int]):
    if len(message.text.split(" ", 1)) < 2:
        return await message.reply_text("🤖 No chat_id specified")
    chat_ids = message.text.split(" ")[1:]
    added_chats = []
    for chat_id in chat_ids:
        try:
            chat_id = int(chat_id)
            chat_name = await get_chat_name(client, chat_id)
            if chat_id not in ids_set:
                ids_set.add(chat_id)
                added_chats.append(f"{chat_name}")
        except ValueError:
            await message.reply_text(f"🤖 Invalid chat_id: {chat_id}")
    if added_chats:
        configs.dump()
        response = "🤖 Added successfully:\n" + "\n".join([f"{name} added successfully!" for name in added_chats])
        await message.reply_text(response)
    else:
        await message.reply_text("🤖 No new chats were added.")


async def on_add_source_command(client: Client, message: Message, configs: Config):
    await add_source_target(client, message, configs, configs.forward_from_chat_ids)


async def on_add_target_command(client: Client, message: Message, configs: Config):
    await add_source_target(client, message, configs, configs.forward_to_chat_ids)


async def remove_source_target(client: Client, message: Message, configs: Config, ids_set: Set[int]):
    if len(message.text.split(" ", 1)) < 2:
        return await message.reply_text("🤖 No chat_id specified")
    chat_ids = message.text.split(" ")[1:]
    removed_chats = []
    for chat_id in chat_ids:
        try:
            chat_id = int(chat_id)
            chat_name = await get_chat_name(client, chat_id)
            if chat_id in ids_set:
                ids_set.remove(chat_id)
                removed_chats.append(f"{chat_name}")
        except ValueError:
            await message.reply_text(f"🤖 Invalid chat_id: {chat_id}")
    if removed_chats:
        configs.dump()
        response = "🤖 Removed successfully:\n" + "\n".join([f"{name} removed successfully!" for name in removed_chats])
        await message.reply_text(response)
    else:
        await message.reply_text("🤖 No chats were removed.")


async def on_remove_source_command(client: Client, message: Message, configs: Config):
    await remove_source_target(client, message, configs, configs.forward_from_chat_ids)


async def on_remove_target_command(client: Client, message: Message, configs: Config):
    await remove_source_target(client, message, configs, configs.forward_to_chat_ids)


async def on_list_command(client: Client, message: Message, configs: Config):
    if not configs.forward_from_chat_ids and not configs.forward_to_chat_ids:
        return await message.reply_text("🤖 No chats have been added yet.")
    response = []
    if configs.forward_from_chat_ids:
        source_list = ["🤖 Source:"]
        for chat_id in configs.forward_from_chat_ids:
            chat_name = await get_chat_name(client, chat_id)
            source_list.append(f"{chat_name}(`{chat_id}`)")
        response.extend(source_list)
    if configs.forward_to_chat_ids:
        if response:
            response.append("")
        target_list = ["🤖 Target:"]
        for chat_id in configs.forward_to_chat_ids:
            chat_name = await get_chat_name(client, chat_id)
            target_list.append(f"{chat_name}(`{chat_id}`)")
        response.extend(target_list)
    await message.reply_text("\n".join(response))
