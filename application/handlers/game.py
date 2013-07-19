""" This handles all games/.* routes and any game.* messages """
from tornado import gen
from tornado.web import asynchronous

from application.lib.route import route
from application.handlers.base import BaseHandler
from tornado.gen import Task as async

from application.lib.mediator import Mediator, subscribe
from application.lib import game

mediator = Mediator()


@route("/games/new")
class NewGameHandler(BaseHandler):
    """ Handle the creation of a new game """

    # TODO: Technically, this should be a post?
    @asynchronous
    @gen.engine
    def get(self):
        game_id = yield async(game.create_new, self.current_user())
        self.redirect("/games/{0}".format(game_id))
        self.finish()


@route("/games/([0-9]+)/?")
class GameDetailHandler(BaseHandler):
    """ Handle the game route """

    def get(self, game_id):
        pass


#
# Messages for game.*
#


@subscribe("game.list_games")
@gen.engine
def list_active_games(session_id, event):
    """ Publish the list of current games """
    games = yield async(game.list_games)
    mediator.publish_to_socketio([session_id], "game.listed_games", games)
