#!/usr/bin/env python

import sys
import yaml
import argparse
import os
import agent_functions

parser = argparse.ArgumentParser(description="Zabbix agent for kea")

parser.add_argument(
  "-c",
  "--config",
  type=str,
  default='/usr/local/etc/zabbix-agent-kea.conf.yaml',
  help="Path to the agent's configuration file"
)

parser.add_argument(
  "command",
  nargs="?",
  default=None,
  help="Meta-command for the agent to run"
)
args = parser.parse_args()

if '--config' not in sys.argv and '-c' not in sys.argv:
  env_config = os.environ.get('ZAK_CONFIG')
  if env_config is not None:
    config_file = env_config
  else:
    config_file = args.config
else:
  config_file = args.config

try:
  with open(config_file, 'r') as fh:
    config = yaml.safe_load(fh)
except Exception as e:
  raise RuntimeError(f'Could not load configuration file for agent: {e}')

password = agent_functions.verify_config_and_get_password(config)
response = agent_functions.exec_check(config, password, args.command)