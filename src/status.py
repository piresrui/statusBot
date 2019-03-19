import json
import os
import urllib.request
import re
from shutil import copyfile
import time

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


    ###
    ###    These functions control the bot funcionalities
    ###

    def poll(self, is_exclude=False, is_include=False, options=""):

        values = self.exclude_include(options)

        for url in self.__data__["services"]:
            
            if (is_exclude and url["id"] in values) or (is_include and url["id"] not in values):      #exclude or include services in values based on exclude parameter
                continue

            req = urllib.request.Request(url["api"], headers=self.__hdr__)
            response = urllib.request.urlopen(req)
            page = json.load(response)

            pat = re.compile('All Systems Operational')
            value = page["status"]["description"].rstrip()

            self.output_message(url["id"], page["page"]["updated_at"], "up" if pat.match(value) else "down")
            
    def backup(self, file):
        try:
            copyfile(self.__backup_file_location__, file)
        except:
            print("Failed file copy")

    def restore(self, file, is_merge):

        if is_merge:
            merge(file)
        else:
            copy(file)

    def history(self, include=False, options=""):

        values = self.exclude_include(options)

        with open(self.__backup_file_location__) as f:

            if include:
                for line in f:
                    for v in values:
                        if v in line:
                            print(line)
            else:
                print(f.read())


    def fetch(self, rate=5):
        while(True):
            self.cls()
            self.poll()
            time.sleep(rate)

    def services(self):
        for i, entry in enumerate(self.__data__["services"]):
            output = '''[{}] - {}
                        url: {}
                        api: {}
                    '''.format(i, entry["name"], entry["url"], entry["api"])
            print(output)

    ###
    #   Auxiliar functions
    ###


    # Prints message format for poll/fetch and writes to history file 
    def output_message(self, id, date, status):
        output = "[{}] {} - {}".format(id, date, status)
        print(output)

        with open(self.__backup_file_location__, "a+") as f:
            try:
                f.write(output + "\n")
            except:
                print( "Error on file write" )


    # Stores JSON data in config file into data variable
    def load_data(self):
        if os.path.exists(self.__config_file_location__):
            with open(self.__config_file_location__) as f:
                try:
                    self.__data__ = json.load(f)
                except:
                    print( "Error on file load" )
        else:
            print("No such file")

    # Terminal window clear
    def cls(self):
        os.system('cls' if os.name=='nt' else 'clear')

    # Splits values for options in to an array
    def exclude_include(self, options):
        values = options.split(",")
        return values

    # Copies given file into backup file
    def copy(self, file):
        try:
            copyfile(file, self.__backup_file_location__)
        except:
            print("Failed file copy")

    # Merges two files
    def merge(self, file):
        file_names = [file, __backup_file_location__]


        #copies both files into a new one line by line, better for bigger files
        with open(os.path.join(__location__, "tmp.txt")) as f:
            for file in file_names:
                with open(file) as in_file:
                    for line in in_file:
                        f.write(line)

        os.remove( __backup_file_location__ )
        os.rename( os.path.join(__location__, "tmp.txt"), __backup_file_location__ )

        