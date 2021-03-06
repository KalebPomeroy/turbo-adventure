#!/usr/bin/env python
""" This init is not dumb and empty. It contains our config logic"""

import yaml

from application.lib.dict import deep_merge


class Config(dict):
    """ Configuration dictionary """

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

    def load_file(self, file_name):
        """ Given a config file, load it up """
        data = yaml.load(open(file_name, 'r'))

        if not isinstance(data, dict):
            raise Exception("config file not parsed correctly")

        deep_merge(self, data)

#
# Singleton Instance
#

config = Config()
