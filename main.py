# (c) @AbirHasan2005
# (c) @Lookingforcommit

from pyrogram import Client, filters
from pyrogram.types import Message, ChatPreview
from pyrogram.enums.chat_type import ChatType
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


async def on_add_forward_command(client: Client, message: Message):
    if len(message.text.split(" ", 1)) < 2:
        return await client.send_message(
            chat_id="me",
            text="No chat_id specified"
        )
    chat_ids = set(message.text.split(" ")[1:])
    invalid_chat_ids = []
    for chat_id in chat_ids:
        valid = await check_chat(client, int(chat_id))
        if not valid:
            invalid_chat_ids.append(int(chat_id))
    if len(invalid_chat_ids) > 0:
        return await client.send_message(
            chat_id="me",
            text=f"Invalid chat_ids or you are not a member of the chats: {invalid_chat_ids}"
        )
    for chat_id in chat_ids:
        chat_id = int(chat_id)
        if message.text.startswith("!add_forward_to_chat") and chat_id not in CONFIGS.forward_to_chat_ids:
            CONFIGS.forward_to_chat_ids.add(chat_id)
        elif message.text.startswith("!add_forward_from_chat") and chat_id not in CONFIGS.forward_to_chat_ids:
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
            text="No chat_id specified"
        )
    chat_ids = set(message.text.split(" ")[1:])
    invalid_chat_ids = []
    for chat_id in chat_ids:
        try:
            chat_id = int(chat_id)
        except ValueError:
            invalid_chat_ids.append(int(chat_id))
    if len(invalid_chat_ids) > 0:
        return await client.send_message(
            chat_id="me",
            text=f"Invalid chat_ids: {invalid_chat_ids}"
        )
    for chat_id in chat_ids:
        chat_id = int(chat_id)
        if message.text.startswith("!remove_forward_to_chat") and chat_id in CONFIGS.forward_to_chat_ids:
            CONFIGS.forward_to_chat_ids.remove(chat_id)
        elif message.text.startswith("!remove_forward_from_chat") and chat_id in CONFIGS.forward_from_chat_ids:
            CONFIGS.forward_from_chat_ids.remove(chat_id)
    return await client.send_message(
        chat_id="me",
        text="Removed successfully"
    )


async def on_list_forward_command(client: Client, message: Message):
    if message.text.startswith("!list_forward_to_chat"):
        return await client.send_message(
            chat_id="me",
            text=f"List of chats you are forwarding to: {CONFIGS.forward_to_chat_ids}"
        )
    elif message.text.startswith("!list_forward_from_chat"):
        return await client.send_message(
            chat_id="me",
            text=f"List of chats you are forwarding from: {CONFIGS.forward_from_chat_ids}"
        )


@user.on_raw_update(group=1)
async def get_session_string(client: Client, message: Message, users, chats):
    if CONFIGS.session_string == "":
        CONFIGS.session_string = await client.export_session_string()
        CONFIGS.dump()


@user.on_message(filters.all, group=0)
async def main(client: Client, message: Message):
    bot_command = (message.chat is not None and message.chat.type == ChatType.PRIVATE and message.from_user.is_self
                   and message.text is not None)
    if bot_command:
        add_forward_command = (message.text.startswith("!add_forward_to_chat") or
                               message.text.startswith("!add_forward_from_chat"))
        remove_forward_command = (message.text.startswith("!remove_forward_to_chat") or
                                  message.text.startswith("!remove_forward_from_chat"))
        list_forward_command = (message.text.startswith("!list_forward_to_chat") or
                                message.text.startswith("!list_forward_from_chat"))
        if message.text == "!start":
            await on_start_command(client, message)
        elif message.text == "!stop":
            await on_stop_command(message)
        elif message.text == "!help":
            await on_help_command(message)
        elif add_forward_command:
            await on_add_forward_command(client, message)
        elif remove_forward_command:
            await on_remove_forward_command(client, message)
        elif list_forward_command:
            await on_list_forward_command(client, message)
    elif message.chat is not None and message.chat.id in CONFIGS.forward_from_chat_ids and RUN["is_running"]:
        try_forward = await ForwardMessage(client, message, CONFIGS.forward_as_copy, CONFIGS.forward_to_chat_ids,
                                           CONFIGS.forward_filters)
        if try_forward == 400:
            return


if __name__ == "__main__":
    user.run()
