from typing import List

from utils.enums import Service
from utils.errors import InvalidServiceError
from utils.processors import Requester, Filter


class Poll:

    def __init__(self):
        pass

    def poll(self, services: List[Service]):

        for service in services:
            try:
                _, response = Requester.request(service=service)

                r = response.json()

                Filter.process(service=service, data=r)
            except KeyError:
                raise InvalidServiceError

