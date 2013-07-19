import memcache

from application.config import config


def get_client():
    return memcache.Client(config['memcache']['servers'])
