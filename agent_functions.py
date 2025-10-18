import json
import requests
from requests.auth import HTTPBasicAuth

def get_config_key(d, keylist, default=None):
  keys = keylist.split(':')
  for key in keys:
    if isinstance(d, dict) and key in d:
      d = d[key]
    else:
      return default
  return d

def verify_config_and_get_password(config):
  if get_config_key(config, 'kea-server:host') is None:
    config['kea-server']['host'] = '127.0.0.1'
  if get_config_key(config, 'kea-server:port') is None:
    config['kea-server']['port'] = '8000'
  if get_config_key(config, 'kea-server:user') is None:
    raise RuntimeError('No Kea server user provided - add it to your configuration')

  if get_config_key(config, 'kea-server:password:type') is not None:
    if config['kea-server']['password']['type'] == 'file':
      with open(config['kea-server']['password']['file'], 'r') as fh:
        pwlines = fh.readlines()
        password = pwlines[0].strip()
  elif get_config_key(config, 'kea-server:password') is not None:
    password = config['kea-server']['password']
  else:
    raise RuntimeError('Configuration error - you need to specify a password file or a password for the Kea Control agent')

  if get_config_key(config, 'commands') is None:
    raise RuntimeError('Cannot invoke this agent without defined commands')
  
  return password

def exec_check(config, password, command_name):
  host = config['kea-server']['host']
  port = config['kea-server']['port']
  user = config['kea-server']['user']
  url = f'http://{host}:{port}'
  print(command_name)
  print(config['commands'])
  if command_name in config['commands']:
    try:
      payload = json.loads(config['commands'][command_name])
    except Exception as e:
      raise RuntimeError(f'Configuration error - issue with command "{command_name}": {e}')

    response = requests.post(url, json=payload, auth=HTTPBasicAuth(user, password), timeout=3)
    if response.status_code == 200:
      return response.json()
    else:
      raise RuntimeError(f'Agent request error - Kea API returned response code {response.status_code}')
  else:
    raise RuntimeError(f'Command {command_name} is not valid')