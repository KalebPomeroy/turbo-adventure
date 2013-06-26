#!/usr/bin/env python

import logging
import motor
from  bson.objectid import ObjectId
from tornado import gen
from tornado.gen import Task as async
from application.lib.database import get_database, get_next_sequence

log = logging.getLogger(__name__)

@gen.engine
def get_fleet(user_id, fleet_id, callback):
    db = get_database()
    fleet = yield motor.Op(db.fleets.find_one, {"user_id": user_id, "fleet_id": fleet_id})
    callback(fleet)

@gen.engine
def create_fleet(user_id, callback):
    db = get_database()
    fleet_id = yield async(get_next_sequence, "fleets")
    fleet = yield motor.Op(db.fleets.insert, {
        "user_id": user_id, 
        "name": "Untitled Document",
        "ships": [],
        "credits": 0,
        "fleet_id": fleet_id
    })
    callback(fleet_id)

@gen.engine
def get_fleets(user_id, callback):
    db = get_database()
    f = db.fleets.find({"user_id": user_id})
    f.limit(1000)
    fleets = yield motor.Op(f.to_list)
    callback(fleets)

@gen.engine
def add_ship(user_id, fleet_id, ship, callback):
    db = get_database()
    fleet = yield motor.Op(db.fleets.find_one, {"user_id": user_id, "_id": fleet_id})
    log.info(user_id)
    log.info(fleet_id)
    log.info({"user_id": user_id, "fleet_id": int(fleet_id)})
    log.info(fleet)
    # Add the ship

    callback(fleet)

def phonetics():
    return [
        "Alpha"
        "Bravo"
        "Charlie"
        "Delta"
        "Echo"
        "Foxtrot"
        "Juliet"
        "Romeo"
        "Tango"
        "Whiskey"
        "Yankee"
    ]