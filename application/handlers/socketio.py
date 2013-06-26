import logging

from tornadio2 import SocketConnection, event
from application.lib.mediator import Mediator, subscribe
from application.lib.memcache_client import get_client as mc_client
from time import gmtime, strftime

log = logging.getLogger(__name__)
mediator = Mediator()

class SocketIOHandler(SocketConnection):

    def on_open(self, request):
        session_id = request.get_cookie("session_id").value
        user = mc_client().get(session_id)

        if not user:
            mediator.publish_to_socketio([session_id], "chat.add_message", "Please login")
        else:
            self.session_id = session_id
            mediator.register_socket(session_id, self)            

    def on_event(self, name, kwargs):
        mediator.publish(self.session_id, name, kwargs)


