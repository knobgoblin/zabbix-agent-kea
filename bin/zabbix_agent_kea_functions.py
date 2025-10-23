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
      if get_config_key(config, 'kea-server:password:path') is None:
        raise RuntimeError('Kea control agent password specified as file but no file path specified')
      try:
        with open(config['kea-server']['password']['path'], 'r') as fh:
          pwlines = fh.readlines()
          password = pwlines[0].strip()
      except FileNotFoundError:
        raise FileNotFoundError(f'Could not find Kea control agent password file, {config["kea-server"]["password"]["path"]}')
  elif get_config_key(config, 'kea-server:password') is not None:
    password = config['kea-server']['password']
  else:
    raise RuntimeError('Configuration error - you need to specify a password file or a password for the Kea Control agent')

  if get_config_key(config, 'commands') is None:
    raise RuntimeError('Cannot invoke this agent without defined commands')

  return config, password

def exec_check(config, password, command_name):
  host = config['kea-server']['host']
  port = config['kea-server']['port']
  user = config['kea-server']['user']
  url = f'http://{host}:{port}'
  if command_name in config['commands']:
    try:
      payload = json.loads(config['commands'][command_name])
    except Exception as e:
      raise RuntimeError(f'Configuration error - issue with command {command_name!r}: {e}')
    response = requests.post(url, json=payload, auth=HTTPBasicAuth(user, password), timeout=3)
    if response.status_code == 200:
      return response.json()
    else:
      raise RuntimeError(f'Agent request error - Kea API returned response code {response.status_code}')
  else:
    raise RuntimeError(f'Command {command_name!r} is not valid')