import requests
import config
from http import HTTPStatus
import json
import time
import shutil


class Poller:

    def __init__(self):
        self.services = self._load_services()
        self.logger = Logger()

    def poll(self):
        for service in self.services:
            r = self._get_request(service['api'])
            message = r.json()

            status = r.status_code == HTTPStatus.OK and message['status'][
                'description'].rstrip() == config.SERVICE_UP_MESSAGE

            service_id = service['id']
            poll_date = message['page']['updated_at']
            state = "up" if status else 'down'

            self.logger.save_to_file(service_id, poll_date, state)
            self._output_message(service_id, poll_date, state)

    def fetch(self, interval: int):
        while True:
            self.poll()
            time.sleep(interval)

    def backup(self, dest: str):
        shutil.copy(config.BACKUP_FILE, dest)

    def restore(self, src: str):
        shutil.copy(src, config.BACKUP_FILE)

    def history(self):
        with open(config.BACKUP_FILE, "r") as f:
            for line in f.readlines()[1:]:
                service_id, date, state = line.rstrip().split(",")
                self._output_message(service_id, date, state)

    """
        Private methods
    """

    def _output_message(self, id, date, status):
        output = "[{}] {} - {}".format(id, date, status)
        print(output)

    def _get_request(self, service: str) -> requests.Response:
        """
        Returns response from service
        :param service: URL of request
        :return: Response of request
        """
        return requests.get(service, headers=config.HEADERS)

    def _load_services(self):
        with open(config.SERVICE_FILE, "r") as f:
            j = json.load(f)
        return j['services']


class Logger:
    """
    Deals with saving logs
    """

    def __init__(self):
        pass

    def save_to_file(self, service: str, date: str, status: str):
        with open(config.BACKUP_FILE, "a") as f:
            f.write("{},{},{}\n".format(service, date, status))
