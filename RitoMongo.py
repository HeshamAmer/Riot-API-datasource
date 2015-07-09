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
        Key = raw_input('Enter your API Key which you retrieved from Rito website: ');
        f = open('RitoMongo.conf','w');
        f.write(SummonerName+'\n'+Region+'\n'+Key);
        f.close();
    return res;
        
def ReformatJSON(SummonerName,Region,Key):
    idURL = "https://na.api.pvp.net/api/lol/" + Region+ "/v1.4/summoner/by-name/" + SummonerName+ "?api_key=" + Key;
    uID_data = getJSONReply(idURL);
    idURL=uID_data[SummonerName.lower()];
    idURL['_id'] = idURL['id'];
    idURL.pop('id');
    print idURL;
    return idURL,uID_data;

#================================= Main =============================================================================
_InputFields= getUserInput();
SummonerName=_InputFields[0];
Region=_InputFields[1];
Key=_InputFields[2];
print "----------------------------------------------------------------------";
print "If you've inputted wrong data, please delete or modify RitoMongo.conf" ;
print "----------------------------------------------------------------------";
# Retrieving the SummonerID;
idURL,uID_data=ReformatJSON(SummonerName,Region,Key);
SummonerID = uID_data[SummonerName.lower()]["_id"];
print "The printed SummonerID from json is : " ,SummonerID;

# Connecting to mongoDB database
client = MongoClient();
db = client['RitoMongoDB'];
collection = db["SummonerID"];
entryID = collection.insert_one(idURL).inserted_id;
client.close();