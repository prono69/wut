# Kanged from FridayUB for Userge by @kirito6969

import os
import re

import requests
from bs4 import BeautifulSoup
from userge import userge, Message

cxc = [
    "Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
    "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
]


@userge.on_cmd("books",
               about={
                   "header": "Gathers All The Book Download links!",
                   "usage": "Read Books",
                   "example": "{tr}books (book name)",
               },
               )
async def bookdl(message: Message):
    book = message.input_or_reply_str
    pablo = await message.edit("`Please Wait!`")
    if not book:
        await pablo.edit("`Please Give Me A Valid Input. You Can Check Help Menu To Know More!`", del_in=3)
        return
    lin = "https://b-ok.cc/s/"
    text = book
    link = lin + text
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    f = open("book.txt", "w")
    total = soup.find(class_="totalCounter")
    for nb in total.descendants:
        nbx = nb.replace("(", "").replace(")", "")
    if nbx == "0":
        await pablo.edit("No Books Found with that name.", del_in=3)
    else:
        for tr in soup.find_all("td"):
            for td in tr.find_all("h3"):
                for ts in td.find_all("a"):
                    title = ts.get_text()
                for ts in td.find_all("a",
                                      attrs={"href": re.compile("^/book/")}):
                    ref = ts.get("href")
                    link = "https://b-ok.cc" + ref

                f.write("\n" + title)
                f.write("\nBook link:- " + link + "\n\n")

        f.write("By Pepe.")
        f.close()
        caption = "By Pepe.\nJoin @LazyAF_Geng peeps"

        await message.client.send_document(
            message.chat.id,
            document=open("book.txt", "rb"),
            caption=f"**{caption}**",
        )
        os.remove("book.txt")
        await pablo.delete()
