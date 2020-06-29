from typing import List

from errors import InvalidServiceError
from utils import Requester, Services


class Poll:

    def __init__(self):
        pass

    def poll(self, services: List[Services]):

        for service in services:
            try:
                _, response = Requester.request(service=service)

                r = response.json()

                print(r)
            except KeyError:
                raise InvalidServiceError


if __name__ == "__main__":
    Poll().poll(services=[s for s in Services])
