"""Give Hugs and kisses to everyone :)
Made by @kirito6969 thanks to Psyco-Ninja for optimize :)"""

import aiohttp
from userge import userge, Message

MAP_LINK = {
    "-g": "https://nekos.life/api/hug",
    "-k": "https://nekos.life/api/kiss",
    "-d": "https://api.computerfreaker.cf/v1/hug",
    "-w": "https://some-random-api.ml/animu/wink",
    "-s": "https://api.rei.my.id/v2/slap"
}


async def get_link(arg: str) -> str:
    """ retrieve link for hug """
    async with aiohttp.ClientSession() as session, \
        session.get(MAP_LINK.get(arg)) as request:
        result = await request.json()
        link = result.get("url", result.get("link", ""))
    return link


@userge.on_cmd("hug", about={
    'header': "Give a hug xD",
    'flags': {
              '-g': "For hug gif",
              '-k': "For kiss gif",
              '-w': "For wink gif",
              '-s': "For slap gif"
             },
    'usage': "{tr}hug [reply | username]"
             "\n{tr}hug -g [reply | username]"
             "\n{tr}hug -k [reply | username]"
             "\n{tr}hug -w [reply | username]"
})
async def hugs(message: Message):
    """ send a hug """
    username: str = message.filtered_input_str
    reply: Message = message.reply_to_message
    unsave: bool = not message.client.is_bot
    reply_id = reply.message_id if reply else message.message_id

    if not username and not reply:
        await message.edit(
            "**Bruh** ~`You shouldn't hug/kiss yourself ಠಗಠ`", del_in=3
        )
        return

    kwargs: dict = {
        "reply_to_message_id": reply_id,
        "unsave": unsave
    }

    if "-g" in message.flags:
        await message.client.send_animation(
            message.chat.id, await get_link("-g"), caption=f"**UwU hugged {username} !**", **kwargs
        )
    elif "-k" in message.flags:
        await message.client.send_animation(
            message.chat.id, await get_link("-k"), caption=f"**OwO kissed {username} !**", **kwargs
        )
    elif "-w" in message.flags:
        await message.client.send_animation(
            message.chat.id, await get_link("-w"), caption=f"**UwU winked at {username} !**", **kwargs
        )
    elif "-s" in message.flags:
    	await message.client.send_animation(message.chat.id, await get_link("-s"), caption=f"**Slapped {username}**", **kwargs)
    else:
        kwargs.pop("unsave")
        await message.reply_photo(await get_link("-d"), caption=f"**UwU hugged {username} !**", **kwargs)

    await message.delete()
