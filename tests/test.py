#!/usr/bin/env python

import yaml
from termcolor import colored as coloured

def nested_get(d, keylist, default=None):
    keys = keylist.split(':')
    for key in keys:
        if isinstance(d, dict) and key in d:
            d = d[key]
        else:
            return default
    return d

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
  password_type = nested_get(config, 'kea-server:password:type')
  assert password_type is None

def test_no_config():
  no_key = nested_get(config, 'fred')
  assert no_key is None

def test_password():
  server_password = nested_get(config, 'kea-server:password')
  assert server_password == 'my secret password'