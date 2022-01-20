"""Random animal pics :) made by @kirito6969"""
import re
import aiohttp
import nekos
from userge import userge, Message

animal = r"([^.]*)$"
ok_exts = ["jpg", "jpeg", "png"]


class AioHttp:
    @staticmethod
    async def get_json(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.json()


animals_data = {
    "dog": {
        "url": "https://random.dog/woof.json",
        "key": "url"},
    "cat": {
        "url": "http://aws.random.cat/meow",
        "key": "file"},
    "panda": {
        "url": "https://some-random-api.ml/img/panda",
        "key": "link"},
    "redpanda": {
        "url": "https://some-random-api.ml/img/red_panda",
        "key": "link"},
    "bird": {
        "url": "https://some-random-api.ml/img/birb",
        "key": "link"},
    "fox": {
        "url": "https://some-random-api.ml/img/fox",
        "key": "link"},
    "koala": {
        "url": "https://some-random-api.ml/img/koala",
        "key": "link"},
}

animals = list(animals_data)


async def prep_animal_image(animal_data):
    ext = ""
    image = None
    while ext not in ok_exts:
        data = await AioHttp().get_json(animal_data["url"])
        image = data[animal_data["key"]]
        ext = re.search(animal, image).group(1).lower()
    return image


@userge.on_cmd("animal", about={
    'header': "Sends desired animals pic",
    'usage': "{tr}animal [dog|cat|panda|redpanda|koala|bird|fox]"})
async def animal_image(message: Message):
    lol = message.input_str
    reply = message.reply_to_message
    reply_id = reply.message_id if reply else None
    if not lol:
        await message.edit("Bruh You hab to gib me animal name :)", del_in=4)
        return

    animal_data = animals_data[lol]
    await message.delete()
    await message.reply_photo(
        photo=await prep_animal_image(animal_data),
        reply_to_message_id=reply_id,
    )


@userge.on_cmd("afact", about={
    'header': "Sends desired animals fact",
    'usage': "{tr}afact [dog|cat|panda|redpanda|koala|bird|fox]"})
async def fact(message: Message):
    cmd = message.input_str
    if not cmd:
        await message.edit("```Not enough params provided```", del_in=3)
        return

    await message.edit(f"```Getting {cmd} fact```")
    if cmd.lower() in animals:
        link = "https://some-random-api.ml/facts/{animal}"
        fact_link = link.format(animal=cmd.lower())
        try:
            data = await AioHttp().get_json(fact_link)
            fact_text = data["fact"]
        except Exception:
            await message.edit("```The fact API could not be reached rn```", del_in=3)
        else:
            await message.reply(f"<u><i>{cmd}</u></i>\n\n`{fact_text}`")
    else:
        await message.edit("`Unsupported animal...`", del_in=3)


@userge.on_cmd("cat", about={
    'header': "Sends a cat Pic",
    'usage': "{tr}cat"})
async def _(message: Message):
    target = nekos.cat()
    reply = message.reply_to_message
    reply_id = reply.message_id if reply else None
    # await message.edit("`Hold on! Your Cat iz Coming..`")
    if reply:
        await message.reply_photo(target, reply_to_message_id=reply_id)
    else:
        await message.client.send_photo(message.chat.id, photo=target)
    await message.delete()
