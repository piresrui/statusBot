import os
import yaml

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

HEADERS = {'User-Agent': "StatusBot v1.0"}
SERVICE_UP_MESSAGE = "All Systems Operational"
DEFAULT_RATE = 5
DEFAULT_POLL_FORMAT = "[{}] {} - {}"
AVAILABLE_FORMATS = ["csv", "json", "txt"]

# New shit

SERVICE_FILE = os.path.join(ROOT_DIR, "services.yaml")
BACKUP_FILE = os.path.join(ROOT_DIR, "backup.csv")


def _load_service():
    with open(SERVICE_FILE, "r") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return data['services']


class BaseConfig:
    SERVICES: dict = _load_service()
