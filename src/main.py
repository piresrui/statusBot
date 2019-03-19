import argparse
from status import Status

def commands():

    arger = argparse.ArgumentParser(description="StatusBot v1.0 by RuiPires")

    subparsers = arger.add_subparsers(dest="command")

    poll_parser = subparsers.add_parser("poll", help="Outputs state of services")
    poll_parser.add_argument("--only", dest="only", help="Show only these services ex: --only=github,slack")
    poll_parser.add_argument("--exclude", dest="exclude")

    fetch_parser = subparsers.add_parser("fetch", help="Polls services every n seconds")
    fetch_parser.add_argument("--rate", dest="rate")

    history_parser = subparsers.add_parser("history", help="Outputs history of poll/fetch requests")
    history_parser.add_argument("--only", dest="only")

    backup_parser = subparsers.add_parser("backup", help="Stores history in provided file")
    backup_parser.add_argument("file")
    backup_parser.add_argument("--format", dest="file_format")

    restore_parser = subparsers.add_parser("restore", help="Replaces history file with provided file")
    restore_parser.add_argument("file")
    restore_parser.add_argument("--merge", dest="merge")

    services_parser = subparsers.add_parser("services", help="Outputs available services")

    opts = arger.parse_args()
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
        if opts.rate:
            bot.fetch(opts.rate)
        else:
            bot.fetch()

    elif command == "history":
        if opts.only:
            bot.history(True, opts.only)
        else:
            bot.history()

    elif command == "backup":
        option = opts.file_format if opts.file_format else "default"
        bot.backup(opts.file, option)

    elif command == "services":
        bot.services()

    elif command == "restore":
        bot.restore(opts.file, True if opts.merge=="true" else False)

    else:
        pass
        
    

if __name__ == "__main__":
    commands()

   


