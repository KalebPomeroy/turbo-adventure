#!/usr/bin/env python

import logging
import motor
import yaml
from random import choice
from  bson.objectid import ObjectId
from tornado import gen
from tornado.gen import Task as async
from application.lib.database import get_database, get_next_sequence

log = logging.getLogger(__name__)

game_data = yaml.load(open("application/config/data.yaml", 'r'))

@gen.engine
def get_fleet(user_id, fleet_id, callback):
    db = get_database()
    fleet = yield motor.Op(db.fleets.find_one, {"user_id": user_id, "fleet_id": int(fleet_id)})
    del fleet['_id']
    callback(fleet)

@gen.engine
def create_fleet(user_id, callback):
    db = get_database()
    fleet_id = yield async(get_next_sequence, "fleets")
    fleet = yield motor.Op(db.fleets.insert, {
        "user_id": user_id, 
        "name": "Untitled Document",
        "ships": {},
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
    query = {"user_id": user_id, "fleet_id": int(fleet_id)}
    fleet = yield motor.Op(db.fleets.find_one, query)
    
    new_ship_name = get_random_ship_name(ship)
    i = 0
    while( new_ship_name in fleet['ships'].keys() or i > 40):
        new_ship_name = get_random_ship_name(ship)
        i+=1

    fleet['credits'] += game_data['ships'][ship]['cost']
    fleet['ships'][new_ship_name] = {
        "type": ship,
        "primary": None,
        "secondary": None,
        "tertiary": None
    } 

    yield motor.Op(db.fleets.update, query, fleet)

    # Add the ship
    del fleet['_id']

    callback(fleet)

def get_random_ship_name(name):
    phonetics = [
        "Alpha",
        "Bravo",
        "Charlie",
        "Delta",
        "Echo",
        "Foxtrot",
        "Juliet",
        "Romeo",
        "Tango",
        "Whiskey",
        "Yankee"
    ]
    numbers = [
        " One",
        " Two",
        " Three",
        " Four"
    ]

    return "{0} {1}{2}".format(name, choice(phonetics), choice(numbers))




