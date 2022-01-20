# Kanged from FridayUB for Userge by @kirito6969

import requests
from userge import userge, Message


@userge.on_cmd(
    "amsearch",
    about={
        "header": "Search Products From Amazon!",
        "usage": "{tr}amsearch Iphone",
    }
)
async def _am_search(message: Message):
    query = message.input_str
    msg_ = await message.edit("`Searching Product!`")
    if not query:
        await msg_.edit("`Please, Give Input!`")
        return
    product = ""
    r = requests.get(f"https://amznsearch.vercel.app/api/?query={query}").json()
    for products in r:
        link = products['productLink']
        name = products['productName']
        price= products['productPrice']
        product += f"<a href='{link}'>• {name}\n{price}</a>\n"
    await msg_.edit(product, parse_mode="HTML")
