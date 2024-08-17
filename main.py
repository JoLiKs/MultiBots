
import asyncio
import multiprocessing
import random
import threading
import time

from firebase_admin import db
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
import firebase_admin

#Fake tokens
tokens = [
    ['', '01af7212bf387be9db432c', 28580],
    ['','938d6b43d328b74d3d34', 235331],
    ['', 'e0a2ad2ae9dfb2f4ca231f1a80', 246289],
["", '84efec8505981e7da20f94ca9', 2115942],
   ['', 'd30c3da13c8263b7fb5605a', 260694],
  ['','d199738bc7c25b59a25ea7', 275391],
    ['', 'af5622e01ed40fe1f571f', 266636],
["", 'fe8d819eed6446a9e0e', 286951],


]
# coding=utf-8


cred_obj = firebase_admin.credentials.Certificate('creds.json')
default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':'https:/*******.firebaseio.com/'
	})
text2 = """

"""

text7 = ''

apps = []

for i in tokens:
    apps.append(Client(name=i[0], api_hash=i[1], api_id=i[2]))


class Botik:
    def __init__(self, app):
        self.app = app


    async def commands2(self, e, message: Message):
        if 'testo' in message.text.lower():
            await self.app.send_message(message.chat.id, "hoho")
   
        if 'oтключить' in message.text.lower():
            await self.app.send_message(message.chat.id, 'Хорошо!')
            dialogs = self.app.get_dialogs()
            photos = [p async for p in self.app.get_chat_photos("me")]
            try: await self.app.delete_profile_photos(photos[0].file_id)
            except: pass
            # Delete the rest of the photos
            #await app.delete_profile_photos([p.file_id for p in photos[1:]])
            async for i in dialogs:
                await self.app.leave_chat(i.chat.id, True)
            dialogs = self.app.get_dialogs()
            async for i in dialogs:
                    async for his in self.app.get_chat_history(i.chat.id):
                        try:
                            await his.delete(True)
                        except Exception as e: print(e)


async def commands(e, message: Message):
    global c
    if 'c = ' in message.text:
        c = int(message.text[-1])
        return await message.edit(f'Counter set to {c}')

ref = db.reference('ids/')


def start_bot():
    rnd = ref.get('ids/')[0][0]
    print(rnd)
    ref.set([rnd+1])
    app = apps[rnd]
    print(f'bot {app.name} started')
    my_handler2 = MessageHandler(Botik(app).commands2)
    app.add_handler(my_handler2, 2)
    app.run()

if __name__  ==  '__main__':
    start = time.perf_counter()
    procs = []
    ref.set([0])
    for i in apps:
        print(f'{i.name} start process')
        p = multiprocessing.Process(target=start_bot)
        procs.append(p)
    for i in procs:
        i.start()
        time.sleep(1)
    for i in procs:
        i.join()



