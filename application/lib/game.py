#!/usr/bin/env python

import logging
import motor
import yaml
from copy import deepcopy
from random import choice
from  bson.objectid import ObjectId
from tornado import gen
from tornado.gen import Task as async
from application.lib.database import get_database, get_next_sequence

log = logging.getLogger(__name__)

game_data = yaml.load(open("application/config/data.yaml", 'r'))

@gen.engine
def list_games(callback):

    db = get_database()
    cursor = db.games.find()
    cursor.limit(1000)
    games = yield motor.Op(cursor.to_list)
    [g.pop('_id') for g in games]
    callback(games)

@gen.engine
def create_new(user, callback):
    db = get_database()   
    game_id = yield async(get_next_sequence, "games")
    game = yield motor.Op(db.games.insert, {
        "host": user['username'], 
        'host_user_id': user['user_id'],
        "game_id": game_id
    })
    callback(game_id)
