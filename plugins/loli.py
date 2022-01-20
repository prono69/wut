# By @kirito6969 for Userge :)

import requests
import html
from userge import userge, Message
from urllib.parse import quote as urlencode
import aiohttp

session = aiohttp.ClientSession()

@userge.on_cmd(
    "loli",
    about={
        "header": "Its only for Lolicons ^_^",
        "usage": "{tr}loli\n{tr}loli -n\n{tr}loli -s",
    },
)
async def loli(message: Message):
    "FBI moment"
    word = message.filtered_input_str
    mode = None
    if "-s" in message.flags:
    	mode = 0
    elif "-n" in message.flags:
    	mode = 1
    else:
    	mode = 2
    async with session.get(
        f"https://api.lolicon.app/setu/v2?num=1&r18={mode}&keyword={urlencode(word)}"
    ) as resp:
        data = await resp.json()
    if not data["data"][0]:
        return await message.err(
            "***Unknown Error occured while fetching data***", 3
        )
    data = data["data"][0]
    pic = data["urls"]["original"]
    title = f'{data["title"]} by {data["author"]}'
    adult = f'{data["r18"]}'
    tags = None
    caption = f'<a href="https://pixiv.net/artworks/{data["pid"]}">{html.escape(data["title"])}</a> by <a href="https://pixiv.net/users/{data["uid"]}">{html.escape(data["author"])}</a>\n'
    if data["tags"]:
        tags = f'{html.escape(", ".join(data["tags"]))}'
    lol = f"<b>{caption}</b>\n<b>✘ Title:</b> <i>{title}</i>\n<b>✘ Adult:</b> <i>{adult}</i>\n<b>"
    await message.delete()
    await message.client.send_photo(
        message.chat.id, photo=pic, caption=lol, parse_mode="html",
    )
        