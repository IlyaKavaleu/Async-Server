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
        start_tasks = asyncio.gather(*list(set([cur(self) for cur in self.on_start])))
        stst_start = []
        stst_stop = []
        for gcb in self.on_stst:
            it = gcb(self).__aiter__()
            stst_start.append(it.__anext__())
            stst_stop.append(it)
        start_tasks = asyncio.gather(*stst_start)
        try:
            yield await factory()
        finally:
            await stst_start
            await stst_stop
            for it in stst_stop[::-1]:
                try:
                    await it.__anext__()
                except StopAsyncIteration:
                    ...
            await asyncio.gather(*list(set([cur(self) for cur in self.on_stop])))
            print("\rStop")

