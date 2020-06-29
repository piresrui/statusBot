from typing import Tuple
import requests

from config import *
from utils.enums import Service, Issue
from utils.errors import ApiParserError
from utils.logger import Logger


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
    def _fetch_base(service: Service) -> str:
        item: dict = BaseConfig.SERVICES[service.value]

        return item.get("api")

    @classmethod
    def get_url(cls, service: Service) -> str:
        return cls._fetch_base(service) + cls._append()


class Requester:

    @staticmethod
    def request(service: Service):
        url = _WS.get_url(service=service)

        return Requester._requester(url=url)

    @staticmethod
    def _requester(url: str) -> Tuple[int, requests.Response]:
        response = requests.request(
            "GET",
            url=url,
        )

        return response.status_code, response


class Filter:

    @staticmethod
    def process(service: Service, data: dict):
        status = data.get("status", {}).get("indicator", None)
        if status is None:
            raise ApiParserError("Failed fetching status")

        if Issue.has_value(status):
            # TODO call logger?
            Logger().output(service=service, indicator=Issue(status))
        else:
            # Should not happen, check APIs
            pass


