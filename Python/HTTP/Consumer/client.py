#!/usr/bin/env python3
import time
import json
import tornado.web
import tornado.websocket
import tornado.ioloop
import requests
#from colorama import Fore, Back, Style

SYSTEM_NAME = 'consumersys42'
PORT = 18101

sr_address = '192.168.11.17'
sr_address = 'localhost'
sr_port = 8443

targetURI = None #'ws://192.168.11.27:8200/sys1/ws/temperature'

class ProducerHandler(tornado.web.RequestHandler):

  def get(self):
    #print(self.request.uri)
    if self.request.uri == "/"+SYSTEM_NAME+"/echo":
      self.write('Got it!')

def on_message(message):
    print(message)

async def main():
    conn = await tornado.websocket.websocket_connect(targetURI, on_message_callback=on_message)
    while True:
        #conn.write_message('[]')
        await tornado.gen.sleep(0.5)


def registerServices():
  print('Starting to register the "echo" service at the Service registry')
  
  regReq = {
    'serviceDefinition': 'echo',
    'providerSystem': {
      'systemName': SYSTEM_NAME,
      'address': '192.168.11.17',
      'port': PORT,
      'authenticationInfo': ''
    },
    'serviceUri': '/' + SYSTEM_NAME +'/echo',
    'secure': 'NOT_SECURE',
    'version': 1,
    'interfaces': ['HTTP-INSECURE-JSON']
  }
  #print(json.dumps(regReq))
  headers = {'Accept': 'application/json', 'Content-type': 'application/json'}
  response = requests.post('http://' + sr_address + ':' + str(sr_port) + '/serviceregistry/register', headers=headers, json=regReq)
  print(response)

  return 0

def unRegisterServices():
  print('Starting to unregister the "echo" service from the Service registry')

def getOrchestrationRule(systemId, targetService):
  print('Starting Orchestration process...')

  return 'ws://192.168.11.27:8200/sys1/ws/temperature'

def make_app():
  return tornado.web.Application([
      (r"/"+SYSTEM_NAME+"/echo", ProducerHandler)
  ])


if __name__ == "__main__":
  myId = registerServices()
  targetURI = getOrchestrationRule(myId, '_temperature._ws.tcp')
  srv = make_app()
  srv.listen(PORT)
  ioloop = tornado.ioloop.IOLoop.current()
  print('Connecting to Producer at "' + targetURI + '"')
  ioloop.run_sync(main)

# pip install colorama
