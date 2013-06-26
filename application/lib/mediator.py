#!/usr/bin/env python
import weakref
import functools
import logging
import datetime

import tornado
from tornado import gen
from tornado.ioloop import IOLoop

log = logging.getLogger(__name__)

class Mediator(object):
    channels = {}   
    sockets = {}

    def get_users(self):
        return Mediator.sockets.keys()

    def get_other_users(self, session_id):
        return [user for user in Mediator().get_users() if user != session_id] 

    def register_socket(self, session_id, socket):
        if(session_id not in Mediator.sockets):
            Mediator.sockets[session_id] = []

        if socket not in Mediator.sockets[session_id]:
            Mediator.sockets[session_id].append(socket)

    def publish(self, session_id, channel, event):
        if channel in Mediator.channels.keys():
            for subscriber in Mediator.channels[channel]:
                data = event['data'][0] if(len(event['data']) > 0) else None
                IOLoop.instance().add_callback(subscriber, session_id, data)

    def publish_to_socketio(self, session_ids, channel, event):
        for session_id, sockets in Mediator.sockets.iteritems():
            if session_id in session_ids:
                for socket in sockets:
                    socket.emit(channel, event)


    def subscribe(self, channel, handler):
        if(channel not in Mediator.channels):
            Mediator.channels[channel] = []

        if handler not in Mediator.channels[channel]:
            print("{0} to event {1}".format(handler, channel))
            Mediator.channels[channel].append(handler)

def subscribe(channel):
    def wrap(func):
        Mediator().subscribe(channel, func)
        return func

    return wrap
