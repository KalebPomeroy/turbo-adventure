""" This handles all lobby/.* routes and any chat.* messages """
from application.lib.route import route
from application.lib.template import render
from application.handlers.base import BaseHandler

from application.lib.mediator import Mediator, subscribe
from application.lib.memcache_client import get_client as mc_client

mediator = Mediator()


@route(r'/lobby')
class LobbyHandler(BaseHandler):
    """ Render the lobby html """

    def get(self):
        self.write(render('lobby.html'))


#
# Messages for chat.*
#


@subscribe("event.connect")
def connected_event(session_id, event):
    """ Notify the user socket IO is talking to the server """
    mediator.publish_to_socketio([session_id], "chat.add_message",
                                 {"message": "Connected to server."})


@subscribe("chat.say")
def say_event(session_id, event):
    """ Publish a chat message to all clients """

    data = {
        "message_type": "self_chat",
        "message": "You said: {0}".format(event['message'])
    }
    mediator.publish_to_socketio([session_id], "chat.add_message", data)

    user = mc_client().get(session_id)['username']
    data = {
        "message_type": "another_player_chat",
        "message": "{0} says: {1}".format(user, event['message'])
    }

    mediator.publish_to_socketio(mediator.get_other_users(session_id),
                                 "chat.add_message", data)
