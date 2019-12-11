
import asyncio
import websockets
import datetime
import pickle

from models.ws_message import WsMessage

uri = "ws://localhost:8888"

class User:
    id = ''
    permissions = 0

    def __init__(self, id, permissions):
        self.id = id
        self.permissions = permissions
        self.status = 1;

class ClientWs:
    user = {}
    ws = {}

    def __init__(self, user):
        self.user = user
        asyncio.get_event_loop().run_until_complete(self.run())


    async def run(self):
        async with websockets.connect(uri) as websocket:
            now = datetime.datetime.now()
            name = input("What's your name? ")
            msg = WsMessage('login','message text', name, now)
            print (msg)

            await websocket.send(pickle.dumps(msg))

            result = await websocket.recv()

            if(result == 'sucess'):
                print('WS: sucessfully logged in')
                self.ws = websocket
                self.user = User(name, 0)
                while (True):
                    try:
                        msg = await self.ws.recv()
                        msg = pickle.loads(msg)
                        print(f'WS: recieved: {msg}')
                    except websockets.ConnectionClosed:
                        print('WS: connection has been closed')
                        await self.ws._close()
                        return

