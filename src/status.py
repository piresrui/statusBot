import json
import os
import urllib.request
import re
from shutil import copyfile
import time
import sys

class Status:
    __config_fileName__ = "config.json"
    __backup_fileName__ = "backup.json"
    __hdr__ = { 'User-Agent' : 'StatusBot v1.0' }
    __data__ = {}
    __location__ = os.path.realpath( os.path.join(os.getcwd(), os.path.dirname(__file__)))
    __config_file_location__ = os.path.join(__location__, __config_fileName__)
    __backup_file_location__ = os.path.join(__location__, __backup_fileName__)
    __date_format__ = "%Y-%m-%dT%H:%M:%S.%fZ"

    def __init__(self):
        self.load_data()
        self.create_backup()


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

            status = "up" if pat.match(value) else "down"

            print(self.output_message(url["id"], page["page"]["updated_at"], status))
            self.save_history(url["id"], page["page"]["updated_at"], status)
            
    def backup(self, file_name, file_format):
        self.backup_type(file_name, file_format)

    def restore(self, file_name, is_merge):

        if is_merge:
            self.merge(file_name)
        else:
            self.copy(file_name)

    def history(self, include=False, options=""):

        values = self.exclude_include(options)

        with open(self.__backup_file_location__) as f:
            if include:
                for line in f:
                    for v in values:
                        if v in line:
                            print(line.rstrip())
            else:
                print(f.read())


    def fetch(self, is_exclude, is_include, options, rate=5):
        while(True):
            self.cls()
            self.poll(is_exclude, is_include, options)
            time.sleep(int(rate))

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
        return output

    # Saves history to file based
    def save_history(self, id, date, status):
        with open(self.__backup_file_location__, 'r+') as f:
            try:

                backup_data = json.load(f)

                backup_data[id].append(
                                    {
                                    "date" : date,
                                    "status" : status
                                    } 
                                )

                f.seek(0)
                json.dump(backup_data, f, indent=4)
                f.truncate()
            
            except Exception as e:
                print( e )

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
    def copy(self, file_name):
        try:
            copyfile(file_name, self.__backup_file_location__)
        except:
            print("Failed file copy")


    def create_backup(self):
        if not os.path.exists(self.__backup_file_location__):
            with open(self.__backup_file_location__, "w+") as f:
                backup = {}
                for service in self.__data__["services"]:
                    backup[service["id"]] = []
                json.dump(backup, f, indent=4)

    # Merges two files
    def merge(self, file_name):

        with open(self.__backup_file_location__, 'r+') as f:
            with open(file_name, 'r+') as merge_file:
                try:

                    backup_data = json.load(f)
                    merge_data = json.load(merge_file)

                    if not self.validate_data(merge_data):  #validate if file data is correct format
                        print("Invalid data format")
                        sys.exit()

                    for service, stats in merge_data.items():
                        for item in stats:
                            backup_data[service].append(item)

                    f.seek(0)
                    json.dump(backup_data, f, indent=4)
                    f.truncate()
                
                except Exception as e:
                    print( e )

    def backup_type(self, file_name, file_format):

        if file_format == "default":
            copyfile(self.__backup_file_location__, file_name)

        elif file_format == "csv":

            with open(file_name, "w+") as f:
                with open(self.__backup_file_location__) as b_file:
                    backup_data = json.load(b_file)
                    for service, stats in backup_data.items():
                        for entry in stats:
                            f.write(service + "," + entry["date"] + "," + entry["status"] + "\n")

        elif file_format == "txt":

            with open(file_name, "w+") as f:
                with open(self.__backup_file_location__) as b_file:
                    backup_data = json.load(b_file)
                    for service, stats in backup_data.items():
                        for entry in stats:
                           f.write(self.output_message(service, entry["date"], entry["status"]) + "\n")
        else:
            print("Invalid format.")

    def validate_data(self, data):

        services = []
        for service in self.__data__["services"]:
            services.append(service["id"])

        
        for service, stats in data.items():
            if service not in services:
                return False
            for item in stats:
                for key, _ in item.items():
                    if key not in ["date", "status"]:
                        return False
        return True





        