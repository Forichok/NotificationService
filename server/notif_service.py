import asyncio
import logging
import websockets, pickle
import datetime
import random

from models.ws_message import WsMessage

class User:
    id = {}
    group = 0

    def __init__(self, id, group):
        self.id = id
        self.group = group

class UserWs:
    ws = {}
    user = {}

    def __init__(self, ws, id, group):
        self.ws = ws
        self.user = User(id, group)

class NotifService:
    def __init__(self, url, port):
        self.url = url
        self.port = port

        logging.basicConfig()

        self.USERS = {}


    async def notify_users(self, message):
        await asyncio.wait([user.ws.send(pickle.dumps(message)) for user in self.USERS.values()])


    async def register(self, user_ws):
        self.USERS[user_ws.user.id] = user_ws
        await user_ws.ws.send('sucess')
        msg = WsMessage('info', f'{user_ws.user.id} went online!', user_ws.user.id, datetime.datetime.utcnow().isoformat() + "Z")
        print(msg)
        await self.notify_users(msg)


    async def unregister(self, user_ws):
        del self.USERS[user_ws.user.id]
        print(f'{user_ws.user.id} went ofline')
        await self.notify_users()


    async def handler(self, ws, path):

        user_ws = {}
        try:
            async for message in ws:
                print(f"dat is a message {message}")
                msg = pickle.loads(message)
                if(msg.type == "login"):
                    user_ws = UserWs(ws, msg.sender, 0)
                    await self.register(user_ws)

                print(msg)
                while not ws.closed:
                    now = datetime.datetime.utcnow().isoformat()
                    await ws.send(pickle.dumps(now))
                    await asyncio.sleep(random.random() * 3 + 5)
        except websockets.ConnectionClosed:
            await self.unregister(user_ws)

    def run(self):
        start_server = websockets.serve(self.handler, "localhost", 8888)

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
