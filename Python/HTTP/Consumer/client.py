#!/usr/bin/env python3
import time
import json
import tornado.websocket
import tornado.ioloop

ioloop = tornado.ioloop.IOLoop.current()

def on_message(message):
    print(message)

async def main():
    url = 'ws://127.0.0.1:8200/sys1/ws/temperature'
    conn = await tornado.websocket.websocket_connect(url, on_message_callback=on_message)
    while True:
        conn.write_message('test')
        await tornado.gen.sleep(1)

ioloop.run_sync(main)
