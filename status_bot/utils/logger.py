import datetime

from utils.enums import Issue, Service


class Singleton(object):
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instances[cls]


class Logger(Singleton):

    def __init__(self):
        self._messages = {
            Issue.NO_ISSUE: "No Issue",
            Issue.MINOR: "Minor Issues",
            Issue.MAJOR: "Major Issues",
            Issue.CRITICAL: "CRITICAL Issues"
        }

    def output(self, service: Service, indicator: Issue):
        print(f"{service.value} - {datetime.datetime.now()} - {self._messages[indicator]}")
