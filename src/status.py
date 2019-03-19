import json
import os
import urllib.request
import re
from shutil import copyfile
import time
import sys
import parameters

class Status:
    def __init__(self):
        self.__load_data__()
        self.__create_backup__()


    ###########################################################
    ###    These functions control the bot funcionalities
    ############################################################

    ### param is_exclude : Boolean, defines if there exists --exclude option
    ### param is_include : Boolean, defines if there exists --only option
    ### param options    : String, contains optional arguments
    def poll(self, is_exclude=False, is_include=False, options=""):

        values = self.__exclude_include__( options )  #separate options into list

        for url in parameters.__data__["services"]:
            
            if (is_exclude and url["id"] in values) or (is_include and url["id"] not in values):      #exclude or include services in values based on exclude parameter
                continue

            # make get request to API
            try:
                req = urllib.request.Request( url["api"], headers=parameters.__hdr__ )
                response = urllib.request.urlopen( req )
            except:
                print("Failed probing", url["url"])
                continue
            
            page = json.load( response )

            pat = re.compile( parameters.__success_message__ )
            value = page["status"]["description"].rstrip()

            status = "up" if pat.match( value ) else "down"

            print( self.__output_message__( url["id"], page["page"]["updated_at"], status ) )
            self.__save_history__( url["id"], page["page"]["updated_at"], status )

    
    ### param is_exclude : Boolean, defines if there exists --exclude option
    ### param is_include : Boolean, defines if there exists --only option
    ### param options    : String, contains optional arguments
    ### param rate       : Integer, refresh rate in seconds
    def fetch(self, is_exclude, is_include, options, rate=5):
        while(True):
            self.__cls__()
            self.poll( is_exclude, is_include, options )
            time.sleep( rate )



    ### param file_name   : String, path of file
    ### param file_format : String, format to save in
    def backup(self, file_name, file_format):
        self.__backup_type__( file_name, file_format )


    ### param file_name : String, path of file
    ### param is_merge  : Boolean, defines if restore should be merge
    def restore(self, file_name, is_merge):

        if not file_name.endswith('.json'):
            print( "Wrong file extension" )
            sys.exit()

        if is_merge:
            self.__merge__( file_name )
        else:
            self.__check_if_format_valid__(file_name)
            self.__copy_file__( file_name, parameters.__backup_file_location__ )

    
    ### param include  : Boolean, defines if option --only is on
    ### param options  : String, contained values of --only option
    def history(self, include=False, options=""):

        values = self.__exclude_include__( options )  #separate options into list

        try:
            with open( parameters.__backup_file_location__ ) as f:
                if include:
                    for line in f:
                        for v in values:
                            if v in line:
                                print( line.rstrip() )
                else:
                    print( f.read() )
        except:
            print( "Failed opening file" )


    ### Prints services
    def services(self):
        for i, entry in enumerate( parameters.__data__["services"] ):
            output = '''[{}] - {}
                        url: {}
                        api: {}
                    '''.format( i, entry["name"], entry["url"], entry["api"] )
            print( output ) 

    
    
    
    ################################################
    #   Auxiliar functions
    #################################################


    

    # Saves history to local storage
    def __save_history__(self, id, date, status):
        try:
            with open(parameters.__backup_file_location__, 'r+') as f:

                backup_data = json.load( f )

                backup_data[id].append(
                                    {
                                    "date" : date,
                                    "status" : status
                                    } 
                                )

                self.__reset_file__( f, backup_data )
        except:
            print( "Failed opening file" )                

    # validates correct format
    def __check_if_format_valid__(self, file_name):
        try:
            with open( file_name, 'r+' ) as f:
                data = json.load( f )

                if not self.__validate_data__( data ):  #validate if file data is correct format
                    print( "Invalid data format" )
                    sys.exit()
        except:
            print( "Failed opening file" )

    # Merges two files
    def __merge__(self, file_name):
        try:
            with open( parameters.__backup_file_location__, 'r+' ) as f:
                with open( file_name, 'r+' ) as merge_file:

                        backup_data = json.load( f )
                        merge_data = json.load( merge_file )

                        if not self.__validate_data__( merge_data ):  #validate if file data is correct format
                            print( "Invalid data format" )
                            sys.exit()

                        for service, stats in merge_data.items():
                            for item in stats:
                                backup_data[service].append( item )

                        self.__reset_file__( f, backup_data )   
        except:
            print( "Failed opening file")


    # Backup files based on type    
    def __backup_type__(self, file_name, file_format):

        if file_format == "default":                                    # default format, simply copy file
            
            self.__copy_file__( parameters.__backup_file_location__, file_name )

        elif file_format == "csv" or file_format == "txt":                                      
            try:
                with open( file_name, "w+" ) as f:
                    with open( parameters.__backup_file_location__ ) as b_file:
                        backup_data = json.load( b_file )
                        for service, stats in backup_data.items():
                            for entry in stats:
                                if file_format == "csv":                                                    
                                    f.write( "{},{},{}\n".format( service, entry["date"], entry["status"] ) )           # csv format, separate content by comma's
                                else:
                                    f.write( self.__output_message__( service, entry["date"], entry["status"]) + "\n" )     # txt format, use poll format
            except:
                print( "Failed opening file" )

        else:
            print("Invalid format")


    # Prints message format for poll/fetch and writes to history file 
    def __output_message__(self, id, date, status):
        output = "[{}] {} - {}".format( id, date, status )
        return output
 
    # load config file into __data__ variable
    def __load_data__(self):
        if os.path.exists( parameters.__config_file_location__ ):
            with open( parameters.__config_file_location__ ) as f:
                try:
                    parameters.__data__ = json.load( f )
                except:
                    print( "Error on file load" )
        else:
            print("No such file")

    # Terminal window clear
    def __cls__(self):
        os.system( 'cls' if os.name=='nt' else 'clear' )

    # Splits values for options in to an array
    def __exclude_include__(self, options):
        values = options.split( "," )
        return values

    # validate is merge file data is in correct format
    def __validate_data__(self, data):

        services = []
        for service in parameters.__data__["services"]:
            services.append( service["id"] )

        
        for service, stats in data.items():
            if service not in services:
                return False
            for item in stats:
                for key, _ in item.items():
                    if key not in ["date", "status"]:
                        return False

        return True

    # created backup file
    def __create_backup__(self):
        if not os.path.exists( parameters.__backup_file_location__ ):
            with open( parameters.__backup_file_location__, "w+" ) as f:
                backup = {}
                for service in parameters.__data__["services"]:
                    backup[service["id"]] = []
                json.dump( backup, f, indent=4 )


    # Copies given file into backup file
    def __copy_file__(self, src, dest):
        try:
            copyfile( src, dest )
        except:
            print("Failed file copy")

    # resets file for writing
    def __reset_file__(self, f, backup_data):
        f.seek( 0 )
        json.dump( backup_data, f, indent=4 )
        f.truncate( )

        