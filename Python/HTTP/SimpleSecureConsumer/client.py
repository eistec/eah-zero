#!/usr/bin/env python3
import time
import json
import toml
import requests

config = toml.load("config.toml")
SR_ADDRESS = config['sraddress']
SR_PORT = config['srport']
SYS_NAME = config['systemName']

ca_file = "truststore.pem"
cert_file = "service_registry.pem"
key_file = "service_registry.key"

url = "https://" + SR_ADDRESS + ":" + str(SR_PORT) + "/serviceregistry"
cert = (cert_file, key_file)
r = requests.get(url + "/echo", cert=cert, verify=ca_file)
if r.status_code == 200:
  print(r.text)
else:
  print('Request failed!\n')

  
