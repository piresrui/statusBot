from config import *
from ws import WS


class Poll:

    def __init__(self):
        pass

    def poll(self):
        for service, items in BaseConfig.SERVICES.items():
            api = WS.get_url(service)

            print(api)
