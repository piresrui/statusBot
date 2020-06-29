from enum import Enum


class Service(Enum):
    github = "github"
    bitbucket = "bitbucket"


class Issue(Enum):
    NO_ISSUE = "none"
    MINOR = "minor"
    MAJOR = "major"
    CRITICAL = "critical"

    @classmethod
    def has_value(cls, value: str) -> bool:
        return value in cls._value2member_map_

