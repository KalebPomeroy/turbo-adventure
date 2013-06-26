#!/usr/bin/env python

import logging

import motor
from tornado import gen
from tornado.web import asynchronous
from pymongo.errors import DuplicateKeyError
from application.config import config

log = logging.getLogger(__name__)

def create_connection(io_loop=None, journaled=True):
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
            j=journaled, # enable journaling for the application
            ssl=ssl
            # w="majority" # make sure writes hit the majority of the replicas
        )
    
    return connection.open_sync()

@gen.engine
def get_next_sequence(sequence, callback):
    """ Get the next value in a mongodb sequence """

    try: 
        get_database().sequence.insert({'_id': sequence, 'seq': 0})
    except DuplicateKeyError, e: 
        pass

    # this is guaranteed atomic by mongodb
    result = yield motor.Op(get_database().command, 
            'findAndModify', 
            'sequence',
            query={'_id': sequence}, 
            update={'$inc': {'seq': 1}},
            new=True
    )
    callback(result['value']['seq'])


def get_database(io_loop=None, journaled=True):
    """ Get a database reference from mongodb """
    
    global connection
    
    if connection is None:
        connection = create_connection(io_loop=io_loop, journaled=journaled)
    
    return connection[config['mongodb']['database']]

#
# singleton connection
#

connection = None
