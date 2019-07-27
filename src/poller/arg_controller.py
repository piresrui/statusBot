import argparse
from poller import poll_helper

class ArgController:

    def __init__(self):
        self._arger = self._set_up_arg_parser()
        self._commands = {
            "poll": self._poll_handler,
            "fetch": self._fetch_handler,
            "history": self._history_handler,
            "backup": self._backup_handler,
            "restore": self._restore_handler,
            "services": self._services_handler,
            "help": self._help_handler
        }

    def _set_up_arg_parser(self):
        """
        ArgParse setup
        """

        arger = argparse.ArgumentParser(description="StatusBot v1.0 by RuiPires")

        subparsers = arger.add_subparsers(dest="command")

        poll_parser = subparsers.add_parser("poll", help="Outputs state of services")
        poll_parser.add_argument("--only")
        poll_parser.add_argument("--exclude")

        fetch_parser = subparsers.add_parser("fetch", help="Polls services every n seconds")
        fetch_parser.add_argument("--rate")
        fetch_parser.add_argument("--only")
        fetch_parser.add_argument("--exclude")

        history_parser = subparsers.add_parser("history", help="Outputs history of poll/fetch requests")
        history_parser.add_argument("--only")

        backup_parser = subparsers.add_parser("backup", help="Stores history in provided file")
        backup_parser.add_argument("file")
        backup_parser.add_argument("--format", dest="file_format")

        restore_parser = subparsers.add_parser("restore", help="Replaces history file with provided file")
        restore_parser.add_argument("file")
        restore_parser.add_argument("--merge")

        services_parser = subparsers.add_parser("services", help="Outputs available services")

        help_parser = subparsers.add_parser("help", help="Outputs help message")

        return arger

    def _poll_handler(self, bot, opts=None):
        """
        Handler for pool command
        :param bot: Bot object
        :param opts: ArgParse output
        """

        options = opts.exclude or opts.only or None

        # bot.poll(is_exclude, is_include, options)

    def _fetch_handler(self, bot, opts=None):
        """
        Handler for fetch command
        :param bot: Bot object
        :param opts: Argparse output
        """
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

    # handler for history command
    def _history_handler(self, bot, opts=""):
        if opts.only:
            bot.history(True, opts.only)
        else:
            bot.history()

    # handler for backup command
    def _backup_handler(self, bot, opts=""):
        option = opts.file_format if opts.file_format else "default"
        bot.backup(opts.file, option.lower())

    # handler for services command
    def _services_handler(self, bot, opts=""):
        bot.services()


    # handler for restore command
    def _restore_handler(self, bot, opts=""):
        bot.restore(opts.file, True if opts.merge == "true" else False)

    # handler for help command
    def _help_handler(self, bot, opts=""):
        self.__help__()

    def _help__(self):
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
                ''')

    # Run bot
    def run(self):

        opts = self._arger.parse_args()
        bot = poll_helper.Poller()
        command = opts.command
        self._commands[command](bot, opts)
