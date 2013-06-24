import logging

from tornadio2 import SocketConnection, event
from application.lib.mediator import Mediator, subscribe
from application.lib.memcache_client import get_client as mc_client

log = logging.getLogger(__name__)
mediator = Mediator()

class SocketIOHandler(SocketConnection):

    def on_open(self, request):
        session_id = request.get_cookie("session_id").value
        user = mc_client().get(session_id)

        if not user:
            mediator.publish("error", {
                "reason": "unauthorized", 
                "message": "Could not find user in memcached"
            })
        else:
            self.session_id = session_id
            mediator.register_socket(session_id, self)            

    def on_event(self, name, kwargs):
        mediator.publish(self.session_id, name, kwargs)

@subscribe("chat.say")
def say_event(session_id, event):
    data = {"message": "You said: {0}".format(event['message'])}
    mediator.publish_to_socketio([session_id], "chat.add_message", data)

    user = mc_client().get(session_id)
    data = {"message": "{0} says: {1}".format(user['name'], event['message'])}

    mediator.publish_to_socketio(mediator.get_other_users(session_id), "chat.add_message", data)

@subscribe("event.connect")
def connected_event(session_id, event):
    mediator.publish_to_socketio([session_id], "chat.add_message",  {"message": "Connected to server."})
    




