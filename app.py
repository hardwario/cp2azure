#!/usr/bin/env python3

import azure
import click
import logging.config
import sys
import yaml
import zmq
import json

config = {
    'zmq': {
        'host': 'localhost',
        'port': 1883,
        'timeout': 5000
    },
    'azure': {
        'connection_string': None
    },
    'log': {
        'disable_existing_loggers': False,
        'version': 1,
        'formatters': {
            'short': {
                'format': '%(asctime)s %(levelname)s %(name)s: %(message)s'
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'formatter': 'short',
                'class': 'logging.StreamHandler',
            }
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'ERROR'
            }
        }
    }
}

@click.command()
@click.option('--config', '-c', 'f', type=click.File('r'), required=True, help='Configuration file.')
@click.version_option()
def cli(f):
    '''ZeroMQ to Azure IoT Hub.'''
    try:
        config_yaml = yaml.safe_load(f)
        for key in config.keys():
            if type(config[key]) == dict:
                config[key].update(config_yaml.get(key, {}))
            elif key in config_yaml:
                config[key] = config_yaml[key]
    except Exception as e:
        logging.error('Failed opening configuration file')
        sys.exit(1)

    logging.config.dictConfig(config['log'])

    server()

def server():
    context = zmq.Context()

    sock = context.socket(zmq.SUB)
    sock.setsockopt_string(zmq.SUBSCRIBE, '')
    '''
    sock.setsockopt(zmq.RCVTIMEO, config['zmq']['timeout'])
    '''
    sock.connect('tcp://%s:%d' % (config['zmq']['host'], config['zmq']['port']))

    try:
        az = azure.AzureClient(config['azure']['connection_string'])
    except:
        logging.error('Failed to create Azure IoT Hub client', exc_info=True)
        sys.exit(1)

    while True:
        try:
            message = sock.recv_json()
            az.send(json.dumps(message))
        except zmq.error.Again as e:
            logging.error('ZeroMQ error: %s' % e)
        except Exception:
            logging.error('Unhandled exception', exc_info=True)

def main():
    cli()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
