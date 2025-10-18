#!/usr/bin/env python

import sys
sys.path.append('..')

import yaml
import json
import agent_functions
from termcolor import colored as coloured

with open('zabbix-agent-kea.conf.test', 'r') as fh:
  config = yaml.safe_load(fh)

with open('zabbix-agent-kea.conf.test', 'r') as fh:
  config_text = fh.read()

print()
print(coloured('#', 'blue'))
print(coloured('# Current test configuration:', 'blue'))
print(coloured('#', 'blue'))
print()
print(config_text)
print()

def test_no_password_type():
  password_type = agent_functions.get_config_key(config, 'kea-server:password:type')
  assert password_type is None

def test_no_config():
  no_key = agent_functions.get_config_key(config, 'fred')
  assert no_key is None

def test_password():
  server_password = agent_functions.get_config_key(config, 'kea-server:password')
  assert server_password == 'my secret password'

def test_standard_parse():
  password = agent_functions.verify_config_and_get_password(config)
  assert password == 'my secret password'

def test_exec():
  password = agent_functions.verify_config_and_get_password(config)
  response = agent_functions.exec_check(config, password, 'status')
  assert json.dumps(response) == '[{"cache_item_value": "Response from Kea"}]'