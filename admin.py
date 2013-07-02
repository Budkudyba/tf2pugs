# room class for handeling admin operations
# app made by Paul Kudyba
# December 2012
#

import datetime
from django.utils import simplejson
import os

import webapp2
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template

from model_db import *
from functions import *

class AdminHandler(webapp2.RequestHandler):#------------------------------------- Handles the Main Room
    def get(self):
        user = users.get_current_user()
        if user:
            steamid64 = parse_id(users.get_current_user().nickname())
            if steamid64 == "76561197990677771":
                self.response.out.write("hello, Paul")
                #create room form
                self.response.out.write("""
                    <div class="create_news">
                    <h1>Create News Post</h1>
                    <form action="/newspost" method="post">
                    <div>Message:<textarea type="text" name="message"></textarea></div>
                    <div><input type="submit" value="Post News"></div>
                    </form>
                    </div>
                    </body>
                    </html>""")
                self.response.out.write("""<hr>""")
                self.response.out.write("""
                    <form action="/create" method="post">
                    <div>Name:<input type="text" name="name" maxlength ="21"></div>
                    <div>IP address:<input type="text" name="ip" maxlength ="23"></div>
                    <div>RCON Password:<input type="text" name="rcon"></div>
                    <div>Room Password:<input type="text" name="pass"placeholder="not availible yet" disabled></div>
                    <div>Map:<input type="text" name="map"></div>
                    <div>Game Type:<select name="type">
                    <option disabled="disabled">6v6</option>
                    <option selected="selected">highlander(9v9)</option>
                    <option disabled="disabled">ultiduo(2v2)</option>
                    <option disabled="disabled">8v8</option>
                    </select>
                    <div><input type="submit" id="create_room_button" value="Create Room"></div>
                    </form>
                    """)
                self.response.out.write("""<hr>""")
                self.response.out.write("""
                    <form action="/forceReady" method="post">
                    <div>RoomID:<input type="text" name="room"></div>
                    <div><input type="submit" id="create_room_button" value="MakeReady"></div>
                    </form>
                    """)
                self.response.out.write("""
                    <form action="/forceLaunch" method="post">
                    <div>RoomID:<input type="text" name="room"></div>
                    <div><input type="submit" id="create_room_button" value="MakeLaunch"></div>
                    </form>
                    """)
            else:
                self.response.out.write("You are not logged in as a regestered admin D:  %s" % steamid64)
        else:
            self.redirect('/login')