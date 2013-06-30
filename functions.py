import datetime

import webapp2
from google.appengine.api import channel
from google.appengine.api import urlfetch
from google.appengine.api import users
from google.appengine.ext import db
#from django.utils import simplejson
import logging
import json
import re

"""takes steamID64 and retrieves player info from steam returning a json"""
def get_steam_user(steamid64):
    key = 'C32E0AC8282A2237AE9580042F7E3FAD'
    header = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key='
    url = header + key + '&steamids=' + steamid64
    urlfetch.set_default_fetch_deadline(10)
    try:
        result = urlfetch.fetch(url)
        if result.status_code == 200:
            json_result = json.loads(result.content)
            return json_result
        else:
            return False
    except:
        logging.error("urlfetch error")
        return False

"""takes a steam id 64 and returns an array of steam info"""
def steam_lookup(steamid64):
        #lookup steam info
        user_json = get_steam_user(steamid64)
        if user_json != False:
            for responsekey, responsevalue in user_json.iteritems():
                for playerkey, playervalue in responsevalue.iteritems():
                    player_info = playervalue
            return player_info
        else:
            return False

"""splits a string by / and returns the last element"""
def parse_id(str):
    urlnick = str.split('/')
    urlnick_email = urlnick[-1].split('@')
    return urlnick_email[0]

"""checks against a members list (steam64:time:classes,) returns true if found"""#2/20
def check_for_player(player_list,player_check):
    for player in player_list:
        steamid64 = str(player).split(';')
        if str(steamid64[0]) == str(player_check):
            return True
    return False

"""checks against a members list (steam64:time:classes,) returns classes if found"""
def player_classes(player_list,player_search):
    players_full = str(player_list).split(',')
    for player in players_full:
        info = str(player).split(';')#0 steamid64, 1 classes_picked
        if str(info[0]) == str(player_search):
            return info[1]
    return False

"""checks against a members list (steam64:time:classes,) returns member if found"""#2/20
def get_member(player_list,player_search):
    for player in player_list:
        info = str(player).split(';')#0 steamid64, 1 classes_picked
        if str(info[0]) == str(player_search):
            return info
    return False

"""checks against a members list (steam64:time:classes,) returns true if cap reached"""#2/20
def class_full_lobby(player_list, check_class, maximum_players):
    count = 0
    for player in player_list:
        info = str(player).split(';')#0 steamid64, 1 classes_picked
        if check_class > 8:#red
            check_class -= 9
            if str(info[1][9]) == "1":
                if str(info[1][check_class]) == "1":
                    count+=1
        else:#blue
            if str(info[1][9]) == "0":
                if str(info[1][check_class]) == "1":
                    count+=1

    if count >= maximum_players:
        return True
    else:
        return False

"""removes player from members list (steam64:time:classes,) returns new list """
def remove_player(player_list, player_check):
    new_list = []
    for player in player_list:
        steam64 = player.split(';')
        if str(steam64[0]) != str(player_check):
                new_list.append(player)
    return new_list

"""checks to see if required classes are met for highlander""" #UNFINISHED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def check_highlander(player_list):
    #check min players
    #check for 1's
    #check for double 2's
    #check for collisions
    if len(player_list) >= 1:#18
        #array prep
            #list of each class_list
        class_list = []
        for e in range(len(player_list)):
            player_info = player_list[e].split(';')
            class_list = [(x,[]) for x in range(len(player_info[1])) if player_info[1][x] == '1']
            return class_list
        """
        #check for 1's
        for y in range(len(class_list)):
            if len(class_list[y]) == 1:
                need_list = []
                need_list.append(y)
                return need_list
        #check for double's --------------------------WIP
        double_list = []
        for y in range(len(class_list)):
            if len(class_list[y]) == 2:
                double_list.append(class_list[y])
        if len(double_list) >= 2:
            group = double_list.pop()
            for z in range(len(group)):
                for x in range(len(double_list)):
                    for a in range(len(double_list[x])):
                        if group[z] == double_list[x][a]:
                            return "double"
                        """
    else:
        return "18"
"""checks to see if required classes are met for highlander"""
def check_number_added(player_list):
    players_added = 0
    for m in player_list:
        user_info = m.split(';')
        for pick in user_info[1]:
            if pick == '1':
                players_added += 1
                break
    return players_added

"""takes incoming chat message removes '<' and checks for urls"""
def parse_chat(message):
    ## find all <html> tags
    HTML_OPEN_REGEX = re.compile(r'''<''')
    if HTML_OPEN_REGEX.search(message) != None:
        return False

    wordlist = message.split(' ')
    compiled_message = ""
    for line in wordlist:
        #search for url elements http:// www. .com .org .net
        if line.find(r'http://') > -1:
            if line.find(r'.com') > -1:
                compiled_message += "<a href='"+line+"' target='_blank'>"+line+"</a>"
            else:
                compiled_message += "<a href='"+line+".com' target='_blank'>"+line+".com</a>"
        elif line.find(r'www.') > -1:
            if line.find(r'.com') > -1:
                compiled_message += "<a href='http://"+line+"' target='_blank'>"+line+"</a>"
            else:
                compiled_message += "<a href='http://"+line+".com' target='_blank'>"+line+".com</a>"
        elif line.find(r'.com') > -1:
            compiled_message += "<a href='http://"+line+"' target='_blank'>"+line+"</a>"
        elif line.find(r'.org') > -1:
            compiled_message += "<a href='http://"+line+"' target='_blank'>"+line+"</a>"
        elif line.find(r'.net') > -1:
            compiled_message += "<a href='http://"+line+"' target='_blank'>"+line+"</a>"
        else:
            compiled_message += line + " "
    return compiled_message












