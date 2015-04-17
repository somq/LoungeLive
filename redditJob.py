#!flask/bin/python

import os
try: 
  import simplejson as json
except:
  import json
import requests
import re
from flask import Flask
from flask import jsonify
from random import randint
from date import *
from dbqueries import *

app = Flask(__name__)

#clear = lambda: os.system('clear')
#clear()
debug = False
# debug = True
def findVsType(stringToFindIn):
    vsArray = [' vs. ', ' Vs. ', ' vs ', ' Vs ' ]
    for i in vsArray:
        if i in stringToFindIn:
            return i
        
#    keywords = [ "Time", "Date", "Tournament/League", "LAN/Online", "Maps" ]
class parseRedditText:
    """       
        ** NOTE ** Redondant writing but I'm new to python, could eventually try this snippet below, but for lisibility im leaving it like this for now...
        def bindFunction1(name):
           def func1(*args):
               for arg in args:
                   print arg
               return 42 # ...
           func1.__name__ = name
           return func1
    """
    
    def __init__(self, redditText, keyword):
        self.toRegexParse = redditText
        self.regexAll = '(?<=' + keyword + '\*\*: )(.*)'
        self.regexFeeds = '(?<=\[' + keyword + '\]\()(.*?)(?=\))'
        self.regexPlayerListTeamA = '[\n]---------------[\n][\n]([^\n]*)(?<=[a-zA-Z0-9]\*\*: )(.*)'
        self.regexPlayerListTeamB = '[\n]--------------------------------------[\n][\n]([^\n]*)(?<=[a-zA-Z0-9]\*\*: )(.*)'
        self.regexTeamA1 = '[\n]---------------[\n][\n]([^\n]*)'
        self.regexTeamB2 = '[\n]--------------------------------------[\n][\n]([^\n]*)'

        
    def groupReturn(self, intPos):
        if self.r :
            result = self.r.group(intPos)
            return result
        else:
            return 'Not_found'
        
    def all(self):
        self.r = re.search(self.regexAll, self.toRegexParse)
        result = self.groupReturn(0)
        return result
        
    def feeds(self):
        self.r = re.search(self.regexFeeds, self.toRegexParse)
        result = self.groupReturn(0)
        return result
 
    def teamA(self):
        self.r = re.search(self.regexPlayerListTeamA, self.toRegexParse)
        result = self.groupReturn(2)
        return result
 
    def teamB(self):
        self.r = re.search(self.regexPlayerListTeamB, self.toRegexParse)
        result = self.groupReturn(2)
        return result

def redditJob():
    print 'redditJob'
    currentFeedSource = "reddit"
    url = "https://www.reddit.com/r/csgobetting/search.json?q=flair:match&restrict_sr=on&sort=new"
    user_agent = {'User-agent': 'Mozilla/5.0'}
    response = requests.get(url, headers = user_agent)

    responseJson = response.json()
    #print response.status_code
    #~ print response.text
    # Build REDDIT properties object
    feedPropsList = []

    for i in responseJson['data']['children']:
        # print i['data']['id']
        # print i
        # The 2 objs containing datas
        feedMatchTitle = i['data']['title']
        feedDatasText = i['data']['selftext']
        feedDatasTextHTML = i['data']['selftext_html']
        redditText = feedDatasText
        # print feedMatchTitle + '\n'
        # print feedDatasText

    # From feedMatchTitle:
        #Splitted sentence, eg. A vs. B BO3 06.02.15  21:00 CET CEVO
        feedMatchTitleSplitted = feedMatchTitle.split(' | ');
        # try any individual split to avoid missing vars cause of OP formating mistakes.
        try:
                fMTS0 = feedMatchTitleSplitted[0]
        except: fMTS0 = 'Not found'
        try:
                fMTS1 = feedMatchTitleSplitted[1]
        except: fMTS1 = 'Not found'
        try:
                fMTS2 = feedMatchTitleSplitted[2]
        except: fMTS2 = 'Not found'
        try:
                fMTS3 = feedMatchTitleSplitted[3]
        except: fMTS3 = 'Not found'
        
        # Match title, eg. Fnatic vs. EnvyUs
        feedMatchname = fMTS0
        #Extract TeamA & TeamB from feedMatchname
        vsType = findVsType(fMTS0)
        if 'vsType' in locals():
            feedTeams = fMTS0.split(vsType)
            feedTeamA = feedTeams[0]
            feedTeamB = feedTeams[1]
        else:
            feedTeamA = ""; feedTeamB = "";
        #FeedDate 06.02.15  21:00

        feedDate = fMTS2 + ' ' + fMTS3 
        
        #TimeZone
        try:
            timeZone = fMTS3.rsplit(None, 1)[-1]
        except:
            timeZone = 'undefined'
        try:
            feedHour = fMTS3.rsplit(None, 1)[-2]
        except:
            feedHour = 'undefined'


        #ISO 8601 formated date
        feedDateFormated = formatDate(fMTS2, feedHour, timeZone)

    # From feedDatasText$
        feedLinks = parseRedditText(redditText, 'Links').all()
        feedUrlReddit = i['data']['url']
        feedUrlHltv = parseRedditText(redditText, 'HLTV').feeds()
        feedUrlCsgl = parseRedditText(redditText, 'CSGL').feeds()
        feedCup = parseRedditText(redditText, "Tournament/League").all()
        try:
            feedBestOf = int(fMTS1.replace('BO', '', 2))
        except: 
            feedBestOf = 'Not found'
        feedLanOnline = parseRedditText(redditText, "LAN/Online").all()
        feedMaps = parseRedditText(redditText, "Maps").all()

        #Teams Players
        #Method #1: regexp **TEAMNAME**
        playersListTeamA = parseRedditText(redditText, '').teamA()
        playersListTeamB = parseRedditText(redditText, '').teamB()
        playersListTeamAArray = playersListTeamA.replace(","," ").encode("utf-8").split()
        playersListTeamBArray = playersListTeamB.replace(","," ").encode("utf-8").split()
        #method #2: regexp ---+newlines
    #    [\n]--------------------------------------[\n][\n]([^\n]*)
    #    [\n]---------------[\n][\n]([^\n]*)
        if debug == True:
            print '\n' +'**00000***' + '\n'
            print feedMatchTitle + '\n'
            print feedTeamA + '\n'
            print feedTeamB + '\n'
            print playersListTeamA + '\n'
            print playersListTeamB + '\n'
            print feedLinks + '\n'
            print feedUrlReddit  + '\n'
            print feedUrlHltv + '\n'
            print feedUrlCsgl + '\n'
            print feedCup + '\n'
            print str(feedBestOf) + '\n'
            print feedLanOnline + '\n'
            print '\n' +'***END**' + '\n'

        feedPropsObjToPushToList = {
                        "rawData":{
                        "selftext":feedDatasText,
                        "selftextHTML":feedDatasTextHTML,
                        "selftextTitle":feedMatchTitle
                        },
                        "feedMatchname" : feedMatchname,
                        "csglliveMatchname" : "",
                        "feedUrls":{
                            "reddit":feedUrlReddit,
                            "hltv":feedUrlHltv,
                            "csgl":feedUrlCsgl
                        },
                        "feedDate": feedDate,
                        "teamA":feedTeamA,
                        "teamB":feedTeamB,
                        "feedCup": feedCup,
                        "feedLanOnline": feedLanOnline,
                        "bestOf" : feedBestOf,
                        "maps":feedMaps,
                        "odds":{
                            "oddTeamA":"",
                            "oddsTeamB":""
                        },
                        "playersList":{
                            "teamA" : playersListTeamAArray,
                            "teamB" : playersListTeamBArray
                    }
            }
        # print 'loopdone'
    #    print json.dumps(feedPropsObjToPushToList)

        feedPropsList.append(feedPropsObjToPushToList)

    #~ #Build Main Json Object
    dateNowx =  dateNow()
    redditDatas = {"feedSource" : currentFeedSource, "date" : dateNowx,  "feedProperties": feedPropsList}
    datas = { "datas" : redditDatas}
    print 'reddit finished'

    def storeJobResult(datas):
        dbq = dbQueries()
        dbq.db_insert('reddit', datas)
        dbq.db_close()
        print 'reddit inserted'

    # datas = redditJob()
    datas_to_store = json.dumps(datas).replace("'", r"''")
    # print datas_to_store
    storeJobResult(datas_to_store)
    return datas

    # print json.dumps(a)
#
# redditJob()