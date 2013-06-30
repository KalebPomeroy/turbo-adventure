import motor
from tornado import gen
from tornado.web import asynchronous

from application.lib.route import route
from application.lib.template import render
from application.handlers.base import BaseHandler
from tornado.gen import Task as async

from application.lib.mediator import Mediator, subscribe
from application.lib.memcache_client import get_client as mc_client
from application.lib import game

from application.lib.database import get_database

mediator = Mediator()

@route(r'/lobby')
class LobbyHandler(BaseHandler):

    def get(self):
        self.write(render('lobby.html'))


@subscribe("chat.say")
def say_event(session_id, event):
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

    mediator.publish_to_socketio(mediator.get_other_users(session_id), "chat.add_message", data)

@subscribe("event.connect")
def connected_event(session_id, event):
    mediator.publish_to_socketio([session_id], "chat.add_message",  {"message": "Connected to server."})
    
@subscribe("queue.list_games")
@gen.engine
def list_active_games(session_id, event):
    games = yield async(game.list_games)
    mediator.publish_to_socketio([session_id], "queue.listed_games", games)


@route("/games/new")
class NewGameHandler(BaseHandler):
    @asynchronous
    @gen.engine
    def get(self):
        game_id = yield async(game.create_new, self.current_user())       
        self.redirect("/games/{0}".format(game_id))
        self.finish()
        

@route("/games/([0-9]+)/?")
class NewGameHandler(BaseHandler):
    def get(self, game_id): 
        pass
