#!/usr/bin/env python

import logging
import daemon
import os
import time
import sys

from optparse import OptionParser
from pkg_resources import resource_filename

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import StaticFileHandler, Application
from tornadio2 import TornadioRouter

from application.lib.autoload import autoload
from application.config import config
from application.lib.route import route
from application.handlers.socketio import Mediator

log = logging.getLogger(__name__)


def command_line_options():
    """ command line configuration """

    parser = OptionParser(usage="usage: %prog [options] <config_file>")

    parser.add_option('-d', '--debug', action="store_true",
                      dest="debug", default=False,
                      help="Start the application in debugging mode.")

    parser.add_option('-p', '--port', action="store",
                      dest="port", default=8000,
                      help="Set the port to listen to on startup.")

    parser.add_option('-a', '--address', action ="store",
                      dest="address", default=None,
                      help="Set the address to listen to on startup. Can be a hostname or an IPv4/v6 address.")

    options, args = parser.parse_args()

    # load the optional configuration file, if given
    if len(args) >= 1:
        config.load_file(args[0])
    else:
        config.load_file('application/config/config.yaml')

    return options



def serve():
    """ application entry point """
    
    # configure the application
    options = command_line_options()

    # setup logging
    log = logging.getLogger()
    handler = logging.FileHandler(config['logging']['file'])
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s"))
    log.addHandler(handler)
    log.setLevel(logging.DEBUG)
    
    if not options.debug:
        log.info("Starting in application in daemon mode")
        logfile = open(os.path.abspath(config['logging']['file']), 'a')
        ctx = daemon.DaemonContext(
                stdout=logfile,
                stderr=logfile,
                working_directory='.',
                files_preserve=[handler.stream])
        ctx.open()
    else:
        log.info("Starting in debug mode")

    autoload(resource_filename("application", "handlers"))
    
    routes = route.get_routes()
    routes.append((r"/public/(.*)", StaticFileHandler, {"path": "public"}))
    routes = routes + TornadioRouter(Mediator).urls
    log.info(routes)

    application = Application(routes, debug=options.debug, socket_io_port = 8000)
    
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
