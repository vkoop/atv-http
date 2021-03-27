import asyncio
import sys

import pyatv
from aiohttp import web

atv = None


async def get_device(loop):
    global atv
    if atv is not None:
        return atv

    atvs = await pyatv.scan(loop, timeout=5)

    if not atvs:
        print('No device found', file=sys.stderr)

    print('Connecting to {0}'.format(atvs[0].address))

    atv = await pyatv.connect(atvs[0], loop)
    return atv


async def handle(request):
    command = request.match_info.get('command', "play")
    loop = asyncio.get_event_loop()
    await get_device(loop)
    global atv

    try:
        if command == "play":
            print("play")
            await atv.remote_control.play()
        elif command == "pause":
            print("pause")
            await atv.remote_control.pause()
    finally:
        # Do not forget to close
        atv.close()

    return web.Response(text="ok")


LOOP = asyncio.get_event_loop()
app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/{command}', handle)])

if __name__ == '__main__':
    web.run_app(app)
