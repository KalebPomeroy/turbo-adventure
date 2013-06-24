from application.lib.route import route
from application.lib.template import render
from application.handlers.base import BaseHandler

@route(r'/lobby')
class LobbyHandler(BaseHandler):

    def get(self):
        self.write(render('lobby.html'))

