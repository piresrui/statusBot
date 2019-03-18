import argparse
from status import Status
import sys

def commands(args=sys.argv[1:]):

    parser = argparse.ArgumentParser(prog='StatusBot', usage='%(prog)s [options]')

    if len(args) == 0:
        print("usage: python3 statusbot [options]")
        return

    bot = Status()

    if args[0] == "poll":
        bot.poll()
    elif agrs[0] == "backup":
        pass
    

if __name__ == "__main__":
    commands()

   


