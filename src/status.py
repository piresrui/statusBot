import json
import os
import urllib.request
import re

class Status:
    fileName = "config.json"
    hdr = { 'User-Agent' : 'StatusBot v1.0' }
    data = {}

    def __init__(self):
        __location__ = os.path.realpath( os.path.join(os.getcwd(), os.path.dirname(__file__)))
        __file_location__ = os.path.join(__location__, self.fileName)
        
        if os.path.exists(__file_location__):
            with open(__file_location__) as f:
                try:
                    self.data = json.load(f)
                except:
                    print( "Error on file load" )
        else:
            print("No such file")

        
    def poll(self):
        for url in self.data["services"]:
            req = urllib.request.Request(url["api"], headers=self.hdr)
            response = urllib.request.urlopen(req)
            page = json.load(response)

            pat = re.compile('All Systems Operational')
            value = page["status"]["description"].rstrip()

            if pat.match(value):
                print(url["name"], "up")
            else:
                print(url["name"], "down")