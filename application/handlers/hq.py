""" This inclueds all of the /hq/.* routes and hq.* messages """
import yaml
import logging
from application.lib.route import route
from application.lib.template import render
from application.handlers.base import BaseHandler
from tornado.gen import Task as async
from application.lib.mediator import Mediator, subscribe
from tornado.web import asynchronous
from tornado import gen

from application.lib.memcache_client import get_client as mc_client
from application.lib import fleet

mediator = Mediator()
log = logging.getLogger(__name__)

game_data = yaml.load(open("application/config/data.yaml", 'r'))


@route(r'/hq')
@route(r'/hq/fleets')
class FleetCollectionHandler(BaseHandler):
    """ This is the fleet collection handler"""
    @asynchronous
    @gen.engine
    def get(self):
        fleets = yield async(fleet.get_fleets, self.current_user()['user_id'])
        self.write(render('hq.html', {"fleets": fleets}))
        self.finish()


@route(r'/hq/fleets/new/?')
class NewFleetHandler(BaseHandler):
    """ This is the new fleet handler """
    @asynchronous
    @gen.engine
    def get(self):
        new_fleet = yield async(fleet.create_fleet,
                                self.current_user()['user_id'])
        self.redirect("/hq/fleets/{0}".format(new_fleet))
        self.finish()


@route(r'/hq/fleets/([0-9]+)/?')
class FleetHandler(BaseHandler):
    """ This is the fleet detail handler"""

    def get(self, fleet_id):

        data = {
            "fleet_id": fleet_id,
            "ships": game_data['ships'],
            "weapons": game_data['weapons']
        }
        self.write(render('build_fleet.html', data))


#
# Messages for hq.*
#


@subscribe("hq.fleet.get")
@gen.engine
def get_fleet(session_id, event):
    """ Get a fleet """
    user = mc_client().get(session_id)['user_id']
    current_fleet = yield async(fleet.get_fleet, user, event['fleet_id'])
    mediator.publish_to_socketio([session_id], "hq.fleet.update",
                                 {'fleet': current_fleet})


@subscribe("hq.fleet.change_name")
@gen.engine
def change_name(session_id, event):
    """ Change the name of a fleet """
    user = mc_client().get(session_id)['user_id']
    yield async(fleet.change_name, user, event['fleet_id'], event['name'])


@subscribe("hq.fleet.remove_ship")
@gen.engine
def remove_ship(session_id, event):
    """ Remove a ship from the fleet """
    user = mc_client().get(session_id)['user_id']

    current_fleet = yield async(fleet.delete_ship, user,
                                event['fleet_id'], event['ship'])
    mediator.publish_to_socketio([session_id], "hq.fleet.update",
                                 {'fleet': current_fleet})


@subscribe("hq.fleet.add_ship")
@gen.engine
def add_ship(session_id, event):
    """ Add a ship to the fleet """
    user = mc_client().get(session_id)['user_id']

    current_fleet = yield async(fleet.add_ship, user, event['fleet_id'],
                                event['ship'])
    mediator.publish_to_socketio([session_id], "hq.fleet.update",
                                 {'fleet': current_fleet})
