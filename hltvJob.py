#!flask/bin/python

import os
try: 
  import simplejson as json
except:
  import json
import requests
from flask import Flask
from flask import jsonify
from random import randint
from dbqueries import *
from date import *

app = Flask(__name__)

def hltvJob():
    print 'hltvJob'
    currentFeedSource = "hltv"
    randNumber = str(randint(1002,9999))
    url = "http://ajax.googleapis.com/ajax/services/feed/load?v=2.0&q=http://www.hltv.org/hltv.rss.php?pri=15&num=50&rand="+randNumber
    response = requests.get(url)
    responseParsed = json.loads(response.text)

    hltvRssArray = responseParsed['responseData']['feed']

    # Build HLTV properties object
    feedPropsList = []

    for i in hltvRssArray['entries']:
        feedMatchname = i['title']
        feedUrl = i['link']
        feedDate = i['publishedDate']
        feedCup = i['content']
        feedPropsObjToPushToList = {
                        "feedMatchname" : feedMatchname,
                        "csglliveMatchname" : "",
                        "feedUrl" : feedUrl,
                        "feedDate": feedDate,
                        "teamA":"",
                        "teamB":"",
                        "feedCup": feedCup,
                        "feedLanOnline": "",
                        "maps":[],
                        "odds":{
                            "oddTeamA":"",
                            "oddsTeamB":""
                        },
                        "playersList":{
                            "teamA":[],
                            "teamB":[]
                    }
            }
        feedPropsList.append(feedPropsObjToPushToList)

    #Build Main Json Object
    dateNowx =  dateNow()
    hltvDatas = {"feedSource" : currentFeedSource, "date" : dateNowx,  "feedProperties": feedPropsList}
    datas = { "datas" : hltvDatas}
    print 'hltv finished'

    def storeJobResult(datas):
        dbq = dbQueries()
        dbq.db_insert('hltv', datas)
        dbq.db_close()
        print 'hltv inserted'

    # datas = hltvJob()
    datas_to_store = json.dumps(datas).replace("'", r"''")
    storeJobResult(datas_to_store)

    return datas


    # print json.dumps(a)

# hltvJob()
