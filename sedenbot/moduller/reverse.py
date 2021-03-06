# Copyright (C) 2020 TeamDerUntergang.
#
# SedenUserBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SedenUserBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from os import path, remove
from re import findall, I, M
from urllib import request, parse
from requests import post, get
from PIL import Image
from bs4 import BeautifulSoup
from pyrogram import InputMediaPhoto

from sedenbot import KOMUT
from sedenecem.core import edit, reply_doc, extract_args, sedenify, download_media_wc

opener = request.build_opener()
useragent = 'Mozilla/5.0 (Linux; Android 9; SM-G960F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.70 Mobile Safari/537.36'
opener.addheaders = [('User-agent', useragent)]

@sedenify(pattern=r'^.reverse$', compat=False)
def reverse(client, message):
    photo = 'reverse.png'
    if path.isfile(photo):
        remove(photo)

    reverse = message.reply_to_message
    revfile = None
    if reverse and reverse.media:
        revfile = download_media_wc(reverse, photo)
    else:
        edit(message, '`Lütfen bir fotoğrafa veya çıkartmaya yanıt verin.`')
        return

    if photo:
        edit(message, '`İşleniyor...`')
        try:
            image = Image.open(revfile)
        except OSError:
            edit(message, '`Desteklenmeyen tür`')
            return
        image.save(photo, "PNG")
        image.close()
        # https://stackoverflow.com/questions/23270175/google-reverse-image-search-using-post-request#28792943
        searchUrl = 'https://www.google.com/searchbyimage/upload'
        multipart = {
            'encoded_image': (photo, open(photo, 'rb')),
            'image_content': ''
        }
        response = post(searchUrl,
                                 files=multipart,
                                 allow_redirects=False)
        fetchUrl = response.headers['Location']

        if response != 400:
            edit(message, "`Görüntü başarıyla Google'a yüklendi.`"
                 "\n`Şimdi kaynak ayrıştırılıyor.`")
        else:
            edit(message, '`Google siktirip gitmemi söyledi.`')
            return

        remove(photo)
        match = ParseSauce(fetchUrl +
                           '&preferences?hl=en&fg=1#languages')
        guess = match['best_guess']
        imgspage = match['similar_images']

        if guess and imgspage:
            edit(message, f'[{guess}]({fetchUrl})\n\n`Resim arıyorum...`')
        else:
            edit(message, '`Çirkin kıçın için bir şey bulamadım.`')
            return

        msg = extract_args(message)
        if len(msg) > 1 and msg.isdigit():
            lim = msg
        else:
            lim = 3
        images = scam(match, lim)
        yeet = []
        for i in range(len(images)):
            k = get(images[i])
            n = f'reverse_{i}.png'
            file = open(n, 'wb')
            file.write(k.content)
            file.close()
            yeet.append(InputMediaPhoto(n))
        reply_doc(message, yeet)
        edit(message,
             f'[{guess}]({fetchUrl})\n\n[Benzer görüntüler]({imgspage})')


def ParseSauce(googleurl):

    source = opener.open(googleurl).read()
    soup = BeautifulSoup(source, 'html.parser')

    results = {'similar_images': '', 'best_guess': ''}

    try:
        for similar_image in soup.findAll('input', {'class': 'gLFyf'}):
            url = 'https://www.google.com/search?tbm=isch&q=' + \
                parse.quote_plus(similar_image.get('value'))
            results['similar_images'] = url
    except BaseException:
        pass

    for best_guess in soup.findAll('div', attrs={'class': 'r5a77d'}):
        results['best_guess'] = best_guess.get_text()

    return results

def scam(results, lim):

    single = opener.open(results['similar_images']).read()
    decoded = single.decode('utf-8')

    imglinks = []
    counter = 0

    pattern = r'^,\[\"(.*[.png|.jpg|.jpeg])\",[0-9]+,[0-9]+\]$'
    oboi = findall(pattern, decoded, I | M)

    for imglink in oboi:
        counter += 1
        if not counter >= int(lim):
            imglinks.append(imglink)
        else:
            break

    return imglinks

KOMUT.update({
    'reverse':
    '.reverse\
    \nKullanım: Fotoğraf veya çıkartmaya yanıt vererek görüntüyü Google üzerniden arayabilirsiniz'
})
