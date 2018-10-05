import click
import json
import logging.config
import sys
import yaml
import zmq
from . import azure
from .config import load_config



@click.command()
@click.option('--config', '-c', 'config_file', type=click.File('r'), required=True, help='Configuration file.')
@click.option('--test', is_flag=True, help='Test configuration file.')
def cli(config_file, test=False):
    '''ZeroMQ to Azure IoT Hub.'''

    try:
        config = load_config(config_file)
        config_file.close()
    except Exception as e:
        logging.error('Failed opening configuration file')
        logging.error(str(e))
        sys.exit(1)

    if test:
        click.echo("The configuration file seems ok")
        return

    logging.config.dictConfig(config['log'])
    logging.info('Process started')

    server(config)


def server(config):
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
