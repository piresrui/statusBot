import argparse
from status import Status
import sys

def commands(args=sys.argv[1:]):

    parser = argparse.ArgumentParser(prog='StatusBot', usage='%(prog)s [options]')
    usage = "usage: python3 statusbot [options]"

    arg_size = len(args)
    if arg_size == 0:
        print(usage)
        return

    bot = Status()

    if args[0] == "poll":
        bot.poll()
    elif args[0] == "backup":
        if(arg_size == 2):
            bot.backup(args[1])
        else:
            print(usage)
    elif args[0]== "history":
        bot.history()
    else:
        print(usage)
        
    

if __name__ == "__main__":
    commands()

   


