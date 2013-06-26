#!/usr/bin/env python

from tornado.web import RequestHandler, HTTPError
from application.lib.memcache_client import get_client as mc_client

class BaseHandler(RequestHandler):
    """ Contains helper methods for all request handlers """
    
    def current_user(self):

        

        return mc_client().get(self.get_cookie('session_id'))