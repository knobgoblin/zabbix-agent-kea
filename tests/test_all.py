#!/usr/bin/env python

import sys
import pytest
sys.path.append('..')

import yaml
import json
import agent_functions
from termcolor import colored as coloured

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
  config = open_config('zabbix-agent-kea.conf.test')
  password_type = agent_functions.get_config_key(config, 'kea-server:password:type')
  assert password_type is None

def test_no_config():
  config = open_config('zabbix-agent-kea.conf.test')
  no_key = agent_functions.get_config_key(config, 'fred')
  assert no_key is None

def test_password():
  config = open_config('zabbix-agent-kea.conf.test')
  server_password = agent_functions.get_config_key(config, 'kea-server:password')
  assert server_password == 'my secret password'

def test_standard_parse():
  config = open_config('zabbix-agent-kea.conf.test')
  password = agent_functions.verify_config_and_get_password(config)
  assert password == 'my secret password'

def test_invalid_command():
  config = open_config('zabbix-agent-kea.conf.test')
  password = agent_functions.verify_config_and_get_password(config)
  with pytest.raises(RuntimeError):
    response = agent_functions.exec_check(config, password, 'bogus')

def test_exec():
  config = open_config('zabbix-agent-kea.conf.test')
  password = agent_functions.verify_config_and_get_password(config)
  response = agent_functions.exec_check(config, password, 'status')
  assert json.dumps(response) == '[{"cache_item_value": "Response from Kea"}]'

def test_defaults1():
  config = open_config('zabbix-agent-kea.conf.defaults.test')
  server_password = agent_functions.verify_config_and_get_password(config)
  assert server_password == 'my password from a file'

def test_nouser():
  config = open_config('zabbix-agent-kea.conf.nouser.test')
  with pytest.raises(RuntimeError):
    server_password = agent_functions.verify_config_and_get_password(config)

def test_nopasswd():
  config = open_config('zabbix-agent-kea.conf.nopasswords.test')
  with pytest.raises(RuntimeError):
    server_password = agent_functions.verify_config_and_get_password(config)

def test_nocommands():
  config = open_config('zabbix-agent-kea.conf.nocommands.test')
  with pytest.raises(RuntimeError):
    server_password = agent_functions.verify_config_and_get_password(config)

def test_borkedcommand():
  config = open_config('zabbix-agent-kea.conf.borkedcommand.test')
  server_password = agent_functions.verify_config_and_get_password(config)
  with pytest.raises(RuntimeError):
    response = agent_functions.exec_check(config, server_password, 'status')