from application.lib.route import route
from application.handlers.base import BaseHandler

@route(r'/todo')
class TodoHandler(BaseHandler):

    def get(self):
        self.write("foo")