#!/usr/bin/env python3

import os
import sys
import logging
import yaml
from schema import Schema, And, Or, Use, Optional, SchemaError


DEFAULT = {
    'log': {
        'disable_existing_loggers': False,
        'version': 1,
        'formatters': {
            'short': {
                'format': '%(asctime)s %(levelname)s %(module)s: %(message)s'
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'formatter': 'short',
                'class': 'logging.StreamHandler'
            }
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'DEBUG'
            }
        }
    }
}


def port_range(port):
    return 0 <= port <= 65535


schema = Schema({
    'zmq': {
        'host': And(str, len),
        'port': And(Use(int), port_range),
        'timeout': And(Use(int), lambda x: x > 0)
    },
    'azure': {
        'connection_string': And(str, len)
    },
    Optional('log'): dict
})


def load_config(config_file):
    config = yaml.safe_load(config_file)
    try:
        config = schema.validate(config)
    except SchemaError as e:
        # Better error format
        error = str(e).splitlines()
        del error[1]
        raise Exception(' '.join(error))

    _apply_default(config, DEFAULT)

    return config


def _apply_default(config, default):
    for key in default:
        if isinstance(default[key], dict):
            if key not in config:
                config[key] = default[key]
            else:
                _apply_default(config[key], default[key])
        else:
            config[key] = default[key]
