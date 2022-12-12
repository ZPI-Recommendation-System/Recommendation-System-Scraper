import json
import pytest
import socketio
import src.websockets
from src.constants import BACKEND_URL, AUTH_TOKEN


class TestWebsockets:
    @pytest.fixture(scope='module')
    def connection(self):
        sio = socketio.Client()
        sio.connect(url=BACKEND_URL, headers={"Authorization": AUTH_TOKEN}, transports="websocket", wait=True,
                    wait_timeout=120)
        yield sio.wait()
        sio.disconnect()

    def test_websocket_connection(self, connection):
        assert connection.connected