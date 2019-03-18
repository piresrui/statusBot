import urllib.request
import json
import os

fileName = "config.json"
hdr = { 'User-Agent' : 'StatusBot v1.0' }


if os.path.exists(fileName):
    with open('config.json') as f:
        try:
           data = json.load(f)
        except:
           print( "Error on file load" )



for url in data["services"]:
    req = urllib.request.Request(url["api"], headers=hdr)
    response = urllib.request.urlopen(req)
    page = json.load(response)

    print( page["status"])
    

   


