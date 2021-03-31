import asyncio
import sys
import os

import pyatv
from aiohttp import web
from pyatv.interface import AppleTV

atv = None  # type: AppleTV


async def get_device(loop):
    global atv
    if atv is not None:
        return atv

    if "ATV_IP" in os.environ:
        atv_ip = (os.environ['ATV_IP'])
        print("Using configured IP: " + atv_ip)
        atvs = await pyatv.scan(loop, timeout=5, hosts=[atv_ip])
    else:
        print("Start scan")
        atvs = await pyatv.scan(loop, timeout=5)

    if not atvs:
        print('No device found', file=sys.stderr)
        return

    print('Connecting to {0}'.format(atvs[0].address))
    print(atvs[0])

    atv = await pyatv.connect(atvs[0], loop)
    return atv


async def handle(request):
    command = request.match_info.get('command', "play")
    loop = asyncio.get_event_loop()
    await get_device(loop)
    global atv

    if atv is None:
        print("No device to handle the request")
        return web.Response(text="nok", status=500)

    response = web.Response(text="ok")

    try:
        if command == "play":
            print("play")
            await atv.remote_control.play()
        elif command == "pause":
            print("pause")
            await atv.remote_control.pause()
        elif command == "volume_up":
            print("volume_up")
            await atv.remote_control.volume_up()
        elif command == "volume_down":
            print("volume_down")
            await atv.remote_control.volume_down()
        elif command == "next":
            print("next")
            await atv.remote_control.next()
        elif command == "previous":
            print("previous")
            await atv.remote_control.previous()
        elif command == "home":
            print("home")
            await atv.remote_control.home()
        elif command == "turn_on":
            print("turn_on")
            await atv.power.turn_on()
        elif command == "turn_off":
            print("turn_off")
            await atv.power.turn_off()
        elif command == "playing_title":
            result_html = await atv.metadata.playing()
            response = web.Response(text=result_html.title)
    finally:
        # Do not forget to close
        atv.close()

    return response


LOOP = asyncio.get_event_loop()
app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/{command}', handle)])

if __name__ == '__main__':
    web.run_app(app, port=os.environ.get("SERVER_PORT", 8080))
