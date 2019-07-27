import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

HEADERS = {'User-Agent': "StatusBot v1.0"}
SERVICE_UP_MESSAGE = "All Systems Operational"
DEFAULT_RATE = 5

SERVICE_FILE = os.path.join(ROOT_DIR, "config/services.json")
BACKUP_FILE = os.path.join(ROOT_DIR, "config/backup.csv")