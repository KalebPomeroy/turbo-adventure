import tornado
from tornado.auth import GoogleMixin
from application.lib.route import route
from application.lib.memcache_client import get_client as mc_client
import os
import hashlib


@route(r'/google/login')
class GoogleHandler(tornado.web.RequestHandler, GoogleMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("openid.mode", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect()

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Google auth failed")


        session_id = hashlib.sha224(user["claimed_id"]).hexdigest()
        self.set_cookie("session_id", session_id)
        mc_client().set(session_id, user, time=60*60*24*7)

        # TODO: See if the user is in the database
        # If not, send them to the  'Choose username' process
        self.redirect(self.get_argument("next", "/lobby"))

        # "first_name": "Kaleb", 
        # "claimed_id": "https://www.google.com/accounts/o8/id?id=AItOawmrPEqLHbW1H8L2O4_t4M-fC-csREVrdqI", 
        # "name": "Kaleb Pomeroy", 
        # "locale": "en", 
        # "last_name": "Pomeroy", 
        # "email": "nolwestel@gmail.com"