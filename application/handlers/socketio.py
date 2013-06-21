import logging

from tornadio2 import SocketConnection, event

log = logging.getLogger(__name__)

class Mediator(SocketConnection):

    # TODO: I should be able to have these events all over the place, not just here
    @event('event.connect')
    def connected_event(self, **kwargs):
        data = kwargs.get('data', None)[0]
        outbound_data = {"message": "Server: {0} connected.".format(data['username'])}
        self.emit('chat.add_message', outbound_data)

    @event('chat.say')
    def say_event(self, **kwargs):
        data = kwargs.get('data', None)[0]
        self.emit('chat.add_message', {"message": "{0} says: {1}".format("??", data['message'])})


    def on_message(self, message):
        log("got a message: {0}".format(message))