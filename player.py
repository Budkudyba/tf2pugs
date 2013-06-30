# room class for handeling team and team db operations
# app made by Paul Kudyba
# December 2012
#

import datetime
from django.utils import simplejson
#import simplejson as json
import os

import webapp2
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template

from model_db import *
from functions import *

class PlayerPage(webapp2.RequestHandler):#----------------------------------used to create a room
    def get(self,page_id):
        home = self.request.host_url
        if not page_id:
            self.redirect(home)

        self.response.out.write('Player #: %s <br>' % page_id)

        q = Player.all()
        q.filter('steamid64', page_id)
        for p in q:
            self.response.out.write('Player Alias: %s <br>' % p.personaname)

        if users.get_current_user():
            steamid64 = parse_id(users.get_current_user().nickname())