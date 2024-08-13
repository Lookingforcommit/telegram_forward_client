# (c) @AbirHasan2005
# (c) @Lookingforcommit
# (c) @synthimental

import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums.chat_type import ChatType
from pyrogram.errors import FloodWait

from configs import CONFIGS
from helpers.forwarder import forward_message
from helpers.handlers import HANDLERS_DICT
import helpers.scenarios_execution as scenarios_execution

user = Client(
    name='pyrogram',
    api_hash=CONFIGS.api_hash,
    api_id=CONFIGS.api_id,
    in_memory=True,
    session_string=CONFIGS.session_string
)


async def process_bot_command(client: Client, message: Message):
    command = message.text.split(" ", maxsplit=1)[0]
    if command in HANDLERS_DICT.keys():
        await HANDLERS_DICT[command](client, message, CONFIGS)
    elif CONFIGS.scenario_input_mode:
        CONFIGS.current_scenario += message.text + "\n"


async def process_forwarding_message(client: Client, message: Message):
    if message.chat.id in CONFIGS.links:
        for target_id, link_number in CONFIGS.links[message.chat.id]:
            try:
                # Apply scenarios before forwarding
                modified_message = await scenarios_execution.execute_scenarios(client, message, link_number,
                                                                               CONFIGS)
                if modified_message is not None:
                    await forward_message(client, modified_message, CONFIGS.forward_as_copy,
                                          {target_id})
            except FloodWait as e:
                print(f"FloodWait: {e.value} seconds")
                await asyncio.sleep(e.value)
            except Exception as e:
                print(f"Error forwarding message: {str(e)}")
                await client.send_message(chat_id="me",
                                          text=f"#ERROR: `{str(e)}`\n\nUnable to forward message to `{target_id}`")


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
        await process_bot_command(client, message)
    elif message.chat is not None and message.chat.id in CONFIGS.forward_from_chat_ids and CONFIGS.is_running:
        await process_forwarding_message(client, message)


if __name__ == "__main__":
    CONFIGS.is_running = True
    user.run()
