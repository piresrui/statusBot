import json
import os
import urllib.request
import re
from shutil import copyfile

class Status:
    __config_fileName__ = "config.json"
    __backup_fileName__ = "backup.txt"
    __hdr__ = { 'User-Agent' : 'StatusBot v1.0' }
    __data__ = {}
    __location__ = os.path.realpath( os.path.join(os.getcwd(), os.path.dirname(__file__)))
    __config_file_location__ = os.path.join(__location__, __config_fileName__)
    __backup_file_location__ = os.path.join(__location__, __backup_fileName__)

    def __init__(self):
        self.load_data()


    def poll(self):
        for url in self.__data__["services"]:
            req = urllib.request.Request(url["api"], headers=self.__hdr__)
            response = urllib.request.urlopen(req)
            page = json.load(response)

            pat = re.compile('All Systems Operational')
            value = page["status"]["description"].rstrip()

            if pat.match(value):
                self.output_message(url["id"], page["page"]["updated_at"], "up")
            else:
                self.output_message(url["id"], page["page"]["updated_at"], "down")

    def backup(self, file):
        try:
            copyfile(self.__backup_file_location__, file)
        except:
            print("Failed file copy")

    def history(self):
        with open(self.__backup_file_location__) as f:
            print(f.read())


    def output_message(self, id, date, status):
        output = "[{}] {} - {}".format(id, date, status)
        print(output)

        with open(self.__backup_file_location__, "a+") as f:
            try:
                f.write(output + "\n")
            except:
                print( "Error on file write" )


    def load_data(self):
        if os.path.exists(self.__config_file_location__):
            with open(self.__config_file_location__) as f:
                try:
                    self.__data__ = json.load(f)
                except:
                    print( "Error on file load" )
        else:
            print("No such file")
