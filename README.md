# StatusBot

### DISCLAIMER. **MUST READ**
This is currenly being re-written because it was an old project I used to learn python. As such, things were working but not ideal.
The documentation bellow is for the original version (tag v1.0).
When I'm done with re-writting, I'll update it.
Tag v1.0 is working, everything until the next release is BROKEN since it is a WIP.

### About
StatusBot is a CLI to monitor certain micro-services, currently it monitors wether or not github and bitbucket are live.

### Libraries

statusBot makes use of requests and pyyaml.

### How to use

```sh
$ git clone git@github.com:piresrui/statusBot.git
$ cd statusBot/
$ cd src/
$ pip install -r requirements.txt
$ ./status_bot.py <command> <options>
$ ./status_bot.py poll --only=github
$ ./status_bot.py help
```

### Functionalities and design

##### 1. Poll

* Usage example
```sh
$ ./status_bot.py poll --only github
```
    
* Poll retrieves the status from all configured services
    * Optional arguments:
        * -\-only        :   Tells poll to only probe provided services
        * -\-exclude    :   Tells poll to not probe provided services
    
* This function iterates over the data in the *config.json* file, makes a request to the specified API, stores the information in the local storage and prints the output for the user.

##### 2. Fetch

* Usage example
```sh
$ ./status_bot.py fetch --rate 2 --only github
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
$ ./status_bot.py history --only github
```

* History outputs the local storage
    * Optional arguments:
        * -\-only        :   Outputs only the data of the provided services

* Data is stored in the *backup.csv* file, it is created on launch if it does not exist.
* The format for this file is as follows:
```csv
   service,date,state
```
* Service is the id of the service
* Date: "%Y-%m-%dT%H:%M:%S.%fZ"
* State: "up || down"

##### 4. Backup

* Usage example
```sh
$ ./status_bot.py backup ~/Desktop/backup.json --format=json
```

* Backup stores the history data in a given location
    * Mandatory arguments:
        * <file_path>
    * Optional arguments:
        * -\-format      :   Saves history in given format
            * Default is CSV, other available formats are JSON and TXT 
        
* The txt format stores the data ordered by service, in the same format as Poll and Fetch
* The JSON format is as follows:
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
* The default format is CSV and is explained in the [History](#history) section


##### 5. Restore

* Usage example
```sh
$ ./status_bot.py restore ~/Desktop/backup.json --merge
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
$ ./status_bot.py services
```

* Services outputs all the available services in the config.json* file

###### 7. Help

* Usage example
```sh
$ ./status_bot.py help
```

* Help prints a hopefully helpful help message :)

### License
MIT
