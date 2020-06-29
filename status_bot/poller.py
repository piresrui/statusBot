import time
from typing import List

from status_bot.utils.enums import Service
from status_bot.utils.errors import InvalidServiceError
from status_bot.utils.processors import Requester, Filter


class Poll:

    def __init__(self):
        pass

    def poll(self, services: List[Service]):

        for service in services:
            try:
                _, response = Requester.request(service=service)

                Filter.process(service=service, data=response.json())
            except KeyError:
                raise InvalidServiceError

    def fetch(self, rate: int):
        while True:
            self.poll(services=[])
            time.sleep(rate)
