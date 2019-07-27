import requests
import config
from http import HTTPStatus
import json
import time
import shutil


class Poller:
    """
    Class that controls essential poller functions
    """

    def __init__(self):
        self.services = self._load_services()
        self.logger = Logger()

    def poll(self, flag: str, service_list: list):
        """
        Polls API of every service defined in configuration
        :param flag: String with type of flag
        :param service_list: List of services associated with flag
        """
        for service in self.services:

            service_id = service['id']

            if flag == "exclude" and service_id in service_list:
                continue

            if flag == "only" and service_id not in service_list:
                continue

            r = self._get_request(service['api'])
            message = r.json()

            status = r.status_code == HTTPStatus.OK and \
                     message['status']['description'].rstrip() == config.SERVICE_UP_MESSAGE

            poll_date = message['page']['updated_at']
            state = "up" if status else 'down'

            self.logger.save_to_file(service_id, poll_date, state)
            self._output_message(service_id, poll_date, state)

    def fetch(self, flag: str, service_list: list, interval: int):
        """
        Calls Poll every N seconds
        :param flag: String with type of flag
        :param service_list: List of services associated with flag
        :param interval: Integer seconds between each poll call
        """
        while True:
            self.poll(flag, service_list)
            time.sleep(interval)

    def backup(self, dest: str):
        """
        Copies system backup to specified file
        :param dest: Path of file to copy to
        """
        shutil.copy(config.BACKUP_FILE, dest)

    def restore(self, src: str):
        """
        Copies given file into system backup
        :param src: FIle of path to copy from
        """
        shutil.copy(src, config.BACKUP_FILE)

    def history(self, service_list: list):
        """
        Outputs contents of backup file with poll format
        :param service_list: List of services to display, empty list or None if all values need to be displayed
        """
        with open(config.BACKUP_FILE, "r") as f:
            for line in f.readlines()[1:]:
                service_id, date, state = line.rstrip().split(",")

                if service_list and service_id not in service_list:
                    continue

                self._output_message(service_id, date, state)

    def list_services(self):
        """
        Outputs all available services and respective endpoints
        """
        for service in self.services:
            print("Service: {}\n\tURL: {}\n\tAPI: {}".format(service['name'], service['url'], service['api']))

    """
        Private methods
    """

    def _output_message(self, id, date, status):
        """
        Prints message in poll format
        :param id: Service ID
        :param date: Poll date
        :param status: State of poll
        """
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
        """
        Loads config services into memory
        """
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
        """
        Logs poll values into backup file
        :param service: Service id
        :param date: Poll date
        :param status: Poll status
        """
        with open(config.BACKUP_FILE, "a") as f:
            f.write("{},{},{}\n".format(service, date, status))
