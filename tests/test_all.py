#!/usr/bin/env python

import os
import sys
import pytest
sys.path.append('../bin')

import yaml
import json
import zabbix_agent_kea_functions
import zabbix_agent_kea
from termcolor import colored as coloured

import time
from functools import wraps

def sleep_after(seconds: float):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            time.sleep(seconds)
            return result
        return wrapper
    return decorator

def open_config(config_file):
  with open(config_file, 'r') as fh:
    config = yaml.safe_load(fh)

  with open(config_file, 'r') as fh:
    config_text = fh.read()

  print()
  print(coloured('#', 'blue'))
  print(coloured('# Current test configuration:', 'blue'))
  print(coloured('#', 'blue'))
  print()
  print(config_text)
  print()
  return config

def test_no_password_type():
  config = open_config('configs/zabbix-agent-kea.conf.test')
  password_type = zabbix_agent_kea_functions.get_config_key(config, 'kea-server:password:type')
  assert password_type is None

def test_no_config():
  config = open_config('configs/zabbix-agent-kea.conf.test')
  no_key = zabbix_agent_kea_functions.get_config_key(config, 'fred')
  assert no_key is None

def test_password():
  config = open_config('configs/zabbix-agent-kea.conf.test')
  password = zabbix_agent_kea_functions.get_config_key(config, 'kea-server:password')
  assert password == 'my secret password'

def test_standard_parse():
  config = open_config('configs/zabbix-agent-kea.conf.test')
  config, password = zabbix_agent_kea_functions.verify_config_and_get_password(config)
  assert password == 'my secret password'

def test_invalid_command():
  config = open_config('configs/zabbix-agent-kea.conf.test')
  config, password = zabbix_agent_kea_functions.verify_config_and_get_password(config)
  with pytest.raises(RuntimeError):
    response = zabbix_agent_kea_functions.exec_check(config, password, 'bogus')

@sleep_after(1)
def test_exec():
  config = open_config('configs/zabbix-agent-kea.conf.test')
  config, password = zabbix_agent_kea_functions.verify_config_and_get_password(config)
  response = zabbix_agent_kea_functions.exec_check(config, password, 'status')
  assert json.dumps(response) == '[{"cache_item_value": "Response from Kea"}]'

def test_defaults1():
  config = open_config('configs/zabbix-agent-kea.conf.defaults.test')
  config, password = zabbix_agent_kea_functions.verify_config_and_get_password(config)
  assert password == 'my password from a file'

def test_nouser():
  config = open_config('configs/zabbix-agent-kea.conf.nouser.test')
  with pytest.raises(RuntimeError):
    config, password = zabbix_agent_kea_functions.verify_config_and_get_password(config)

def test_nopasswd():
  config = open_config('configs/zabbix-agent-kea.conf.nopasswords.test')
  with pytest.raises(RuntimeError):
    config, password = zabbix_agent_kea_functions.verify_config_and_get_password(config)

def test_missing_password_file_path():
  config = open_config('configs/zabbix-agent-kea.conf.nopwfile.test')
  with pytest.raises(RuntimeError):
    config, password = zabbix_agent_kea_functions.verify_config_and_get_password(config)

def test_incorrect_password_file_path():
  config = open_config('configs/zabbix-agent-kea.conf.wrongpwfile.test')
  with pytest.raises(FileNotFoundError):
    config, password = zabbix_agent_kea_functions.verify_config_and_get_password(config)

def test_nocommands():
  config = open_config('configs/zabbix-agent-kea.conf.nocommands.test')
  with pytest.raises(RuntimeError):
    config, password = zabbix_agent_kea_functions.verify_config_and_get_password(config)

def test_borkedcommand():
  config = open_config('configs/zabbix-agent-kea.conf.borkedcommand.test')
  config, password = zabbix_agent_kea_functions.verify_config_and_get_password(config)
  with pytest.raises(RuntimeError):
    response = zabbix_agent_kea_functions.exec_check(config, password, 'status')

def test_server_error():
  config = open_config('configs/zabbix-agent-kea.conf.error.test')
  config, password = zabbix_agent_kea_functions.verify_config_and_get_password(config)
  with pytest.raises(RuntimeError):
    response = zabbix_agent_kea_functions.exec_check(config, password, 'status')

@sleep_after(1)
def test_basic_agent_call(capsys):
  zabbix_agent_kea.main(['--config', 'configs/zabbix-agent-kea.conf.test', 'status'])
  captured = capsys.readouterr()
  assert '[{"cache_item_value": "Response from Kea"}]' in captured.out

@sleep_after(1)
def test_agent_call_no_args():
  with pytest.raises(SystemExit):
    zabbix_agent_kea.main()

def test_agent_call_wrong_config_path():
  with pytest.raises(RuntimeError):
    zabbix_agent_kea.main(['--config', '/a/bogus/1948e38/configuration/file', 'status'])

@sleep_after(1)
def test_agent_call_config_from_env(capsys):
  os.environ['ZAK_CONFIG'] = 'configs/zabbix-agent-kea.conf.test'
  zabbix_agent_kea.main(['status'])
  captured = capsys.readouterr()
  assert '[{"cache_item_value": "Response from Kea"}]' in captured.out