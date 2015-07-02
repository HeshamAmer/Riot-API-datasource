"""
Created on Tue Jun 30 01:09:30 2015

@author: GedyHD
"""
import json;
import urllib2
import os.path
from pymongo import MongoClient;

#================================= end of includes ==================================================================

def getJSONReply(URL):
    response = urllib2.urlopen(URL);
    html = response.read()
    data = json.loads(html)
    return data;


def getUserInput():
    FileExists=os.path.isfile('RitoMongo.conf') 
    
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
        f = open('RitoMongo.conf','w')
        f.write('SummonerName='+SummonerName+'\nRegion='+Region+'\nAPI_Key='+Key) 
        f.close();
    return res;
        
    
#================================= Main =============================================================================
_InputFields= getUserInput();
SummonerName=_InputFields[0];
Region=_InputFields[1];
Key=_InputFields[2];

# Retrieving the SummonerID;
idURL = "https://na.api.pvp.net/api/lol/" + Region+ "/v1.4/summoner/by-name/" + SummonerName+ "?api_key=" + Key;
uID_data = getJSONReply(idURL);
SummonerID = uID_data[SummonerName.lower()]["id"];
print "The printed SummonerID from json is : " ,SummonerID;


# Connecting to mongoDB database
client = MongoClient();
db = client['RitoMongoDB'];
collection = db["SummonerID"];

print uID_data;
uID_data ['_id'] = uID_data['gedyhd']['id'];
#doc['_id'] = doc['objName']['id']
print "New UIDData is " , uID_data;
#collection.insert_one(doc)
    

entryID = collection.insert_one(uID_data).inserted_id;
