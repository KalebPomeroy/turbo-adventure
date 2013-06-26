from tornado import gen
import logging
import motor
from application.lib.route import route
from application.lib.template import render
from application.handlers.base import BaseHandler

from application.lib.database import get_database
from application.lib.mediator import Mediator, subscribe
mediator = Mediator()

log = logging.getLogger(__name__)

@subscribe("queue.list_games")
@gen.engine
def list_active_games(session_id, event):

    db = get_database()
    cursor = db.games.find()
    cursor.limit(1000)
    games = yield motor.Op(cursor.to_list)
    for game in games:
        log.info(game)
        mediator.publish_to_socketio([session_id], "queue.add_game", {
            "game_id": game['game_id'],
            "host": game['host'],
            "opponent": game['opponent'],
        })
