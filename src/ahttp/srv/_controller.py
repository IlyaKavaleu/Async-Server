import asyncio
import json
from dataclasses import dataclass
from src.ahttp.web.urls import urlspatterns
from datetime import datetime

RESPONSE_H = (
    "{version} 200 OK\r\n"
    "Date: {dt}\r\n"
    "Server: {srv}\r\n"
    "Content-Type: text/html\r\n"
    "Content-Length: {length}\r\n"
    "Connection: keep-alive"
)


@dataclass
class Request:
    meth: str
    path: str
    version: str
    headers: dict
    body: str

    def text(self):
        return self.body

    def json(self):
        return json.loads(self.body)


class Controller(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        raw_data = data.decode("utf-8")
        raw_info, raw_body = raw_data.split('\r\n\r\n')
        raw_http, *raw_headers = raw_info.split('\r\n')
        headers = dict(list(map(lambda l: tuple(l.split(': ')), raw_headers)))

        meth, path, version = raw_http.split(' ')
        req = Request(meth, path, version, headers, raw_body)

        handler = tuple(filter(lambda v: path == v[0], urlspatterns))[0][1]
        handler = next(controller for url_path, controller in urlpatterns if path == url_path)

        resp = handler(req)
        loop = asyncio.get_running_loop()

        def send_resp_cb(task: asyncio.Task):
            result = task.result()
            heads = RESPONSE_H.format(
                version=req.version,
                dt=datetime.now().strftime("%a %d %b %Y %H:%M:%S"),
                srv="Custom python framework",
                length=len(result)
            )
            response = f'{heads}\r\n\r\n{result}'

            self.transport.write(response.encode('utf-8'))
            self.transport.close()
        loop.create_task(resp).add_done_callback(send_resp_cb)
