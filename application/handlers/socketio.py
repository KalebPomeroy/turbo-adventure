""" Handler for socket IO """
import logging

from tornadio2 import SocketConnection
from application.lib.mediator import Mediator
from application.lib.memcache_client import get_client as mc_client

log = logging.getLogger(__name__)
mediator = Mediator()


class SocketIOHandler(SocketConnection):
    """ Class to handle on_opens and on_events """

    def on_message(self, message):
        raise NotImplementedError("No Messages Yet")

    def on_open(self, request):
        session_id = request.get_cookie("session_id").value
        user = mc_client().get(session_id)

        if not user:
            mediator.register_socket(session_id, self)
            mediator.publish_to_socketio([session_id], "chat.add_message",
                                         {"message": "Please login"})
            mediator.destroy_socket(session_id)
        else:
            self.session_id = session_id
            mediator.register_socket(session_id, self)

    def on_event(self, name, kwargs):
        if hasattr(self, 'session_id'):
            mediator.publish(self.session_id, name, kwargs)
