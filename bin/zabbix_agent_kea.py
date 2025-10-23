#!/usr/bin/env python

import os
import sys
import json
import yaml
import argparse
import logging
import zabbix_agent_kea_functions

def main(provided_args=None):

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
    default='no-command',
    help="Meta-command for the agent to run"
  )

  if provided_args is None:
    provided_args = sys.argv[1:]
  
  args = parser.parse_args(provided_args)

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

  logging.info(f'Executing diagnostic {args.command!r}')
  config, password = zabbix_agent_kea_functions.verify_config_and_get_password(config)
  
  logging.basicConfig(
    filename=config['logging']['logfile'],
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
  )

  logging.info(f'Executing Zabbix Kea agent with command {args.command!r}')
  response = zabbix_agent_kea_functions.exec_check(config, password, args.command)

  print(json.dumps(response))

if __name__ == "__main__":
  main()