import yaml
import logging
from application.lib.route import route
from application.lib.template import render
from application.handlers.base import BaseHandler
from tornado.gen import Task as async
from application.lib.mediator import Mediator, subscribe
from tornado.web import asynchronous
from tornado import gen

from application.lib.fleet import get_fleets, create_fleet

mediator = Mediator()
log = logging.getLogger(__name__)


ships = yaml.load(open("application/config/data.yaml", 'r'))

@route(r'/hq')
@route(r'/hq/fleets')
class HQHandler(BaseHandler):
    @asynchronous
    @gen.engine
    def get(self):
        fleets = yield async(get_fleets, self.current_user()['user_id'])
        self.write(render('hq.html', {"fleets": fleets}))
        self.finish()

@route(r'/hq/fleets/new/?')
class FleetCollectionHandler(BaseHandler):
    @asynchronous
    @gen.engine
    def get(self):
        fleet = yield async(create_fleet, self.current_user()['user_id'])
        self.redirect("/hq/fleets/{0}".format(fleet))
        self.finish()

@route(r'/hq/fleets/([0-9a-z]+)/?')
class FleetHandler(BaseHandler):

    def get(self, fleet_id):
        self.write(render('build_fleet.html', ships))

@subscribe("hq.add_ship")
def say_event(session_id, event):
    for ship in ships['ships']:
        if (ship['name'] == event['ship']):
            mediator.publish_to_socketio([session_id], "hq.ship_added", ship)
