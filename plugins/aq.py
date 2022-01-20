"""Ramdom anime quotes plugin by @kirito6969\nLong live @LazyAF_Geng"""
# Thanks @Meli_odas_Bot for telling about the api
# Thanks @PhycoNinja13b for fixing a bug :) #LazyAF_Geng

import random
import aiohttp
from userge import userge, Message

QUOTE_TEMPLATE = """
❅ <b><u>Anime:</b></u>
  ➥ `{anime}`

❅ <b><u>Character:</b></u>
  ➥ `{character}`

❅ <b><u>Quote:</u></b>
  ➥ `{quote}`""".strip("\n").format


@userge.on_cmd("aq", about={
    'header': "Get random anime quotes",
    'flags': {
              '-a': "A random quote by anime name",
              '-c': "A random quote by character name"
    },
    'usage': "{tr}aq"
             "\n{tr}aq -a Boku No Pico"
             "\n{tr}aq -c Pico"
})
async def anime_quote(message: Message):
    # Get desired endpoints
    input_text = message.filtered_input_str
    reply: Message = message.reply_to_message
    reply_id = reply.message_id if reply else None
    if input_text:
        if "-a" in message.flags:
            url = f"https://animechan.vercel.app/api/quotes/anime?title={input_text}"
        elif "-c" in message.flags:
            url = f"https://animechan.vercel.app/api/quotes/character?name={input_text}"
    else:
        url = "https://animechan.vercel.app/api/random"

    try:
        async with aiohttp.ClientSession() as requests:
            data = await (await requests.get(url)).json()

            if isinstance(data, list):
                data = random.choice(data)
            error = data.get("error")
            await message.delete()
            if error:
                return await message.err(error)
            await message.client.send_message(message.chat.id, QUOTE_TEMPLATE(**data), reply_to_message_id=reply_id)

    except Exception as e:
        await message.err(e)
