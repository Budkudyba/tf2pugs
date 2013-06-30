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

class TeamPage(webapp2.RequestHandler):#----------------------------------------
    def get(self,page_id):
        home = self.request.host_url
        if not page_id:
            self.redirect(home)

        self.response.out.write('Your in room #: %s <br>' % page_id)

        if users.get_current_user():
            steamid64 = parse_id(users.get_current_user().nickname())

class CreateTeam(webapp2.RequestHandler):#------------------------------------- Handles the Create Team
    def post(self):
        if users.get_current_user():
            steamid64 = parse_id(users.get_current_user().nickname())

        team_name = self.request.get('team_name')
        team = Team(parent = team_key(team_name))

        team.leader = steamid64
        team.name = self.request.get('name')
        team.discription = self.request.get('discription')
        #team.picture =
        team.put()