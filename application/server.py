#!/usr/bin/env python
"""
    This module is the actual server. It handles startup options,
    logging, and all configuration options
"""
import logging
import sys

from optparse import OptionParser

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import StaticFileHandler, Application
from tornadio2 import TornadioRouter

from application.config import config
from application.lib.route import route
from application import handlers


def command_line_options():
    """ command line configuration """

    parser = OptionParser(usage="usage: %prog [options] <config_file>")

    parser.add_option('-d', '--debug', action="store_true",
                      dest="debug", default=False,
                      help="Start the application in debugging mode.")

    parser.add_option('-p', '--port', action="store",
                      dest="port", default=8000,
                      help="Set the port to listen to on startup.")

    parser.add_option('-a', '--address', action="store",
                      dest="address", default=None,
                      help="Set the address to listen to on startup. Can be a "
                      "hostname or an IPv4/v6 address.")

    parser.add_option('-l', '--level', action="store",
                      choices=['DEBUG', 'INFO', 'WARNING',
                               'ERROR', 'CRITICAL'],
                      dest="log_level", default='INFO',
                      help="Set the log level. Logging messages which are less"
                      " severe than the specified level will not be logged.")

    options, args = parser.parse_args()

    # load the optional configuration file, if given
    if len(args) >= 1:
        config.load_file(args[0])
    else:
        config.load_file('application/config/config.yaml')

    return options


def configure_logging(options):
    """ setup application logging """

    log = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s"
    ))
    log.addHandler(handler)
    log.setLevel(options.log_level)

    return log


def serve():
    """ application entry point """

    # configure the application
    options = command_line_options()
    log = configure_logging(options)
    log.info("Starting application")
    # create the server
    routes = route.get_routes()
    routes.append((r"/public/(.*)", StaticFileHandler, {"path": "public"}))
    routes = routes + TornadioRouter(handlers.socketio.SocketIOHandler).urls

    application = Application(routes,
                              debug=options.debug,
                              socket_io_port=8000)

    server = HTTPServer(application)
    server.bind(options.port, options.address)

    if options.debug:
        server.start(1)
    else:
        server.start(0)

    # startup done, rock and roll
    log.info("Application Ready")
    IOLoop.instance().start()

if __name__ == "__main__":
    serve()
