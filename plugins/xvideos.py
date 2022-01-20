""" xvideos, Get free Sax Videos """

import requests
import bs4

from userge import userge, Message


@userge.on_cmd("xvdo", about={
    'header': "Get Sax from xvideos",
    'description': "Get direct DL link from xvideos",
    'usage': "{tr}xvdo (xvideo_link)"})
async def xvid(message:Message):
    editer= await message.edit("`Please Wait.....`")
    msg = message.input_or_reply_str
    if not msg:
            await editer.edit("`Enter xvideos url bish`", del_in=3)
            return
    try:
        req = requests.get(msg)
        soup = bs4.BeautifulSoup(req.content, 'html.parser')

        soups = soup.find("div",{"id":"video-player-bg"})
        link =""
        for a in soups.find_all('a', href=True):
            link = a["href"]
        await editer.edit(f"**HERE IS YOUR LINK 🌚:**\n\n`{link}`")
    except Exception:
        await editer.edit("**Something went wrong**", del_in=3)




@userge.on_cmd("xsearch", about={
        "header": "Xvideo Searcher",
        "description": "Search sax videos",
        "usage": "{tr}xsearch query"})
async def xvidsearch(message: Message):
    editer= await message.edit("`Please Wait.....`")
    msg = message.input_or_reply_str
    if not msg:
            await editer.edit("`Please Enter Valid Input`", del_in=3)
            return
    try:
        qu = msg.replace(" ","+")
        page= requests.get(f"https://www.xvideos.com/?k={qu}").content
        soup = bs4.BeautifulSoup(page, 'html.parser')
        col= soup.findAll("div",{"class":"thumb"})

        links= ""

        for i in col:
            a = i.find("a")
            link = a.get('href')

            semd = link.split("/")[2]

            links += f"<a href='https://www.xvideos.com{link}'>• {semd.upper()}</a>\n"
        await editer.edit(f"<b>Search Query:</b> <code>{msg}</code>\n\n" + links,parse_mode="HTML", disable_web_page_preview=True)


    except Exception:
         await editer.edit("**Something Went Wrong**", del_in=3)
         