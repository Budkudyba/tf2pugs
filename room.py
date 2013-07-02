# room class for handeling rooms and room db operations
# app made by Paul Kudyba
# December 2012
#

import datetime
from django.utils import simplejson
#import simplejson as json
import os
import random

import webapp2
from google.appengine.api import channel
from google.appengine.api import urlfetch
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template

from model_db import *
from functions import *

class GameRoomCreate(webapp2.RequestHandler):#----------------------------------used to create a room
    def post(self):
        if users.get_current_user():
            steamid64 = parse_id(users.get_current_user().nickname())

            gameroomcreate_name = self.request.get('gameroomcreate_name')
            gameroom = GameRoom(parent = gameroom_key(gameroomcreate_name))
            gameroom.leader = steamid64
            gameroom.ip = self.request.get('ip')
            gameroom.name = self.request.get('name')
            self.response.out.write(gameroom.name)
            gameroom.rcon = self.request.get('rcon')
            gameroom.password = self.request.get('pass')
            gameroom.level = self.request.get('map')
            gameroom.gstyle = self.request.get('type')
            gameroom.mic = self.request.get('req')
            if gameroom.mic:
                gameroom.mumble = self.request.get('mumble')
            gameroom.specAllow = self.request.get('spec')
            gameroom.put()
            gameroom.number = gameroom.key().id()
            gameroom.put()

            room = {
                'type': "room",
                'name': gameroom.name,
                'members': gameroom.members,
                'elo': gameroom.elo,
                'mic': gameroom.mic,
                'style': gameroom.gstyle,
                'number': gameroom.number,
                'level': gameroom.level,
                #'date': gameroom.date, //needs to be formatted differently
            }
            message = simplejson.dumps(room)
            s = ActiveChannelMember.all()
            for r in s:
                channel.send_message(r.steamid64, message)
            self.response.out.write("Room Created")
            #self.redirect('/')

class GameRoomDisband(webapp2.RequestHandler):#---------------------------------Used to disband a room
    def post(self):
        if users.get_current_user():
            steamid64 = parse_id(users.get_current_user().nickname())
            room = self.request.get('room')

            key = db.Key.from_path('GameRoom','default_gameroom','GameRoom', long(room))
            record = GameRoom.get(key)
            if steamid64 == record.leader:
                #remove room from join menu
                response2 = {
                        'type': "remove_room",
                        'reason': "The Room was Disbanded by the leader",
                        'room': room,
                }
                message2 = simplejson.dumps(response2)
                for player in record.members:
                    channel.send_message(player.split(';')[0], message2)
                #remove everyone from room
                response = {
                        'type': "quit",
                        'reason': "The room was disbanded by the leader",
                }
                message = simplejson.dumps(response)
                for player in record.members:
                    channel.send_message(player.split(';')[0], message)
                #remove db entry
                record.delete()


class GameRoomEnter(webapp2.RequestHandler):#-----------------------------------used to enter a room
    def post(self):
        if users.get_current_user():
            steamid64 = parse_id(users.get_current_user().nickname())
            room = self.request.get('room')
            now  = datetime.datetime.now()

            key = db.Key.from_path('GameRoom','default_gameroom','GameRoom', long(room))
            record = GameRoom.get(key)
            if record:
                if record.active and not check_for_player(record.banned,steamid64):
                    q = ActiveChannelMember.all()
                    q.filter('steamid64', steamid64)
                    for p in q:
                        alias = p.personaname
                        p.currrentRoom = long(room)
                        p.put()
                    append_name = steamid64 + ';' + '0000000000' + ";" + alias
                else:
                    popup(steamid64, "Room Not Active.")
                if not check_for_player(record.members,steamid64):
                    record.members.append(db.Text(append_name))
                    record.put()
                #Leader Info
                q = Player.all()
                q.filter('steamid64', record.leader)
                for p in q:
                    alias = p.personaname

                if record.leader == steamid64:
                    disband_able = True
                else:
                    disband_able = False

                #send ROOM INFO JSON
                response = {
                        'type': "room_info",
                        'name': record.name,
                        'mumble': record.mumble,
                        'leader': alias,
                        'level': record.level,
                        'disband': disband_able,
                        'id':   record.number,
                    }
                message = simplejson.dumps(response)
                channel.send_message(steamid64, message)

                players = []
                for m in record.members:
                    user_info = m.split(';')
                    if  m == record.members[-1]:
                        update_type = "update_end"
                    else:
                        update_type = "update_room"
                    user = {
                    "type": update_type,
                    'alias': user_info[2],
                    'id':   user_info[0],
                    'classes': user_info[1],
                    }
                    players.append(user)
                message_mbrs = simplejson.dumps(players)
                channel.send_message(steamid64, message_mbrs)

class GameRoomLeave(webapp2.RequestHandler):#-----------------------------------used to leave a room
    def post(self):
        if users.get_current_user():
            steamid64 = parse_id(users.get_current_user().nickname())
            self.response.out.write('You\'re leaving a room!<br>')
            room = self.request.get('room')
            if room != "": #check to see if player is actually in a room
                q = ActiveChannelMember.all()
                q.filter('steamid64', steamid64)
                for p in q:
                    p.currrentRoom = None
                    p.put()

                key = db.Key.from_path('GameRoom','default_gameroom','GameRoom', long(room))

                record = GameRoom.get(key)
                if record:
                    if record.members:
                        if check_for_player(record.members,steamid64):
                            #remove
                            record.members = remove_player(record.members,steamid64)
                            record.put()
                    if record.members != None:
                        players = []
                        for m in record.members:
                            user_info = m.split(';')
                            if  m == record.members[-1]:
                                update_type = "update_end"
                            else:
                                update_type = "update_room"
                            user = {
                                "type": update_type,
                                'alias': user_info[2],
                                'id':   user_info[0],
                                'classes': user_info[1],
                            }
                            players.append(user)
                        message_mbrs = simplejson.dumps(players)
                        for player in players:
                            channel.send_message(player['id'], message_mbrs)

                else:
                    self.response.out.write('db error!')

class GameRoomGet(webapp2.RequestHandler):#-------------------------------------used to retrieve room info
    def post(self):
        self.response.out.write('wigwam')
        steamid64 = parse_id(users.get_current_user().nickname())

        q = GameRoom.all()
        q.filter('active', True)
        q.filter('picking', False)
        rooms = []
        for gameroom in q:
            room = {
                'type': "room",
                'name': gameroom.name,
                'members': gameroom.members,
                'elo': gameroom.elo,
                'mic': gameroom.mic,
                'style': gameroom.gstyle,
                'number': gameroom.number,
                #'date': gameroom.date, //needs to be formatted differently
            }
            rooms.append(room)
        message = simplejson.dumps(rooms)
        #send message to requester
        channel.send_message(steamid64, message)

class ToggleClass(webapp2.RequestHandler):#-------------------------------------used to pick/unpick classes in a room ##LOBBY STYLE EDIT
    def post(self):
        steamid64 = parse_id(users.get_current_user().nickname())
        room = self.request.get('room')
        _class = int(self.request.get('class'))#the index of the class to change (0=scout,red=9-17)
        mod_class = _class
        if mod_class > 8:
            mod_class -= 9
            red = True
        else:
            red = False

        key = db.Key.from_path('GameRoom','default_gameroom','GameRoom', long(room))
        record = GameRoom.get(key)

        #get old info and remove player
        member_info = get_member(record.members,steamid64)#steamid64;classes;alias
        classes_picked = member_info[1]
        alias = member_info[2]
        record.members = remove_player(record.members,steamid64)

        if not class_full_lobby(record.members,_class,1):
            class_list = list('0000000000')
            class_list[mod_class] = '1'
            if red == True:
                class_list[9] = '1'
            new_classes = "".join(class_list)
            #readd with new classes
            append_name = steamid64 + ';' + new_classes + ';' + alias
            #record.members = remove_player(record.members,steamid64)
            record.members.append(db.Text(append_name))
            record.put()

            #check for launch
            if check_number_added(record.members) == 18:
                rdy_message = {
                    'type': "launch",
                    'room': room
                }
                for m in record.members:
                    user_info = m.split(';')
                message = simplejson.dumps(rdy_message)
                channel.send_message(user_info[0], message)

            #JSON to other members
            players = []
            for m in record.members:
                user_info = m.split(';')
                if  m == record.members[-1]:
                    update_type = "update_end"
                else:
                    update_type = "update_room"
                user = {
                    "type": update_type,
                    'alias': user_info[2],
                    'id':   user_info[0],
                    'classes': user_info[1],
                }
                players.append(user)
            message = simplejson.dumps(players)
            #send message to everyone in the room
            for player in players:
                channel.send_message(player['id'], message)
        else:
            popup(steamid64,"Class Limit Reached")

class ForceReady(webapp2.RequestHandler):#--------------------------------------used to force a room ready
    def post(self):
        steamid64 = parse_id(users.get_current_user().nickname())
        if steamid64 == "76561197990677771":
            room = self.request.get('room')
            key = db.Key.from_path('GameRoom','default_gameroom','GameRoom', long(room))
            record = GameRoom.get(key)
            rdy_message = {
                'type': "ready",
                'room': room
            }
            for m in record.members:
                user_info = m.split(';')
                message = simplejson.dumps(rdy_message)
                channel.send_message(user_info[0], message)
            self.response.out.write("Room %s Ready" % room)
class ForceLaunch(webapp2.RequestHandler):#--------------------------------------used to force a room ready
    def post(self):
        steamid64 = parse_id(users.get_current_user().nickname())
        if steamid64 == "76561197990677771":
            room = self.request.get('room')
            key = db.Key.from_path('GameRoom','default_gameroom','GameRoom', long(room))
            record = GameRoom.get(key)
            password = random.randrange(100,999,1)
            rdy_message = {
                'type': "launch",
                'ip': record.ip,
                'password': password,
                'room': room
            }
            for m in record.members:
                user_info = m.split(';')
                message = simplejson.dumps(rdy_message)
                channel.send_message(user_info[0], message)

            #make room inactive
            record.active = False
            record.put()

            """form_fields = {
                "ip"    :"199.21.112.10:27015",
                "rcon"  :"lalala",
                "command":"status"
            }
            form_data = urllib.urlencode(form_fields)
            url = "http://budkudyba.com/__pug/command.php"
            result = urlfetch.fetch(url = url,
                                    payload=form_data,
                                    method=urlfetch.POST,
                                    headers={'Content-Type': 'application/x-www-form-urlencoded'})
            self.response.out.write(result.content)"""

            self.response.out.write("Room %s Launched" % room)

class ReadyPlayer(webapp2.RequestHandler):#--------------------------------------used to force a room ready
    def post(self):
        steamid64 = parse_id(users.get_current_user().nickname())
        room = self.request.get('room')

        key = db.Key.from_path('GameRoom','default_gameroom','GameRoom', long(room))
        record = GameRoom.get(key)
        member_info = get_member(record.members,steamid64)#steamid64;classes;alias
        #member_info.append(";ready")
        ready_member_info = member_info[0] + ';' + member_info[1] + ';' + member_info[2] + ';' + "ready"
        record.members = remove_player(record.members,steamid64)
        record.members.append(db.Text(ready_member_info))
        record.put()

        if record.gstyle == "highlander(9v9)":
            players_needed_to_ready = 18
            for player in record.members:
                info = str(player).split(';')
                if len(info) == 4:
                    players_needed_to_ready -= 1
            #if players_needed_to_ready == 0:
            popup("76561197990677771", players_needed_to_ready)

class GameStateGet(webapp2.RequestHandler):#------------------------------------used to retrieve player state (if in room)
    def post(self):
        self.response.out.write('jimway')
        steamid64 = parse_id(users.get_current_user().nickname())

        q = Player.all()
        q.filter('steamid64', steamid64)
        for p in q:
            room = {
                'type': "gamestate",
                'room': p.name,
            }
            message = simplejson.dumps(room)
            #send message to requester
            channel.send_message(steamid64, message)

#-------------------------------------------------------------------------------
app = webapp2.WSGIApplication([
], debug=True)


#-------------------------------------------------------------------------------
#------------------------------------class end----------------------------------
def popup(steamid64,something):
    build_message = {
        'type': "popup",
        'message': something,
    }
    mess = simplejson.dumps(build_message)
    channel.send_message(steamid64, mess)







