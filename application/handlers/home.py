import logging

from tornado.web import asynchronous

from tornado import gen
from tornado.gen import Task as async

from application.lib.route import route
from application.lib.template import render
from application.handlers.base import BaseHandler
from application.lib.user import get_user_by_username, add_user
from application.lib.memcache_client import get_client as mc_client
from random import choice

log = logging.getLogger(__name__)

@route(r'/')
class HomeHandler(BaseHandler):

    def get(self):
        self.write(render('index.html'))




@route(r'/user/create')
class HomeHandler(BaseHandler):

    def silly_header(self):
        verbs = ["Preparing", "Readying", "Last check of the", "Loading", "Securing", 
                "Doubling"]
        nouns = ["missiles", "lasers", "fighters", "docking bay", "warheads", 
                "atomic subparticles"]
        return "{0} {1}...".format(choice(verbs), choice(nouns))

    def get(self):
        self.write(render('create_account.html', {
            "silly_header": self.silly_header(),
            "message": "While we do so, why don't you create an amazingly epic username."
        }))

    @asynchronous
    @gen.engine
    def post(self):
        username = self.get_argument('username')
        session_id = self.get_cookie("session_id")
        

        if username == "":
            self.write(render('create_account.html', {
                "silly_header": self.silly_header(),
                "message": "Don't be silly. You can think of a better name than nothing."
            }))

        elif (len(username) > 20):
            self.write(render('create_account.html', {
                "silly_header": self.silly_header(),
                "message": "That's way too epic. Try a shorter nickname (20 characters or less)."
            }))
        else:
            user = yield async(get_user_by_username, username)
            if user is None:
                user_id = mc_client().get("temp:{0}".format(session_id))
                user = yield async(add_user, user_id, username)

                mc_client().set(session_id, {"username": username}, time=60*60*24*7)
                self.redirect(self.get_argument("next", "/lobby"))
            else:
                self.write(render('create_account.html', {
                    "silly_header": self.silly_header(),
                    "message": "Too epic - someone else already has that username. Try again."
                }))

        self.finish()
