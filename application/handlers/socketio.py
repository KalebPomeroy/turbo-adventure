import logging

from tornadio2 import SocketConnection, event
from application.lib.mediator import Mediator, subscribe

log = logging.getLogger(__name__)

class SocketIOHandler(SocketConnection):
    def on_event(self, name, kwargs):
        Mediator().publish(name, kwargs)

@subscribe("chat.say")
def say_event(event):
    log.info(event)
    log.info("Saying event")

@subscribe("chat.say")
def say_event_loud(event):
    log.info(event)
    log.info("SAYING EVENT REALLY REALLY LOUD")
#     data = kwargs.get('data', None)[0]
#     self.emit('chat.add_message', {"message": "{0} says: {1}".format("??", data['message'])})

@subscribe("event.connect")
def connected_event(event):
    log.info(event)
    log.info("CONNECTED_EVENT")
#     data = kwargs.get('data', None)[0]
#     outbound_data = {"message": "Server: {0} connected.".format(data['username'])}
#     self.emit('chat.add_message', outbound_data)
