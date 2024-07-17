# (c) @AbirHasan2005
# (c) @Lookingforcommit

import asyncio
import json
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from pyrogram.errors import FloodWait
import pyrogram.utils as utils

from configs import Config
from helpers.forwarder import ForwardMessage


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
RUN = {"isRunning": True}
CONFIGS = Config()
user = Client(
    name='pyrogram',
    api_hash=CONFIGS.api_hash,
    api_id=CONFIGS.api_id,
    in_memory=True,
    session_string=CONFIGS.session_string
)


@user.on_raw_update(group=1)
async def get_session_string(client: Client, message: Message, users, chats):
    if CONFIGS.session_string == "":
        CONFIGS.session_string = await client.export_session_string()
        configs_json = json.dumps(vars(CONFIGS), indent=2)
        with open("configs.json", "w") as f:
            f.write(configs_json)


@user.on_message(filters.all, group=0)
async def main(client: Client, message: Message):
    if CONFIGS.forward_to_chat_ids is None or CONFIGS.forward_from_chat_ids is None:
        try:
            await client.send_message(
                chat_id="me",
                text=f"#VARS_MISSING: Please Set `FORWARD_FROM_CHAT_ID` or `FORWARD_TO_CHAT_ID` CONFIGS!"
            )
        except FloodWait as e:
            await asyncio.sleep(e.value)
        return
    if (message.text == "!start") and message.from_user.is_self:
        if not RUN["isRunning"]:
            RUN["isRunning"] = True
        await message.edit(
            text=f"Hi, **{(await client.get_me()).first_name}**!\nThis is a Forwarder Userbot by @AbirHasan2005",
            disable_web_page_preview=True)
    elif (message.text == "!stop") and message.from_user.is_self:
        RUN["isRunning"] = False
        return await message.edit("Userbot Stopped!\n\nSend `!start` to start userbot again.")
    elif (message.text == "!help") and message.from_user.is_self and RUN["isRunning"]:
        await message.edit(
            text=CONFIGS.HELP_TEXT,
            disable_web_page_preview=True)
    elif message.text and (message.text.startswith("!add_forward_")) and message.from_user.is_self and RUN["isRunning"]:
        if len(message.text.split(" ", 1)) < 2:
            return await message.edit(f"{message.text} chat_id")
        for x in message.text.split(" ", 1)[-1].split(" "):
            if x.isdigit() and message.text.startswith("!add_forward_to_chat"):
                CONFIGS.forward_to_chat_ids.append(int(x))
            elif x.isdigit() and message.text.startswith("!add_forward_from_chat"):
                CONFIGS.forward_from_chat_ids.append(int(x))
            elif x.lower().startswith("all_joined_"):
                chat_ids = []
                if x.lower() == "all_joined_groups":
                    await message.edit("Listing all joined groups ...")
                    async for dialog in client.get_dialogs():
                        chat = dialog.chat
                        if chat and (chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]):
                            chat_ids.append(chat.id)
                if x.lower() == "all_joined_channels":
                    await message.edit("Listing all joined channels ...")
                    async for dialog in client.get_dialogs():
                        chat = dialog.chat
                        if chat and (chat.type == enums.ChatType.CHANNEL):
                            chat_ids.append(chat.id)
                if not chat_ids:
                    return await message.edit("No Chats Found !!")
                for chat_id in chat_ids:
                    if chat_id not in CONFIGS.forward_to_chat_ids:
                        CONFIGS.forward_to_chat_ids.append(chat_id)
            else:
                pass
        return await message.edit("Added Successfully!")
    elif message.text and (message.text.startswith("!remove_forward_")) and message.from_user.is_self and RUN[
        "isRunning"]:
        if len(message.text.split(" ", 1)) < 2:
            return await message.edit(f"{message.text} chat_id")
        for x in message.text.split(" ", 1)[-1].split(" "):
            try:
                if x.isdigit() and message.text.startswith("!remove_forward_to_chat"):
                    CONFIGS.forward_to_chat_ids.remove(int(x))
                elif x.isdigit() and message.text.startswith("!remove_forward_from_chat"):
                    CONFIGS.forward_from_chat_ids.remove(int(x))
                else:
                    pass
            except ValueError:
                pass
        return await message.edit("Removed Successfully!")
    elif message.chat.id in CONFIGS.forward_from_chat_ids and RUN["isRunning"]:
        try_forward = await ForwardMessage(client, message, CONFIGS.forward_as_copy, CONFIGS.forward_to_chat_ids,
                                           CONFIGS.forward_filters)
        if try_forward == 400:
            return


if __name__ == "__main__":
    user.run()
