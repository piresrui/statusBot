import argparse
from status import Status


class Arg_Controller():

    def __init__(self):
       self.__arger__ = self.set_up_arg_parser()

    def set_up_arg_parser(self):
        arger = argparse.ArgumentParser(description="StatusBot v1.0 by RuiPires")

        subparsers = arger.add_subparsers(dest="command")

        poll_parser = subparsers.add_parser("poll", help="Outputs state of services")
        poll_parser.add_argument("--only", dest="only")
        poll_parser.add_argument("--exclude", dest="exclude")

        fetch_parser = subparsers.add_parser("fetch", help="Polls services every n seconds")
        fetch_parser.add_argument("--rate", dest="rate")
        fetch_parser.add_argument("--only", dest="only")
        fetch_parser.add_argument("--exclude", dest="exclude")

        history_parser = subparsers.add_parser("history", help="Outputs history of poll/fetch requests")
        history_parser.add_argument("--only", dest="only")

        backup_parser = subparsers.add_parser("backup", help="Stores history in provided file")
        backup_parser.add_argument("file")
        backup_parser.add_argument("--format", dest="file_format")

        restore_parser = subparsers.add_parser("restore", help="Replaces history file with provided file")
        restore_parser.add_argument("file")
        restore_parser.add_argument("--merge", dest="merge")

        services_parser = subparsers.add_parser("services", help="Outputs available services")

        help_parser = subparsers.add_parser("help", help="Outputs help message")

        return arger 

    def run(self):

        opts = self.__arger__.parse_args()
        bot = Status()

        command = opts.command

        if command == "poll":
            is_exclude = True if opts.exclude else False
            is_include = True if opts.only else False

            if opts.exclude:
                options = opts.exclude
            elif opts.only:
                options = opts.only
            else:
                options = ""

            bot.poll(is_exclude, is_include, options)
        
        elif command == "fetch":
            is_exclude = True if opts.exclude else False
            is_include = True if opts.only else False

            if opts.exclude:
                options = opts.exclude
            elif opts.only:
                options = opts.only
            else:
                options = ""

            if opts.rate:
                bot.fetch(is_exclude, is_include, options, int(opts.rate))
            else:
                bot.fetch(is_exclude, is_include, options)

        elif command == "history":
            if opts.only:
                bot.history(True, opts.only)
            else:
                bot.history()

        elif command == "backup":
            option = opts.file_format if opts.file_format else "default"
            bot.backup(opts.file, option.lower())

        elif command == "services":
            bot.services()

        elif command == "restore":
            bot.restore(opts.file, True if opts.merge=="true" else False)

        elif command == "help":
            self.help()
        else:
            pass

    def help(self):
        print('''
                    poll                Outputs state of services
                                            Optional args:
                                                --only      Show only provided services                 
                                                            usage: poll --only=bitbucket
                                                --exclude   Omit provided services                      
                                                            usage: poll --exclude=github  

                    fetch               Calls poll every 5 seconds
                                            Optional agrs:
                                                --rate      Refresh every rate seconds                  
                                                            usage: fetch --rate=2
                                                --only      Show only provided services                 
                                                            usage: fetch --only=bitbucket
                                                --exclude   Omit provided services                      
                                                            usage: fetch --exclude=github  

                    history             Outputs all previous recorded poll/fetch calls
                                            Optional args:
                                                --only      Show only provided services                 
                                                            usage: history --only=github

                    backup <file_path>  Copies history to <file_path> in JSON format
                                            Optional args:
                                                --format    Store data in requested format (TXT or CSV) 
                                                            usage: backup <file_path> --format=csv

                    restore <file_path> Replaces provided JSON backup into history
                                            Optional args:
                                                --merge     Merges content instead of replacing it      
                                                            usage: restore <file_path> --merge=true

                    services            Outputs available services and endpoints

                    help                Outputs help message

                    status              Outputs stats for the services
                ''')