import click
import json
import logging.config
import sys
import yaml
import zmq
from . import azure

config = {
    'zmq': {
        'host': 'localhost',
        'port': 5680,
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

@click.command()
@click.option('--config', '-c', 'config_file', type=click.File('r'), required=True, help='Configuration file.')
@click.version_option()
def cli(config_file):
    '''ZeroMQ to Azure IoT Hub.'''
    try:
        config_yaml = yaml.safe_load(config_file)
        for key in config.keys():
            if type(config[key]) == dict:
                config[key].update(config_yaml.get(key, {}))
            elif key in config_yaml:
                config[key] = config_yaml[key]
    except Exception as e:
        logging.error('Failed opening configuration file')
        sys.exit(1)

    logging.config.dictConfig(config['log'])
    logging.info('Process started')

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
    try:
        cli()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        click.echo(str(e), err=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
