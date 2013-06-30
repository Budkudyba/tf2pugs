import urllib2
import json

'''takes a string of 64 bit steam id's and returns json reponse'''

def get_steam_user(str):
    key = 'C32E0AC8282A2237AE9580042F7E3FAD'
    header = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key='
    url = header + key + '&steamids=' + str
    result = urlfetch.fetch(url)
    if result.status_code == 200:
        json_result = json.loads(result)
        return json_result
    else:
        return false