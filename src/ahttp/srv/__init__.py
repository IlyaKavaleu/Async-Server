import asyncio
from argparse import ArgumentParser
from datetime import date
from ._server import Server

__all__ = ('run',)


def get_args():
    parser = ArgumentParser(
        prog="This is a Super server (c) {}\n".format(date.today().year)
    )
    parser.add_argument("--port", type=int, default=8000, help="Port")
    parser.add_argument("--host", default="127.0.0.1", help="Host"),
    return parser.parse_known_args()


def run():
    args, other = get_args()
    srv = Server(host=args.host, port=args.port)
    try:
        asyncio.run(srv())
    except KeyboardInterrupt:
        ...
