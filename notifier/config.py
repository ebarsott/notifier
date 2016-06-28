#!/usr/bin/env python
"""
Read in a config file from the home directory that contains:
- from_email
- password
- host
- port
- to_email (optional)
"""

import ConfigParser
import os


defaults = {
    'host': 'smtp.gmail.com',
    'port': 587
}

config_section = 'notifier'
config_filename = '~/.notifier.ini'

required_keys = ['from_email', 'password', 'host', 'port']


def resolve_config(cfg):
    if 'to_email' in cfg:
        if ',' in cfg['to_email']:
            cfg['to_email'] = cfg['to_email'].split(',')
    if 'port' in cfg:
        cfg['port'] = int(cfg['port'])
    return cfg


def validate_config(cfg):
    for k in required_keys:
        if k not in cfg:
            raise KeyError("Notifer config missing key: %s" % k)


def load_config(fn=None):
    if fn is None:
        fn = os.path.abspath(os.path.expanduser(config_filename))
    parser = ConfigParser.ConfigParser(defaults)
    parser.read(fn)
    if not parser.has_section('notifier'):
        raise IOError("Invalid config[%s] missing notifier section" % fn)
    return resolve_config(dict(parser.items('notifier')))
