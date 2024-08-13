from pyrogram import Client
from pyrogram.types import Message

from configs import Config


async def on_help_command(client: Client, message: Message, configs: Config) -> None:
    await message.edit(text=configs.HELP_TEXT, disable_web_page_preview=True)


async def on_start_command(client: Client, message: Message, configs: Config) -> None:
    if not configs.is_running:
        configs.is_running = True
    await message.edit(
        text=f"🤖 Hi, **{(await client.get_me()).first_name}**!\nThis is a forwarder userbot by @Lookingforcommit",
        disable_web_page_preview=True)


async def on_stop_command(client: Client, message: Message, configs: Config) -> Message:
    if configs.is_running:
        configs.is_running = False
    return await message.edit("🤖 Userbot stopped!\n\nSend `!start` to start userbot again.")
