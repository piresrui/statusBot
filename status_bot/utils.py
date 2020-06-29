from enum import Enum
from typing import Tuple
import requests

from config import *


class Services(Enum):
    github = "github"
    bitbucket = "bitbucket"


class _WS:
    """
        Wrapper class for endpoint composition
    """

    @staticmethod
    def _append(**kwargs) -> str:
        # TODO make actual appender? Or get rid of this?
        # Currently no need for it since I only make requests to summary but when
        # we add more services it might be needed
        url_suffix = "summary.json"

        return url_suffix

    @staticmethod
    def _fetch_base(service: Services) -> str:
        item: dict = BaseConfig.SERVICES[service.value]

        return item.get("api")

    @classmethod
    def get_url(cls, service: Services) -> str:
        return cls._fetch_base(service) + cls._append()


class Requester:

    @staticmethod
    def request(service: Services):
        url = _WS.get_url(service=service)

        return Requester._requester(url=url)

    @staticmethod
    def _requester(url: str) -> Tuple[int, requests.Response]:
        response = requests.request(
            "GET",
            url=url,
        )

        return response.status_code, response
