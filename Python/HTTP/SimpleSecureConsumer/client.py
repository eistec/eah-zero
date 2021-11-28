#!/usr/bin/env python3
import time
import json
import toml
import requests

config = toml.load("config.toml")
SR_ADDRESS = config['sraddress']
SR_PORT = config['srport']
SYS_NAME = config['systemName']

ca_file = config['trustStore']
cert_file = config['certFile']
key_file = config['keyFile']

if False: # check ServiceRegistry
  url = "https://" + SR_ADDRESS + ":" + str(SR_PORT) + "/serviceregistry"
  cert = (cert_file, key_file)
  r = requests.get(url + "/echo", cert=cert, verify=ca_file)
  if r.status_code == 200:
    print(r.text)
  else:
    print('Request failed!\n')

# use the DataManager instead (should use ServiceRegistry or Orchestrator instead!)
else:
  url = "https://" + SR_ADDRESS + ":" + str(8461) + "/datamanager/proxy"
  cert = (cert_file, key_file)
  r = requests.get(url + "/serviceregistry.testcloud2.aitia.arrowhead.eu/test", cert=cert, verify=ca_file)
  r = requests.get(url + "/serviceregistry/test", cert=cert, verify=ca_file)
  if r.status_code == 200:
    print(r.text)
  else:
    print('Request failed! with ' + str(r.status_code)  + '\n')
    print(r.text)

