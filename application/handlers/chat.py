from application.lib.route import route
from application.lib.template import render
from application.handlers.base import BaseHandler

@route(r'/chat')
class ChatHandler(BaseHandler):

    def get(self):
        self.write(render('chat.html'))

