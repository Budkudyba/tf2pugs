#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from google.appengine.api import urlfetch
from google.appengine.api import users
from google.appengine.ext import db
import json

'''class PlayerStats(db.Model):
    #retrieved regularly from steam
    steamid = db.StringProperty()
    personaname = db.StringProperty()
    profileurl = db.StringProperty()
    avatar = db.StringProperty()
    #kept in db
    kudos = db.StringListProperty()
    elo = db.IntegerProperty()
    pug_num = db.IntegerProperty()
    last_login = db.DateTimeProperty()'''

class GameRoom(db.Model):#------------------------------------------------------
    name = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add = True)
    leader = db.StringProperty()
    members = db.StringListProperty()
    region = db.StringProperty()
    rcon = db.StringProperty()
    level = db.StringProperty() #map name
    ip = db.StringProperty()
    password = db.StringProperty()
    active = db.BooleanProperty() #if the room has launched
def gameroom_key(gameroom_name=None):
    return db.Key.from_path('GameRoom',gameroom_name or 'default_gameroom')

class GameRoomCreate(webapp2.RequestHandler):#----------------------------------
    def post(self):
        if users.get_current_user():
            gameroomcreate_name = self.request.get('gameroomcreate_name')
            gameroom = GameRoom(parent = gameroom_key(gameroomcreate_name))
            gameroom.leader = parse_id(users.get_current_user().nickname())
            gameroom.ip = self.request.get('ip')
            gameroom.name = self.request.get('name')
            gameroom.rcon = self.request.get('rcon')
            gameroom.password = self.request.get('password')
            gameroom.level = self.request.get('level')
            gameroom.put()

            self.response.out.write('You made a room! Redirecting...')
            self.redirect('/')

class MainHandler(webapp2.RequestHandler):#-------------------------------------
    def get(self):
        #self.response.write('Hello world! v2.0 <br>')
        self.response.out.write("""
          <html>
            <body>""")
        user = users.get_current_user()
        if user:  # signed in already
            #parse url response into steamID
            urlnick = user.nickname().split('/')
            steamid64 = urlnick[-1] #last element
            #lookup steam info
            user_json = get_steam_user(steamid64)
            if user_json != False:
                for responsekey, responsevalue in user_json.iteritems():
                    for playerkey, playervalue in responsevalue.iteritems():
                        player_info = playervalue
            else:
                self.response.out.write('Player info not retrieved from valve!')

            self.response.out.write('<div>Hello %s [<a href="%s">sign out</a>]</div>' % (player_info[0]['personaname'], users.create_logout_url(self.request.uri)))

            #query db for gamerooms
            gameroom_name = self.request.get('gameroom_name')
            '''rooms = db.GqlQuery("SELECT *"
                                "FROM GameRoom"
                                "WHERE ANCESTOR IS :1 "
                                "ORDER BY date DESC LIMIT 50",
                                gameroom_key(gameroom_name))'''
            gamerooms = GameRoom.gql("WHERE ANCESTOR IS :1 ORDER BY date DESC LIMIT 50",
                             gameroom_key(gameroom_name))
            self.response.out.write('<div>')
            for gameroom in gamerooms:
                self.response.out.write('<div>')
                self.response.out.write('<b>%s</b>:' % gameroom.name)
                self.response.out.write('<b>%s</b>:' % gameroom.ip)
                self.response.out.write('<b>%s</b>:' % gameroom.level)
                self.response.out.write('</div>')
            self.response.out.write('</div>')

            #self.response.out.write('%s' % gameroom_key.id())

            #create room form
            self.response.out.write("""
                <div class="create_room">
                <h1>create a lobby</h1>
              <form action="/create" method="post">
                <div>      Name:<input type="text" name="name" maxlength ="20"</textarea></div>
                <div>IP address:<input type="text" name="ip" maxlength ="23"</textarea></div>
                <div> RCON Password:<input type="text" name="rcon"</textarea></div>
                <div> Room Password:<input type="text" name="password"</textarea></div>
                <div> Map:<input type="text" name="level"</textarea></div>
                <div><input type="submit" value="Create Room"></div>
              </form>
              </div>
            </body>
          </html>""")
        else:     # Not signed in--------------------
            self.response.out.write('Welcome to TF2 Pugs! Sign in here: ')
            #self.response.out.write('[<a href="%s">%s</a>]' % (users.create_login_url(federated_identity='http://steamcommunity.com/openid'), 'steam'))
            self.response.out.write('<a href="%s"><img src="%s"/></a>' % (users.create_login_url(federated_identity='http://steamcommunity.com/openid'), "/images/sits_large_noborder.png"))

"""class Room(object):
    def __init__(self, name, entity=None):
        self.name = name
        self.entity = entity
        if entity:
            if entity.has_key('user'):
                self.user = entity['user']
        else:
            self.user = None
        self.members = entity['members']
        self.
"""


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/create', GameRoomCreate)
], debug=True)

def get_steam_user(str):
    key = 'C32E0AC8282A2237AE9580042F7E3FAD'
    header = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key='
    url = header + key + '&steamids=' + str
    result = urlfetch.fetch(url)
    if result.status_code == 200:
        json_result = json.loads(result.content)
        return json_result
    else:
        return False

def parse_id(str):
    urlnick = str.split('/')
    return urlnick[-1] #last element










