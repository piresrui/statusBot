import urllib.request
import json
import os
import argparse
import re

fileName = "config.json"
hdr = { 'User-Agent' : 'StatusBot v1.0' }


def stuff():
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

        pat = re.compile('All Systems Operational')
        value = page["status"]["description"].rstrip()

        if pat.match(value):
            print("Bitbucket up")
        else:
            print("Bitbucket down")


def commands():

    parser = argparse.ArgumentParser(description='Status Bot')
    parser.add_argument("poll", help="Outputs status of supported services") 

    args = parser.parse_args()

    if args.poll:
        stuff()

        

commands()

   


