# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import requests
from userge import userge, Message

@userge.on_cmd(
    "pokemon",
    about={
        "header": "Get Details About Pokémon!",
        "usage": "{tr}pokemon (Pokemon name)",
    }
)
async def pokedex(message: Message):
    pablo = await message.edit("`Searching For Pokémon.....`")
    sgname = message.input_or_reply_str
    reply = message.reply_to_message
    reply_id = reply.message_id if reply else None
    if not sgname:
        await pablo.edit("`Please Give Me A Valid Input. You Can Check Help Menu To Know More!`")
        return
    url = f"https://starkapis.herokuapp.com/pokedex/{sgname}"
    r = requests.get(url).json()
    pokemon = r
    if pokemon.get("error") is not None:
        kk = f"""
Error:   {pokemon.get("error")}"""
        await pablo.edit(kk)
        return
    name = str(pokemon.get("name"))
    number = str(pokemon.get("number"))
    species = str(pokemon.get("species"))
    typo = pokemon.get("types")
    types = "".join(str(tu) + ",  " for tu in typo)
    lol = pokemon.get("abilities")
    lmao = lol.get("normal")
    ok = ""
    for ty in lmao:
        ok = str(ty) + ",  "

    kk = lol.get("hidden")
    hm = "".join(str(pq) + ",  " for pq in kk)
    hell = pokemon.get("eggGroups")
    uio = "".join(str(x) + ",  " for x in hell)
    height = pokemon.get("height")
    weight = pokemon.get("weight")
    yes = pokemon.get("family")
    Id = str(yes.get("id"))
    evo = str(yes.get("evolutionStage"))
    pol = yes.get("evolutionLine")
    xy = "".join(str(p) + ",  " for p in pol)
    start = pokemon.get("starter")
    start = "No" if not start else "True"
    leg = pokemon.get("legendary")

    leg = "No" if not leg else "True"
    myt = pokemon.get("mythical")
    myt = "No" if not myt else "True"
    ultra = pokemon.get("ultraBeast")

    ultra = "No" if not ultra else "True"
    megA = pokemon.get("mega")

    megA = "No" if not megA else "True"
    gEn = pokemon.get("gen")
    link = pokemon.get("sprite")
    des = pokemon.get("description")
    caption = f"<b><u>Pokemon Information Gathered Successfully</b></u>\n\n\n<b>Name:-   {name}\nNumber:-  {number}\nSpecies:- {species}\nType:- {types}\n\n<u>Abilities</u>\nNormal Abilities:- {ok}\nHidden Abilities:- {hm}\nEgg Group:-  {uio}\nHeight:- {height}\nWeight:- {weight}\n\n<u>Family</u>\nID:- {Id}\nEvolution Stage:- {evo}\nEvolution Line:- {xy}\nStarter:- {start}\nLegendary:- {leg}\nMythical:- {myt}\nUltra Beast:- {ultra}\nMega:- {megA}\nGen:-  {gEn}\n\nDescription:-  <i>{des}</i></b>"
    await message.client.send_photo(
        message.chat.id,
        photo=link,
        caption=caption,
        parse_mode="HTML",
        reply_to_message_id=reply_id
    )
    await pablo.delete()

    
@userge.on_cmd(
    "pokecard",
    about={
        "header": "Get a Pokecard!",
        "usage": "{tr}pokecard (Pokemon name)",
    }
)
async def pokecard(message: Message):
    pokename = message.input_or_reply_str
    reply = message.reply_to_message
    reply_id = reply.message_id if reply else None
    if not pokename:
        await message.edit("`Give A Pokemon name`", del_in=3)
        return
    rw = f"https://api.pokemontcg.io/v1/cards?name={pokename}"
    r = requests.get(rw)
    a = r.json()
    try:
        pic = a["cards"][0]["imageUrlHiRes"]
        await message.client.send_photo(
            message.chat.id, pic, reply_to_message_id = reply_id
        )
        await message.delete()
    except BaseException:
        await message.edit("`Be sure To give correct Name`", del_in=3)
        return
    