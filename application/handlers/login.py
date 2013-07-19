""" Handle the different types of logins """
import tornado
from tornado.auth import GoogleMixin
from application.lib.route import route
from application.lib.memcache_client import get_client as mc_client
import hashlib
import logging
from application.config import config
from application.lib.user import get_user

log = logging.getLogger(__name__)


class LoginHandler(tornado.web.RequestHandler):
    """ Login handler for oAuth services """

    def _on_auth(self, user):
        """ This is the callback method that is called on successful auth """
        if not user:
            raise tornado.web.HTTPError(500, "{0} auth failed".format(
                self.provider))

        if self.provider == "google":
            self.user_id = "google:{0}".format(user['email'])
            self.session_id = hashlib.sha224(user["claimed_id"]).hexdigest()

        elif self.provider == "twitter":
            self.user_id = "twitter:{0}".format(user['username'])
            self.session_id = hashlib.sha224(
                user["access_token"]['secret']).hexdigest()
        else:
            raise tornado.web.HTTPError(500, "No token set".format(
                self.provider))

        self.set_cookie("session_id", self.session_id)

        get_user(self.user_id, self.redirect_user)

    def redirect_user(self, user):
        """ After """
        if user is None:
            mc_client().set("temp:{0}".format(self.session_id),
                            self.user_id, time=60*5)
            self.redirect(self.get_argument("next", "/user/create"))
        else:
            mc_client().set(self.session_id, user, time=60*60*24*7)
            self.redirect(self.get_argument("next", "/lobby"))


@route(r'/login/twitter')
class TwitterHandler(LoginHandler, tornado.auth.TwitterMixin):
    """ Twitter login """

    @tornado.web.asynchronous
    def get(self):
        self.provider = 'twitter'
        self.settings['twitter_consumer_key'] = config['oAuth']['twitter']['key']
        self.settings['twitter_consumer_secret'] = config['oAuth']['twitter']['secret']
        if self.get_argument("oauth_token", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authorize_redirect()


@route(r'/login/google')
class GoogleHandler(LoginHandler, GoogleMixin):
    """ Google login """

    @tornado.web.asynchronous
    def get(self):
        self.provider = 'google'
        if self.get_argument("openid.mode", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect()
