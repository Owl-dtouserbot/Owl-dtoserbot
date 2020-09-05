

from pyrogram import Client

# Copyright (c) @NaytSeyd, @frknkrc44 | 2020
print("""Xahis edirik my.telegram.org linkine gedin
Telegram hesabınızdan istifade ederek giriş edin
API Development Tools hissesine toxunun
Lazımlı melumatları yazın""")
API_KEY = int(input('API ID: '))
API_HASH = input('API HASH: ')

app = Client(
    'dtouserbot',
    api_id=API_KEY,
    api_hash=API_HASH,
    app_version="dto UserBot",
    device_model="Der Untergang",
    system_version="1.0",
    lang_code="az",
)

with app:
    print(app.export_session_string())
