# db class that holds the database entities
# app made by Paul Kudyba
# December 2012
#

import webapp2
from google.appengine.ext import db

class GameRoom(db.Model):#------------------------------------------------------All info for a pug or gameroom
    number = db.IntegerProperty() #copy of the unique ID

    name = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add = True)
    leader = db.StringProperty()
    members = db.ListProperty(item_type=db.Text)
    banned = db.ListProperty(item_type=db.Text)
    whitelist = db.ListProperty(item_type=db.Text) #only allow members
    region = db.StringProperty()
    rcon = db.StringProperty()
    level = db.StringProperty() #map name
    ip = db.StringProperty()
    password = db.StringProperty()
    active = db.BooleanProperty(default = True)
    picking = db.BooleanProperty(default = False) #if room is closed to pick
    elo = db.IntegerProperty()
    gstyle = db.StringProperty() #6's or 9's maybe others to come
    mic = db.StringProperty() #if mic/mumble is reqired
    mumble = db.StringProperty() #mumble info
    #m_port = db.StringProperty()
    #m_pass = db.StringProperty()
    specAllow = db.StringProperty()
    tournement = db.StringProperty() #if this belongs to some tourney
    group_allow = db.ListProperty(item_type=db.Text)

def gameroom_key(gameroom_name=None):
    return db.Key.from_path('GameRoom',gameroom_name or 'default_gameroom')

class ActiveChannelMember(db.Model):#-------------------------------------------All active channels open
    steamid64 = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add = True)
    currrentRoom = db.IntegerProperty(default = None)
    personaname = db.StringProperty()
    chatcolor = db.StringProperty()

def ActiveChannel_key(ActiveChannelMember_name=None):
    return db.Key.from_path('ActiveChannelMember',ActiveChannelMember_name or 'default_ActiveChannelMember')

class Player(db.Model):#--------------------------------------------------------Player info
    #retrieved regularly from steam
    steamid64 = db.StringProperty()
    personaname = db.StringProperty()
    profileurl = db.StringProperty()
    avatarurl = db.StringProperty()
    #--------------------------------
    elo = db.IntegerProperty()
    pug_num = db.IntegerProperty()
    last_update = db.DateTimeProperty()
    playerpage = db.StringProperty()
    playerwins = db.IntegerProperty()
    playerloses = db.IntegerProperty()
    captainable = db.BooleanProperty(default = True)
    #---------------------------------
    kudos = db.ListProperty(item_type=db.Text)
    playermedals = db.StringProperty()
    chatcolor = db.StringProperty()
    server = db.ListProperty(item_type=db.Text) #previously used servers and settings
    #States--------------------------
    playerteams = db.ListProperty(item_type=db.Text)
    playerstandings = db.ListProperty(item_type=db.Text) #goodstanding, banned and date, warning, etc
    groups = db.ListProperty(item_type=db.Text)

def player_key(player_name=None):
    return db.Key.from_path('player',player_name or 'default_player')

class News(db.Model):#----------------------------------------------------------News for the main page
    content = db.StringProperty() #steamid64
    date = db.DateTimeProperty(auto_now_add = True)

def news_key(news_name=None):
    return db.Key.from_path('news',news_name or 'default_news')

class Server(db.Model):#--------------------------------------------------------Previous server info's
    owner = db.StringProperty() #steamid64
    ip = db.StringProperty()
    rcon = db.StringProperty()
    mumip = db.StringProperty() #contains port as well as password

def server_key(server_name=None):
    return db.Key.from_path('server',server_name or 'default_server')

class Team(db.Model):#----------------------------------------------------------Team Of Players
    captain = db.StringProperty()
    members = db.ListProperty(item_type=db.Text)
    fans = db.ListProperty(item_type=db.Text)
    picture = db.BlobProperty()
    discription = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add = True)

def team_key(team_name=None):
    return db.Key.from_path('team',team_name or 'default_team')













