from pyrogram import Client
from pyrogram.types import Message

from configs import Config
from helpers.utilities import get_chat_name


async def on_link_command(client: Client, message: Message, configs: Config):
    parts = message.text.split()
    if len(parts) != 3:
        return await message.reply_text("🤖 Usage: !link <source_id> <target_id>")
    try:
        source_id, target_id = map(int, parts[1:3])
    except ValueError:
        return await message.reply_text("🤖 Invalid chat IDs. Please use numeric IDs.")
    if source_id not in configs.forward_from_chat_ids:
        return await message.reply_text("🤖 Source ID is not in the list of source chats.")
    if target_id not in configs.forward_to_chat_ids:
        return await message.reply_text("🤖 Target ID is not in the list of target chats.")
    used_numbers = set()
    for links in configs.links.values():
        used_numbers.update(number for _, number in links)
    link_number = 1
    while link_number in used_numbers:
        link_number += 1
    if source_id not in configs.links:
        configs.links[source_id] = []
    configs.links[source_id].append((target_id, link_number))
    configs.link_counter = max(configs.link_counter, link_number)
    print(configs.links)
    configs.dump()
    source_name = await get_chat_name(client, source_id)
    target_name = await get_chat_name(client, target_id)
    await message.reply_text(
        f"🤖 Linked: {source_name}(`{source_id}`) -> {target_name}(`{target_id}`) - Link #{link_number}")


async def on_unlink_command(client: Client, message: Message, configs: Config):
    parts = message.text.split()
    if len(parts) != 2:
        return await message.reply_text("🤖 Usage: !unlink <link_number>")
    try:
        link_number = int(parts[1])
    except ValueError:
        return await message.reply_text("🤖 Invalid link number. Please use a numeric value.")
    found = False
    for source_id, links in configs.links.items():
        for i, (target_id, number) in enumerate(links):
            if number == link_number:
                del configs.links[source_id][i]
                if not configs.links[source_id]:
                    del configs.links[source_id]
                configs.link_counter -= 1
                for s_id in configs.links:
                    configs.links[s_id] = [(t_id, n if n < link_number else n - 1) for t_id, n in configs.links[s_id]]
                configs.dump()
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


async def on_list_links_command(client: Client, message: Message, configs: Config):
    if not configs.links:
        return await message.reply_text("🤖 No active links.")
    links_list = ["🤖 List of links:"]
    for source_id, links in configs.links.items():
        source_name = await get_chat_name(client, source_id)
        for target_id, link_number in links:
            target_name = await get_chat_name(client, target_id)
            links_list.append(f"#{link_number} Link:\n{source_name}(`{source_id}`) -> {target_name}(`{target_id}`)")
    await message.reply_text("\n\n".join(links_list))
