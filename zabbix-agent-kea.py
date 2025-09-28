#!/usr/bin/env python

import requests
import json
import sys
import yaml

from requests.auth import HTTPBasicAuth

def handle_error(message, code):
  print(f'ERROR: {message}')
  if code != 0:
    sys.exit(code)

def get_config_key(d, keylist, default=None):
  keys = keylist.split(':')
  for key in keys:
    if isinstance(d, dict) and key in d:
      d = d[key]
    else:
      return default
  return d

config_file = '/usr/local/etc/zabbix-agent-kea.conf.yaml'
command_name = sys.argv[1]

with open(config_file, 'r') as fh:
  config = yaml.safe_load(fh)

host = get_config_key(config, 'kea-server:host')
if host is None:
  host = '127.0.0.1'
port = get_config_key(config, 'kea-server:port')
if port is None:
  port = '8000'
user = get_config_key(config, 'kea-server:user')

if user is None:
  handle_error('Configuration error - you need to specify a Kea API user.', 1)
password_type = get_config_key(config, 'kea-server:password:type')
if password_type is not None:
  if config['kea-server']['password']['type'] == 'file':
    with open(config['kea-server']['password']['file'], 'r') as fh:
      password = fh.readlines[0].strip()
else:
  password_value = get_config_key(config, 'kea-server:password')
  if password_value is not None:
    password = config['kea-server']['password']
  else:
    handle_error('Configuration error - you need to specify a password file or a password for the Kea Control agent.', 1)

commands = get_config_key(config, 'commands')
if commands is None:
  handle_error('Cannot invoke this agent without defined commands.')

url = f'http://{host}:{port}'
if command_name in commands:
  try:
    payload = json.loads(config['commands'][command_name])
  except Exception as e:
    handle_error(f'Configuration error - issue with command {command_name}', 1)

response = requests.post(url, json=payload, auth=HTTPBasicAuth(user, password), timeout=3)
if response.status_code == 200:
  data = response.json()
else:
  handle_error(f'Agent request error - Kea API returned response code {response.status_code}')