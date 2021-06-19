#!/usr/bin/env python3
import asyncio
import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import random
import http.client
import threading
import time
from random import randrange

SYSTEM_NAME = 'sys1'
PORT = 8200

wsclients = []

#
class ProducerHandler(tornado.web.RequestHandler):

  def get(self):
    #print(self.request.uri)
    if self.request.uri == "/"+SYSTEM_NAME+"/echo":
      self.write('Got it!')
    elif self.request.uri == "/"+SYSTEM_NAME+"/temperature":
      temp = 22.0 + random.randint(0,9)/10
      resp = {'temperature': temp}
      self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
      self.set_header('Content-Type', 'application/json')
      self.write(json.dumps(resp))
    else:
      self.set_status(404)

#
class WSProducerHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        print ('New connection')
        #self.write_message('Welcome!')
        wsclients.append(self)

    def on_message(self, message):
        print(message)
        #self.write_message(message)

    def on_close(self):
        wsclients.remove(self)

    def check_origin(self, origin):
        return True

    def path(self):
        return request.path

#
def make_app():
  return tornado.web.Application([
      (r"/"+SYSTEM_NAME+"/echo", ProducerHandler),
      (r"/"+SYSTEM_NAME+"/temperature", ProducerHandler),
      (r'/'+SYSTEM_NAME+'/ws/temperature', WSProducerHandler),
  ])

#
def threadfunc(wsclients):
  asyncio.set_event_loop(asyncio.new_event_loop())

  while True:
    temperature = 21.0 + randrange(10) / 10
    print("The temperature is: " + str(temperature) + "\N{DEGREE SIGN}C");

    outMsg = [{'bn': 'urn:sys:name:'+SYSTEM_NAME+':', 'bt': round(time.time(), 3), 'bver': 10, 'n': '3303/0/5700', 'v': temperature}]
    outMsg = json.dumps(outMsg)
    for wsc in wsclients:
      wsc.write_message(outMsg)
    time.sleep(0.999)

  connection.close()

if __name__ == "__main__":
  print('Starting Eclipse Arrowhead example Producer - HTTP')
  tclient = threading.Thread(target=threadfunc, args=(wsclients,))
  tclient.start()
  srv = make_app()
  srv.listen(PORT)
  tornado.ioloop.IOLoop.current().start()

# sudo python3 -m pip install tornado
# sudo pip3 install w1thermsensor
