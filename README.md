# StatusBot

* Author:     Rui Pires
* Email:      rfn.pires15@gmail.com
* College:    FCT/UNL
* Degree:     MSc in Computer Science and Engineering
* Year:       4th

### About
Status
StatusBot is a CLI to monitor certain micro-services, currently it monitors wether or not github and bitbucket are live.

### Tech
* StatusBot was developed in python 3.7.2 and it uses only included modules
* The modules used are:
    * argparse  :   Parsing arguments
    * os        :   File operations
    * json      :   JSON parsing
    * urllib    :   API requests
    * re        :   String compares
    * shutil    :   File copying   
    * time      :   Sleep
    * sys       :   Exiting

### How to use

```sh
$ git clone git@github.com:piresrui/statusBot.git
$ cd src/
$ python3 status_bot.py <command> <options>
$ python3 status_bot.py poll --only=github
$ python3 status_bot.py help
```

### Functionalities and design

##### 1. Poll

* Usage example
```sh
$ python3 status_bot.py poll --only=github
```
    
* Poll retrieves the status from all configured services
    * Optional arguments:
        * -\-only        :   Tells poll to only probe provided services
        * -\-exclude    :   Tells poll to not probe provided services
    
* This function iterates over the data in the *config.json* file, makes a request to the specified API, stores the information in the local storage and prints the output for the user.

##### 2. Fetch

* Usage example
```sh
$ python3 status_bot.py fetch --rate=2 --only=github
```

* Fetch calls Poll every n seconds
    * The default n is 5 seconds, if none is provided
    * Optional arguments:
        * -\-rate        :   Integer n
        * -\-only        :   Tells fetch to only probe provided services
        * -\-exclude     :   Tells fetch to not probe provided services

* This function calls clears the terminal, calls Poll and sleeps for n seconds

##### 3. History

* Usage example
```sh
$ python3 status_bot.py history --only=github
```

* History outputs the local storage
    * Optional arguments:
        * -\-only        :   Outputs only the data of the provided services

* Data is stored in the *backup.json* file, it is created on launch if it does not exist.
* The format for this file is as follows:
```json
    {
        "service_1":
            [
                {
                    "date"      :   "%Y-%m-%dT%H:%M:%S.%fZ",
                    "status"    :   "up" || "down"
                }
            ],
        "service_2":
             [
                    {
                        "date"      :   "%Y-%m-%dT%H:%M:%S.%fZ",
                        "status"    :   "up" || "down"
                    }
                ]
    }
```

##### 4. Backup

* Usage example
```sh
$ python3 status_bot.py backup ~/Desktop/backup.csv --format=csv
```

* Backup stores the history data in a given location
    * Mandatory arguments:
        * <file_path>
    * Optional arguments:
        * -\-format      :   Saves history in given format
            * Default is JSON, other available formats are CSV and TXT 
        
* The txt format stores the data ordered by service, in the same format as Poll and Fetch
* The CSV format adheres to the conventional CSV format 
```csv
Service,Date,Status
```
* The default format is JSON and is explained in the [History](#history) section


##### 5. Restore

* Usage example
```sh
$ python3 status_bot.py restore ~/Desktop/backup.json --merge=true
```

* Restore takes a file and replaces the content in the local storage with it's content
    * Mandatory arguments:
        * <file_path>
    * Optional arguments:
        * -\-merge      :    Merge the content instead of replacing
         
* In this case, the only file format allowed is JSON, and the JSON must be in the same format as the one defined in the [History](#history) section, otherwise it will fail


##### 6. Services

* Usage example
```sh
$ python3 status_bot.py services
```

* Services outputs all the available services in the config.json* file

###### 7. Help

* Usage example
```sh
$ python3 status_bot.py help
```

* Help prints a hopefully helpful help message :)

### License
MIT
