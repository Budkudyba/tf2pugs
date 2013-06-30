# main class for handling login and the main page
# app made by Paul Kudyba
# December 2012
# --clear_datastore

import datetime
import logging

import webapp2
from google.appengine.api import urlfetch
import urllib
from google.appengine.api import channel
from google.appengine.api import users
from google.appengine.ext import db
from django.utils import simplejson
#import simplejson as json

#local imports
from model_db import *
from functions import *
from room import *
from team import *
from player import *
from admin import *

update_after = 59 #in minutes

class MainHandler(webapp2.RequestHandler):#------------------------------------- Handles the Main Room
    def get(self):
        user = users.get_current_user()
        steam_server = False #holds true if able to retrieve info from steam
        if user:
            steamid64 = parse_id(users.get_current_user().nickname())
            newPlayer = True
            now = datetime.datetime.now()

            q = Player.all()
            q.filter('steamid64', steamid64)
            for p in q:
                newPlayer = False
                #check last updated (1 hours is the timeout)
                if now > p.last_update + datetime.timedelta(minutes=update_after):
                    player_info = steam_lookup(steamid64)
                    steam_server = True
                else:
                    steam_server = False
                    player_info = False
                #check if new player info from steam
                if player_info != False:
                    player_alias = player_info[0]['personaname']
                else:
                    player_alias = p.personaname
                    steam_server = False

                if steam_server:
                    p.personaname = player_info[0]['personaname']
                    p.profileurl = player_info[0]['profileurl']
                    p.avatarurl = player_info[0]['avatar']
                    p.last_update = now
                    p.put()

            if newPlayer:
                player_info = steam_lookup(steamid64)
                if player_info != False:
                    player_alias = player_info[0]['personaname']
                    steam_server = True
                else:
                    player_alias = steamid64
                    steam_server = False

                player = Player(parent = player_key(steamid64))
                player.steamid64 = steamid64
                if steam_server:
                    player.personaname = player_info[0]['personaname']
                    player.profileurl = player_info[0]['profileurl']
                    player.avatarurl = player_info[0]['avatar']
                    player.last_update = now
                else:
                    player.personaname = player_alias
                    player.avatarurl = "/images/unknown.jpg"
                    player.last_update = now - datetime.timedelta(minutes=update_after)
                player.chatcolor = "color:#000000"
                player.elo = 1400
                player.pug_num = 0
                player.playerwins = 0
                player.playerloses = 0
                player.playerpage = "" #needs to be made
                player.playermedals = "newb"
                player.put()

            token = channel.create_channel(steamid64,720)
            #token = channel.create_channel(steamid64 + str(now))
            version = os.environ['CURRENT_VERSION_ID']
            logout_url = users.create_logout_url(self.request.uri)

            news = News.all()
            news.order('-date')
            currentNews = news.fetch(limit=3)

            gameroom = GameRoom.all()
            gameroom.filter('active', True)
            gameroom.filter('picking', False)

            template_values = {
            'token': token,
            'user' : steamid64,
            'version' : version,
            'logout_url': logout_url,
            'nickname': player_alias,
            'steam_server': steam_server,
            'news': currentNews,
            'gameroom': gameroom,
            }
            directory = os.path.dirname(__file__)
            path = os.path.join(directory, os.path.join('templates', 'main.html'))
            self.response.out.write(template.render(path, template_values, debug=True))

            ## how to post to a url example-------------------------------------------------------
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

        else:
            self.redirect('/login')

class LoginHandler(webapp2.RequestHandler):#------------------------------------Handles the login page
    def get(self):
        user = users.get_current_user()
        if user:  # signed in already
            self.redirect('/')
        else:
            login_link = users.create_login_url(federated_identity='http://steamcommunity.com/openid')
            login_image = "/images/sits_large_noborder.png"
            login_background = "/images/background.jpg"
            version = os.environ['CURRENT_VERSION_ID']
            home = self.request.host_url
            faq = home + "/faq"
            #self.response.out.write(faq)

            template_values = {
                'login_url': login_link,
                'login_img': login_image,
                'login_background': login_background,
                'version' : version,
                'faq_link': faq,
                }
            directory = os.path.dirname(__file__)
            path = os.path.join(directory, os.path.join('templates', 'login.html'))
            self.response.out.write(template.render(path, template_values, debug=True))

class FAQHandler(webapp2.RequestHandler):#------------------------------------- Handles the the FAQ Page
    def get(self):
        home = self.request.host_url
        login_background = "/images/background.jpg"
        template_values = {
            'login_background': login_background,
            'home_link': home,
        }
        directory = os.path.dirname(__file__)
        path = os.path.join(directory, os.path.join('templates', 'faq.html'))
        self.response.out.write(template.render(path, template_values, debug=True))

class NewsPost(webapp2.RequestHandler):#------------------------------------- Handles the Main Room
    def post(self):
        message = self.request.get('message')
        user = users.get_current_user()
        if user:
            steamid64 = parse_id(users.get_current_user().nickname())
            if steamid64 == "76561197990677771":
                newscreate_name = self.request.get('newscreate_name')
                news = News(parent = news_key(newscreate_name))
                news.content = message
                news.date = datetime.datetime.now()
                news.put()
                self.response.out.write("News Posted")
            else:
                self.response.out.write("You are not a regestered admin D:")
        else:
            self.redirect('/login')

class ChatPost(webapp2.RequestHandler):#------------------------------------Handles chat post
    def post(self):
        inbound_message = parse_chat(self.request.get('message'))
        room = self.request.get('room')
        sender = self.request.get('sender')

        if inbound_message==False:
            inbound_message = "We apologize but you cannot use the character '<' our creator was lazy."
            response = {
                    'type': "chat",
                    'room': room,
                    'sender': "SYSTEM MESSAGE",
                    'message': inbound_message,
                }
            message = simplejson.dumps(response)
            channel.send_message(sender, message)
        else:
            q = ActiveChannelMember.all()
            member_count = 0
            for member in q:#count the number of active members
                member_count+=1

            q.filter('steamid64', sender)
            for p in q:
                alias = p.personaname
                color = p.chatcolor

            response = {
                    'type': "chat",
                    'room': room,
                    'sender': alias,
                    'message': inbound_message,
                    'member_count': member_count,
                    'color': color,
                }
            message = simplejson.dumps(response)
            for r in q:
                channel.send_message(r.steamid64, message)
        self.redirect('/')

class ChannelConnect(webapp2.RequestHandler):#----------------------------------Handles when a client connects and tracks them in db
    def post(self):
        steamid64 = self.request.get('from')
        #add user to active channel db
        ActiveChannelMember_name = self.request.get('ActiveChannelMember_name')
        channel_member = ActiveChannelMember(parent = ActiveChannel_key(ActiveChannelMember_name))
        channel_member.steamid64 = steamid64
        q = Player.all()
        q.filter('steamid64', steamid64)
        for p in q:
            alias = p.personaname
            color = p.chatcolor
        channel_member.personaname = alias
        channel_member.chatcolor = color
        channel_member.put()

class ChannelDisconnect(webapp2.RequestHandler):#-------------------------------Handles when a client disconnects and removes them in db
    def post(self):
        steamid64 = self.request.get('from')
        #remove user from active channel db

        q = ActiveChannelMember.all()
        q.filter('steamid64', steamid64)
        for member in q:
            roomid = member.currrentRoom
            member.delete()
        if roomid != None:
            #get current room and remove member
            key = db.Key.from_path('GameRoom','default_gameroom','GameRoom', roomid)
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

class YourHandler(webapp2.RequestHandler):#-------------------------------------Handles errors
    def handle_exception(self, exception, mode):
        # run the default exception handling
        webapp.RequestHandler.handle_exception(self,exception, mode)
        # note the error in the log
        logging.error("Something bad happend: %s" % str(exception))
        # tell your users a friendly message
        self.response.out.write("Sorry lovely users, something went wrong")


#-------------------------------------------------------------------------------
app = webapp2.WSGIApplication([
    #-----------------------------------#page handlers
    ('/', MainHandler),
    ('/login', LoginHandler),
    ('/a', AdminHandler),
    ('/faq', FAQHandler),
    #-----------------------------------#Main post request handlers
    ('/_ah/channel/connected/', ChannelConnect),
    ('/_ah/channel/disconnected/', ChannelDisconnect),
    ('/chat', ChatPost),
    ('/newspost', NewsPost),
    ('/create_team', CreateTeam),
    #-----------------------------------#room.py
    ('/getroom', GameRoomGet),
    ('/create', GameRoomCreate),
    ('/enter', GameRoomEnter),
    ('/leave', GameRoomLeave),
    ('/toggle_class', ToggleClass),
    ('/disband', GameRoomDisband),
    ('/forceReady', ForceReady),
    ('/ready', ReadyPlayer),

    #----------------------------------#team.py
    ('/t/(.*)', TeamPage),
    #----------------------------------#player.py
    ('/p/(.*)', PlayerPage),
], debug=True)
#-------------------------------------------------------------------------------
#------------------------------------app end------------------------------------







