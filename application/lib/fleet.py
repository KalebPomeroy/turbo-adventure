#!/usr/bin/env python
""" All logic for fleets belong here """

import logging
import motor
import yaml
from copy import deepcopy
from random import choice
from tornado import gen
from tornado.gen import Task as async
from application.lib.database import get_database, get_next_sequence

log = logging.getLogger(__name__)

game_data = yaml.load(open("application/config/data.yaml", 'r'))


@gen.engine
def change_name(user_id, fleet_id, name, callback):
    """ Change the name of a fleet"""
    query = {"user_id": user_id, "fleet_id": int(fleet_id)}
    fleet = yield motor.Op(get_database().fleets.find_and_modify, query,
                           {"$set": {"name": name}})
    del fleet['_id']
    callback(fleet)


@gen.engine
def get_fleet(user_id, fleet_id, callback):
    """ Get all of the details about a fleet """
    fleet = yield motor.Op(get_database().fleets.find_one,
                           {"user_id": user_id, "fleet_id": int(fleet_id)})
    del fleet['_id']
    callback(fleet)


@gen.engine
def create_fleet(user_id, callback):
    """ Create a new fleet """
    fleet_id = yield async(get_next_sequence, "fleets")
    yield motor.Op(get_database().fleets.insert, {
        "user_id": user_id,
        "name": "Untitled Document",
        "ships": {},
        "credits": 0,
        "fleet_id": fleet_id
    })
    callback(fleet_id)


@gen.engine
def get_fleets(user_id, callback):
    """ Get a list of fleets belonging to the current user """
    f = get_database().fleets.find({"user_id": user_id})
    f.limit(1000)
    fleets = yield motor.Op(f.to_list)
    callback(fleets)


@gen.engine
def delete_ship(user_id, fleet_id, ship, callback):
    """ Remove a fleet from a ship """

    query = {"user_id": user_id, "fleet_id": int(fleet_id)}
    fleet = yield motor.Op(get_database().fleets.find_one, query)
    fleet['credits'] -= get_weapon_cost(fleet["ships"][ship]['weapons']['Primary'])
    fleet['credits'] -= get_weapon_cost(fleet["ships"][ship]['weapons']['Secondary'])
    fleet['credits'] -= get_weapon_cost(fleet["ships"][ship]['weapons']['Tertiary'])

    fleet['credits'] -= fleet["ships"][ship]['cost']
    del fleet["ships"][ship]

    yield motor.Op(get_database().fleets.update, query, fleet)

    del fleet['_id']
    callback(fleet)


@gen.engine
def add_ship(user_id, fleet_id, ship_details, callback):
    """ Add a fleet to a ship """

    query = {"user_id": user_id, "fleet_id": int(fleet_id)}
    fleet = yield motor.Op(get_database().fleets.find_one, query)

    new_ship_name = get_random_ship_name(ship_details['type'])
    i = 0
    while(new_ship_name in fleet['ships'].keys() or i > 40):
        new_ship_name = get_random_ship_name(ship_details['type'])
        i += 1

    ship = deepcopy(game_data['ships'][ship_details['type']])

    del ship['description']
    # TODO: Fix the mixed caps
    ship['weapons'] = {
        "Primary": ship_details['primary'],
        "Secondary": ship_details['secondary'],
        "Tertiary": ship_details['tertiary'],
    }

    fleet['credits'] += get_weapon_cost(ship_details['primary'])
    fleet['credits'] += get_weapon_cost(ship_details['secondary'])
    fleet['credits'] += get_weapon_cost(ship_details['tertiary'])
    fleet['credits'] += ship['cost']

    fleet['ships'][new_ship_name] = ship

    yield motor.Op(get_database().fleets.update, query, fleet)

    # Add the ship
    del fleet['_id']

    callback(fleet)


def get_weapon_cost(weapon_name):
    """ Get the cost of a weapon by name """
    for list_of_weapons in game_data['weapons'].values():
        for weapon in list_of_weapons.values():
            if(weapon['name'] == weapon_name):
                return weapon['cost']
    return 0


def get_random_ship_name(name):
    """ Generate a random name for a new ship """
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
