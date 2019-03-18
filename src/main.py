import argparse
from status import Status

def commands():

    arger = argparse.ArgumentParser(description="StatusBot v1.0 by RuiPires")

    subparsers = arger.add_subparsers(dest="command")

    poll_parser = subparsers.add_parser("poll")
    poll_parser.add_argument("--only", dest="only")
    poll_parser.add_argument("--exclude", dest="exclude")

    history_parser = subparsers.add_parser("history")
    history_parser.add_argument("--only", dest="only")

    backup_parser = subparsers.add_parser("backup")
    backup_parser.add_argument("file")

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
        bot.fetch()

    elif command == "history":
        if opts.only:
            bot.history(True, opts.only)
        else:
            bot.history()

    elif command == "backup":
        bot.backup(opts.file)

    elif command == "services":
        bot.services()

    else:
        pass
        
    

if __name__ == "__main__":
    commands()

   


