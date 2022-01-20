# Ported from sukinote for Userge by @kirito6969
# Don't use my api bish, use ur own from saucenao.com

import os
import html
import asyncio
import aiohttp
import mimetypes
import tempfile
from decimal import Decimal
from urllib.parse import urlparse, urlunparse, parse_qs, quote as urlencode
from bs4 import BeautifulSoup
from pyrogram.types import Sticker
from userge import userge, Message

session = aiohttp.ClientSession()
saucenao_api = "1cd221c4dbd8784776a46a42106cbe4325264e06"


async def get_file_ext(filename):
    proc = await asyncio.create_subprocess_exec('file', '--brief', '--extension', filename, stdout=asyncio.subprocess.PIPE)
    stdout, _ = await proc.communicate()
    ext = stdout.decode().strip().split('/', maxsplit=1)[0]
    if not ext or ext == '???':
        mimetype = await get_file_mimetype(filename)
        ext = mimetypes.guess_extension(mimetype) or '.bin'
    if not ext.startswith('.'):
        ext = '.' + ext
    return ext


async def get_file_mimetype(filename):
    mimetype = mimetypes.guess_type(filename)[0]
    if not mimetype:
        proc = await asyncio.create_subprocess_exec('file', '--brief', '--mime-type', filename, stdout=asyncio.subprocess.PIPE)
        stdout, _ = await proc.communicate()
        mimetype = stdout.decode().strip()
    return mimetype or ''


async def download_file(url, filename, referer=None):
    headers = {'Referer': referer} if referer else None
    async with session.get(url, headers=headers) as resp:
        if resp.status != 200:
            return False
        with open(filename, 'wb') as file:
            while True:
                chunk = await resp.content.read(4096)
                if not chunk:
                    return True
                file.write(chunk)


@userge.on_cmd(
    "sauce",
    about={
        "header": "Reverse Search",
        "description": "Reverse searches anime art, thanks to saucenao.com",
        "usage": "{tr}sauce [caption of Photo/GIF/Video/Sticker or reply]",
    }
)
async def saucenao(message: Message):
    media = message.photo or message.animation or message.video or message.sticker or message.document
    if not media:
        reply = message.reply_to_message
        if not getattr(reply, 'empty', True):
            media = reply.photo or reply.animation or reply.video or reply.sticker or reply.document
    if not media:
        await message.edit('Photo or GIF or Video or Sticker required', del_in=3)
        return
    if isinstance(media, Sticker) and media.is_animated:
        await message.edit('No animated stickers', del_in=3)
        return
    with tempfile.TemporaryDirectory() as tempdir:
        await message.edit("`Downloading...`")
        filename = await message.client.download_media(media, file_name=os.path.join(tempdir, '0'))
        mimetype = await get_file_mimetype(filename)
        if not mimetype.startswith(
                'image/') and not mimetype.startswith('video/'):
            await message.edit('Photo or GIF or Video or Sticker required', del_in=3)
            return
        if mimetype.startswith('video/'):
            new_path = os.path.join(tempdir, '1.gif')
            proc = await asyncio.create_subprocess_exec('ffmpeg', '-an', '-sn', '-i', filename, new_path)
            await proc.communicate()
            filename = new_path
        with open(filename, 'rb') as file:
            async with session.post(f'https://saucenao.com/search.php?db=999&output_type=2&api_key={urlencode(saucenao_api)}', data={'file': file}) as resp:
                json = await resp.json()
        if json['header']['status']:
            await message.edit(f'<b>{json["header"]["status"]}:</b> {html.escape(json["header"].get("message", "No message"))}')
            return
        minimum_similarity = Decimal(json['header']['minimum_similarity'])
        caption = text = ''
        to_image = False
        to_thumbnail = None
        filename = os.path.join(tempdir, '0')
        for result in json['results']:
            if not result['data'].get('ext_urls'):
                continue
            atext = f'<b>{html.escape(result["header"]["index_name"])}'
            low_similarity = Decimal(
                result['header']['similarity']) < minimum_similarity
            if low_similarity:
                atext += ' (low similarity result)'
            atext += '</b>'
            atext += '\n<b>URL'
            if len(result['data']['ext_urls']) > 1:
                atext += 's:</b>\n'
                atext += '\n'.join(map(html.escape,
                                   result['data']['ext_urls']))
            else:
                atext += f':</b> {html.escape(result["data"]["ext_urls"][0])}'
            if not to_image:
                for url in result['data']['ext_urls']:
                    if result['header']['index_id'] in (5, 6):
                        parsed = urlparse(url)
                        qs = parse_qs(parsed.query)
                        if qs.get('illust_id'):
                            async with session.get(f'https://www.pixiv.net/touch/ajax/illust/details?illust_id={urlencode(qs["illust_id"][0])}', headers={'Accept': 'application/json'}) as resp:
                                json = await resp.json()
                            if json['body']:
                                to_break = False
                                for i in (
                                    'url_big',
                                    'url',
                                    'url_s',
                                    'url_placeholder',
                                        'url_ss'):
                                    pimg = json['body']['illust_details'].get(
                                        i)
                                    if (
                                        pimg
                                        and await download_file(
                                            pimg, filename, url
                                        )
                                        and os.path.getsize(filename)
                                        < 10000000
                                    ):
                                        to_image = to_break = True
                                        break
                                if to_break:
                                    break
                    if await download_file(url, filename):
                        with open(filename) as file:
                            soup = BeautifulSoup(file.read())
                        pimg = soup.find(lambda tag: tag.name == 'meta' and tag.attrs.get(
                            'property') == 'og:image' and tag.attrs.get('content'))
                        if pimg:
                            pimg = pimg.attrs.get('content', '').strip()
                        if pimg:
                            parsed = list(urlparse(pimg))
                            if not parsed[0]:
                                parsed[0] = 'https'
                                pimg = urlunparse(parsed)
                            if parsed[0] not in ('http', 'https'):
                                continue
                            if await download_file(pimg, filename):
                                to_image = True
                                break
                else:
                    if not to_thumbnail and not low_similarity:
                        to_thumbnail = result['header'].get('thumbnail')
            atext += '\n\n'
            length = len((await message.client.parser.parse(caption + atext, 'html'))['message'])
            if length <= 1024:
                caption += atext
            if length < 4096:
                text += atext
            elif low_similarity:
                break
        if not text:
            text = caption = 'No results found'
        try:
            if to_thumbnail and not to_image:
                await download_file(to_thumbnail, filename)
            elif not to_image:
                raise Exception()
            ext = await get_file_ext(filename)
            os.rename(filename, filename + ext)
            await message.reply_photo(filename + ext, caption=caption)
        except Exception:
            await message.edit(text)
        else:
            await message.delete()
