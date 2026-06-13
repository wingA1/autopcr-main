import asyncio

from .httpserver import HttpServer
from ..constants import SERVER_PORT, SERVER_HOST
from ..db.dbstart import db_start
from ..module.crons import queue_crons
from ..util.memobserve import queue_memory_observer

server = HttpServer(host=SERVER_HOST, port=SERVER_PORT)

queue_crons()
queue_memory_observer()

asyncio.get_event_loop().create_task(db_start())

server.run_forever(asyncio.get_event_loop())
