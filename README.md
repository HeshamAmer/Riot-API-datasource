# Riot-API-datasource
This a python script that gets you started with Riot league of legends API to interface with MongoDB
This script requires that you have a mongodb instance running at your local host (127.0.0.1) 
The script will take your Summoner Name, Region and your API key.
The script will help you get started by creating a database "RitoMongoDB" and collection "SummonerID",
which will have your current SummonerID parsed in a manner of 
{
    "_id" : 24754800,
    "profileIconId" : 529,
    "name" : "GedyHD",
    "summonerLevel" : 30,
    "revisionDate" : NumberLong(1436402086000)
}
This parsing was edited from the original JSON response replied from the riot API, I believe this could be easier to get you started

