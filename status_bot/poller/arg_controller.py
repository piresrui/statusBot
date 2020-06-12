import argparse
import sys

from poller import poll_helper
from config import config


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

    @staticmethod
    def _set_up_arg_parser() -> argparse.ArgumentParser:
        """
        ArgParse setup
        """

        arger = argparse.ArgumentParser(description="StatusBot")

        subparsers = arger.add_subparsers(dest="command")

        poll_parser = subparsers.add_parser("poll", help="Outputs state of services")
        poll_parser.add_argument("--only", nargs="+")
        poll_parser.add_argument("--exclude", nargs="+")

        fetch_parser = subparsers.add_parser("fetch", help="Polls services every n seconds")
        fetch_parser.add_argument("--rate", type=int)
        fetch_parser.add_argument("--only", nargs="+")
        fetch_parser.add_argument("--exclude", nargs="+")

        history_parser = subparsers.add_parser("history", help="Outputs history of poll/fetch requests")
        history_parser.add_argument("--only", nargs="+")

        backup_parser = subparsers.add_parser("backup", help="Stores history in provided file")
        backup_parser.add_argument("file")
        backup_parser.add_argument("--format", nargs="?", default="csv", choices=config.AVAILABLE_FORMATS)

        restore_parser = subparsers.add_parser("restore", help="Replaces history file with provided file")
        restore_parser.add_argument("file")
        restore_parser.add_argument("--merge", action="store_true")

        subparsers.add_parser("services", help="Outputs available services")

        subparsers.add_parser("help", help="Outputs help message")

        return arger

    """
    Handlers for system functions
    """

    @staticmethod
    def _poll_handler(bot: poll_helper.Poller, opts: argparse.Namespace):
        service_list = opts.exclude or opts.only or []
        if opts.exclude:
            flag = "exclude"
        elif opts.only:
            flag = "only"
        else:
            flag = None

        bot.poll(flag, service_list)

    @staticmethod
    def _fetch_handler(bot: poll_helper.Poller, opts: argparse.Namespace):
        service_list = opts.exclude or opts.only or []
        if opts.exclude:
            flag = "exclude"
        elif opts.only:
            flag = "only"
        else:
            flag = None

        bot.fetch(flag, service_list, opts.rate or config.DEFAULT_RATE)

    @staticmethod
    def _history_handler(bot: poll_helper.Poller, opts: argparse.Namespace):
        bot.history(opts.only)

    @staticmethod
    def _backup_handler(bot: poll_helper.Poller, opts: argparse.Namespace):
        bot.backup(opts.file, opts.format)

    @staticmethod
    def _services_handler(bot, opts=None):
        bot.list_services()

    @staticmethod
    def _restore_handler(bot: poll_helper.Poller, opts: argparse.Namespace):
        bot.restore(opts.file, opts.merge)

    def _help_handler(self, bot=None, opts=None):
        self._help()

    @staticmethod
    def _help():
        print('''
                    poll                Outputs state of services
                                            Optional args:
                                                --only      Show only provided services                 
                                                --exclude   Omit provided services                      

                    fetch               Calls poll every 5 seconds
                                            Optional args:
                                                --rate      Refresh every rate seconds                  
                                                --only      Show only provided services                 
                                                --exclude   Omit provided services                      

                    history             Outputs all previous recorded poll/fetch calls
                                            Optional args:
                                                --only      Show only provided services                 

                    backup <file_path>  Copies history to <file_path> in CSV format
                                            Optional args:
                                                --format    Store data in requested format (TXT or JSON) 

                    restore <file_path> Replaces provided JSON backup into history
                                            Optional args:
                                                --merge     Merges content instead of replacing

                    services            Outputs available services and endpoint
s
                    help                Outputs help message
                ''')

    # Run bot
    def run(self):
        opts = self._arger.parse_args()
        bot = poll_helper.Poller()
        if not opts.command:
            print("Invalid usage. Use -h/--help/help.")
            sys.exit(1)
        self._commands[opts.command](bot, opts)
