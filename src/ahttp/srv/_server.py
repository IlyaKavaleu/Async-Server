import asyncio
from functools import partial
from contextlib import asynccontextmanager
from src.ahttp.srv._controller import Controller


class Server:
    def __init__(self, *, host: str, port: int):
        self._host = host
        self._port = port

    async def _start(self):
        loop = asyncio.get_running_loop()
        server = partial(loop.create_server, Controller, host=self._host, port=self._port)
        async with self.serve(server) as srv:
            await srv.serve_forever()

    def __call__(self):
        return self._start()

    @asynccontextmanager
    async def serve(self, factory):
        print(f"Start: host - {self._host}, port - {self._port}")
        try:
            yield await factory()
        finally:
            print("\rStop")

