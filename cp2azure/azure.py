import iothub_client
import logging

PROTOCOL = iothub_client.IoTHubTransportProvider.AMQP
RECEIVE_CONTEXT = 0
CONNECTION_STATUS_CONTEXT = 0
MESSAGE_TIMEOUT = 10000


class AzureClient:

    def __init__(self, connection_string):
        self._client = iothub_client.IoTHubClient(connection_string, PROTOCOL)
        self._client.set_option('messageTimeout', MESSAGE_TIMEOUT)
        self._client.set_connection_status_callback(self._connection_status_callback, CONNECTION_STATUS_CONTEXT)
        self._client.set_message_callback(self._receive_message_callback, RECEIVE_CONTEXT)

    def send(self, message):
        try:
            m = iothub_client.IoTHubMessage(message)
            self._client.send_event_async(m, self._send_confirmation_callback, None)
        except iothub_client.IoTHubError as e:
            logging.error('Azure IoT Hub error: %s', e)
        except Exception as e:
            logging.error('Unhandled exception', exc_info=True)

    def _connection_status_callback(self, result, reason, user_context):
        logging.info('Connection status: %s (%d)', result, reason)

    def _receive_message_callback(self, message, counter):
        logging.info('Received message: %s', message)

    def _send_confirmation_callback(self, message, result, user_context):
        logging.info('Send confirmation: %s', result)
