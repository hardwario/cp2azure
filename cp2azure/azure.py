import logging
import threading
import queue
from azure.iot.device import IoTHubDeviceClient, Message


class AzureClient:

    def __init__(self, connection_string):
        self._client = IoTHubDeviceClient.create_from_connection_string(connection_string)
        self._client.connect()
        self._q = queue.Queue()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def _loop(self):
        while self._thread.is_alive():
            message = self._q.get()
            if message:
                msg = Message(message)
                self._client.send_message(msg)
            logging.info('Queue size: %d', self._q.qsize())

    def send(self, message):
        self._q.put(message)
        logging.info('Queue size: %d', self._q.qsize())
