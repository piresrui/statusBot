from status_bot.poller import Poll
from status_bot.utils.enums import Service

if __name__ == "__main__":
    Poll().poll(services=[s for s in Service])

