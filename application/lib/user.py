#!/usr/bin/env python
import logging
import motor
from tornado import gen
from application.lib.database import get_database

log = logging.getLogger(__name__)


@gen.engine
def get_user(user_id, callback):

    db = get_database()
    user = yield motor.Op(db.users.find_one, {"user_id": user_id})
    callback(user)


@gen.engine
def get_user_by_username(username, callback):
    db = get_database()
    user = yield motor.Op(db.users.find_one, {"username": username})
    callback(user)


@gen.engine
def add_user(user_id, username, callback):
    db = get_database()
    user = yield motor.Op(db.users.insert, {
        "username": username,
        "user_id": user_id
    })
    callback(user)
