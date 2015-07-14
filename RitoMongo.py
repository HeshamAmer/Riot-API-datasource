"""
Created on Tue Jun 30 01:09:30 2015

@author: GedyHD
"""
import json;
import urllib2
import os.path
import re;
from pymongo import MongoClient;

#================================= end of includes ==================================================================

def getJSONReply(URL):
    response = urllib2.urlopen(URL);
    html = response.read();
    data = json.loads(html);
    return data;


def getUserInput():
    FileExists=os.path.isfile('RitoMongo.conf') ;
    res=[];
    if (FileExists):
        with open('RitoMongo.conf') as f:
            for line in f:
                res.append(line.rstrip('\n'));
                print line.rstrip('\n');
    elif (not FileExists):
        SummonerName= raw_input('Enter your Summoner name: ');
        Region  = (raw_input('Enter your region: ')).upper();
        Key = raw_input('Enter your API Key which you retrieved from Riot website: ');
        f = open('RitoMongo.conf','w');
        f.write(SummonerName+'\n'+Region+'\n'+Key);
        f.close();
    return res;


def getMatchHistory(SummonerID):

      mhURL="https://eune.api.pvp.net/api/lol/" + Region.lower() + "/v2.2/matchhistory/" + `SummonerID`+ "?api_key=" + Key;
      print mhURL;
      mh_data=getJSONReply(mhURL);
      print mh_data;
      
      return mh_data;
      
def getRecentHistory(SummonerID):
      rURL="https://eune.api.pvp.net/api/lol/" + Region.lower()+ "/v1.3/game/by-summoner/" + `SummonerID`+ "/recent?api_key=" + Key;
      print rURL;
      r_data=getJSONReply(rURL);
      print r_data;
      r_data['_id']=r_data['summonerId'];
      r_data.pop('summonerId');
      return r_data;
def ReformatJSON(SummonerName,Region,Key):
    idURL = "https://na.api.pvp.net/api/lol/" + Region+ "/v1.4/summoner/by-name/" + SummonerName+ "?api_key=" + Key;
    id_data = getJSONReply(idURL);
    idRes=id_data[SummonerName.lower()];
    idRes['_id'] = idRes['id'];
    idRes.pop('id');
    print idRes;
    return idRes,id_data;

#================================= Main =============================================================================
_InputFields= getUserInput();
SummonerName=_InputFields[0];
Region=_InputFields[1];
Key=_InputFields[2];
print "----------------------------------------------------------------------";
print "If you've inputted wrong data, please delete or modify RitoMongo.conf" ;
print "----------------------------------------------------------------------";
# Retrieving the SummonerID;
idURL,id_data=ReformatJSON(SummonerName,Region,Key);
SummonerID = id_data[SummonerName.lower()]["_id"];

mh_data=getMatchHistory(SummonerID);
rdata=getRecentHistory(SummonerID);
# Connecting to mongoDB database
client = MongoClient();
db = client['RitoMongoDB'];
SummonerID_Collection = db["SummonerID"];
MatchHistory_Collection = db["MatchHistory"];
RecentHistory_Collection = db["RecentHistory"];
#entryID = SummonerID_Collection.insert_one(idURL).inserted_id;
entryID = MatchHistory_Collection.insert_one(mh_data).inserted_id;
entryID = RecentHistory_Collection.insert_one(rdata).inserted_id;
client.close();