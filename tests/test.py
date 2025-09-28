#!/usr/bin/env python

import yaml

def nested_get(d, keylist, default=None):
    keys = keylist.split(':')
    for key in keys:
        if isinstance(d, dict) and key in d:
            d = d[key]
        else:
            return default
    return d

with open('zabbix-agent-kea.conf.test') as fh:
  config = yaml.safe_load(fh)

print(config)

print(nested_get(config, 'kea-server:password:type'))
print(nested_get(config, 'fred'))
print(nested_get(config, 'kea-server:password'))
