import asyncio
import time
from socket import gaierror

import websockets
from websockets.exceptions import ConnectionClosedError

from ._data_types import SocketConfig
from ... import TriggerableEventBatchSource, Event
from ..._private._utilities import *


class SocketListener(TriggerableEventBatchSource):
    def __init__(self,
                 socket_config: SocketConfig,
                 deserializer: Callable[[str], List[Any]],
                 initial_message_generator: Callable[[], List[str]] = lambda: [],
                 responder: Callable[[str], List[str]] = lambda message: [],
                 **kwargs):
        super().__init__(**kwargs)
        self.socket_config: SocketConfig = socket_config
        self.deserializer = deserializer
        self.initial_message_generator = initial_message_generator
        self.responder = responder
        self.last_try_for_connect = None
        self.current_reconnect_timeout = self.socket_config.initial_reconnect_timeout
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None

    def get_event_batch(self) -> List[Event]:
        event_string = asyncio.get_event_loop().run_until_complete(self._get_message_string())
        if event_string is None:
            return []
        try:
            return self.deserializer(event_string)
        except Exception as e:
            self.logger.exception(f"Failed to deserialize socket message \"{event_string}\": {e.__str__()}")

    async def _get_message_string(self) -> Optional[str]:
        if self.websocket is None:
            self.websocket = await self._get_initial_websocket()
            if self.websocket is None:
                return None
        try:
            message = await self.websocket.recv()
            responses: List[str] = self.responder(message)
            for response in responses:
                self.websocket.send(response)
            return message
        except ConnectionClosedError as e:
            self.logger.error(f"Disconnected from {self.socket_config.server.__str__()}: {str(e)}")
        except Exception as e:
            self.logger.exception(f"Disconnected from {self.socket_config.server.__str__()}: {str(e)}")
        self.websocket = None
        return None

    async def _get_initial_websocket(self) -> Optional[websockets.WebSocketClientProtocol]:
        if self.last_try_for_connect is not None and (
                self.last_try_for_connect + self.current_reconnect_timeout) > time.time():
            return None
        self.last_try_for_connect = time.time()
        self.current_reconnect_timeout = min(self.current_reconnect_timeout*2, self.socket_config.max_reconnect_timeout)
        self.logger.debug(f"Trying to connect to {self.socket_config.server.__str__()}")
        try:
            result = await websockets.connect(
                uri=self.socket_config.server.address,
                port=self.socket_config.server.port,
                **self.socket_config.connection_kwargs)
            self.logger.info(f"Connected to {self.socket_config.server.__str__()}")
            self.current_reconnect_timeout = self.socket_config.initial_reconnect_timeout
            for initial_message in self.initial_message_generator():
                await result.send(initial_message)
            return result
        except gaierror as e:
            self.logger.info(f"Failed to connect to {self.socket_config.server.__str__()}: {str(e)}. Retrying in {self.current_reconnect_timeout} seconds")
        except Exception as e:
            self.logger.exception(f"Failed to connect to {self.socket_config.server.__str__()}: {str(e)}. Retrying in {self.current_reconnect_timeout} seconds")
        return None
