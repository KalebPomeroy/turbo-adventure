#!/usr/bin/env python
""" Handle all of our mongodb stuff """

import logging

import motor
from tornado import gen
from pymongo.errors import DuplicateKeyError
from application.config import config

log = logging.getLogger(__name__)


class Connection(object):
    """ Basically just a safe place to stash the connection """

    conn = None

    @classmethod
    def create_connection(cls, io_loop=None, journaled=True):
        """ Create a database connection """

        host = config['mongodb']['server']['host']
        port = config['mongodb']['server']['port']
        database = config['mongodb']['database']
        username = config['mongodb']['server'].get('username', None)
        password = config['mongodb']['server'].get('password', None)
        ssl = config['mongodb']['server'].get('ssl', False)

        # setup the connection string
        conn_string = "{0}:{1}/{2}".format(host, port, database)

        if (username is not None) and (password is not None):
            conn_string = "{0}:{1}@{2}".format(username, password, conn_string)

        conn_string = "mongodb://{0}".format(conn_string)

        # create our connection
        connection = motor.MotorClient(
            conn_string,
            io_loop=io_loop,
            j=journaled,
            ssl=ssl
        )

        return connection.open_sync()


@gen.engine
def get_next_sequence(sequence, callback):
    """ Get the next value in a mongodb sequence """

    # this is guaranteed atomic by mongodb
    result = yield motor.Op(
        get_database().command,
        'findAndModify',
        'sequence',
        query={'_id': sequence},
        update={'$inc': {'seq': 1}},
        new=True
    )
    callback(result['value']['seq'])


def get_database(io_loop=None, journaled=True):
    """ Get a database reference from mongodb """

    if Connection.conn is None:
        Connection.conn = Connection.create_connection(
            io_loop=io_loop, journaled=journaled)

    return Connection.conn[config['mongodb']['database']]
