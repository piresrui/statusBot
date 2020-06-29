from typing import NewType

from poller.utils import ServiceEnum
from config import *


URL = NewType("URL", str)


class WS:
    """
        Wrapper class for endpoint composition
    """

    @staticmethod
    def _fetch_base(service: ServiceEnum) -> URL:
        return BaseConfig.SERVICES[service.value]

    @staticmethod
    def get_url(service: ServiceEnum) -> URL:
        return WS._fetch_base(service)
