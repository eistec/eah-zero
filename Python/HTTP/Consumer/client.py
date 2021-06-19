#!/usr/bin/env python3
import time
import json
import tornado.websocket
import tornado.ioloop

targetURI = 'ws://192.168.11.27:8200/sys1/ws/temperature'

def on_message(message):
    print(message)

async def main():
    conn = await tornado.websocket.websocket_connect(targetURI, on_message_callback=on_message)
    while True:
        #conn.write_message('[]')
        await tornado.gen.sleep(0.5)

ioloop = tornado.ioloop.IOLoop.current()
ioloop.run_sync(main)
