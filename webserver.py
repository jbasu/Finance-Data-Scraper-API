#!/usr/bin/python3

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from api import app

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(8399)
IOLoop.instance().start()