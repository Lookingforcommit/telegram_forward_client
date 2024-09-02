# (c) @AbirHasan2005
# (c) @Lookingforcommit
# (c) @synthimental

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums.chat_type import ChatType
from pyrogram.errors import FloodWait

from configs import Config
from scenarios.scenarios_configs import ScenariosConfig
from helpers.forwarder import forward_message
from helpers.handlers import HANDLERS_DICT
import helpers.scenarios_execution as scenarios_execution

CONFIGS = Config()
SCENARIOS_CONFIGS = ScenariosConfig()
user = Client(
    name='pyrogram',
    api_hash=CONFIGS.api_hash,
    api_id=CONFIGS.api_id,
    in_memory=True,
    session_string=CONFIGS.session_string
)


async def process_bot_command(client: Client, message: Message):
    if message.text is not None:
        text = message.text
    else:
        text = message.caption
    command = text.split(" ", maxsplit=1)[0]
    if command in HANDLERS_DICT.keys():
        await HANDLERS_DICT[command](client=client, message=message, configs=CONFIGS,
                                     scenarios_configs=SCENARIOS_CONFIGS)


async def process_forwarding_message(client: Client, message: Message):
    if message.chat.id in CONFIGS.links:
        for target_id, link_number in CONFIGS.links[message.chat.id]:
            try:
                # Apply scenarios before forwarding
                modified_message = await scenarios_execution.execute_scenarios(client, message, link_number, CONFIGS,
                                                                               SCENARIOS_CONFIGS)
                if modified_message is not None:
                    await forward_message(client, modified_message, {target_id})
            except FloodWait as e:
                pass
            except Exception as e:
                await client.send_message(chat_id="me",
                                          text=f"#ERROR: `{e}`\n\nUnable to forward message to `{target_id}`")


def is_bot_command(message: Message) -> bool:
    chat_condition = message.chat is not None and message.chat.type == ChatType.PRIVATE
    user_condition = message.from_user is not None and message.from_user.is_self
    text_condition = message.text is not None or message.caption is not None
    return chat_condition and user_condition and text_condition


@user.on_raw_update(group=1)
async def get_session_string(client: Client, *args):
    if CONFIGS.session_string == "":
        CONFIGS.session_string = await client.export_session_string()
        CONFIGS.dump()


@user.on_message(filters.all, group=0)
async def main(client: Client, message: Message):
    if is_bot_command(message):
        await process_bot_command(client, message)
    elif message.chat is not None and message.chat.id in CONFIGS.forward_from_chat_ids and CONFIGS.is_running:
        await process_forwarding_message(client, message)


if __name__ == "__main__":
    CONFIGS.is_running = True
    user.run()
