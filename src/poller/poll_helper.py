import requests
import config
from http import HTTPStatus
import json
import time
import shutil
from collections import defaultdict
import datetime
import sys
import signal


class Poller:
    """
    Class that controls essential poller functions
    """

    def __init__(self):
        self.services = self._load_services()
        self.logger = Logger()
        self.file_editor = FileEditor()

        self.DEFAULT_FORMATS = {
            "csv": self.file_editor.default_format,
            "json": self.file_editor.json_format,
            "txt": self.file_editor.txt_format
        }
        self._capture_sigint()

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

            # poll_date = message['page']['updated_at']
            poll_date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
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

    def backup(self, dest: str, flag: str):
        """
        Copies system backup to specified file
        :param dest: Path of file to copy to
        :param flag: Format to copy as
        """

        self.DEFAULT_FORMATS[flag](dest)
        print("Successfully created {} with {} format".format(dest, flag))

    def restore(self, src: str, merge: bool):
        """
        Copies given file into system backup
        :param src: FIle of path to copy from
        """
        if merge:
            self.file_editor.merge(src)
        else:
            shutil.copy(src, config.BACKUP_FILE)
        print("Successfully restored backup file.")

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

    @staticmethod
    def _output_message(service_id, date, status):
        """
        Prints message in poll format
        :param service_id: Service ID
        :param date: Poll date
        :param status: State of poll
        """
        output = config.DEFAULT_POLL_FORMAT.format(service_id, date, status)
        print(output)

    @staticmethod
    def _get_request(service: str) -> requests.Response:
        """
        Returns response from service
        :param service: URL of request
        :return: Response of request
        """
        return requests.get(service, headers=config.HEADERS)

    @staticmethod
    def _load_services():
        """
        Loads config services into memory
        """
        with open(config.SERVICE_FILE, "r") as f:
            j = json.load(f)
        return j['services']

    @staticmethod
    def _capture_sigint():
        def signal_handler(sig, frame):
            print("Exiting...")
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)


class FileEditor:
    """
    Class to deal with file writes
    """

    def __init__(self):
        pass

    @staticmethod
    def txt_format(dest: str):

        with open(config.BACKUP_FILE, "r") as f:
            with open(dest, "a+") as dest_f:
                for line in f.readlines()[1:]:
                    service_id, date, state = line.split(",")
                    dest_f.write(config.DEFAULT_POLL_FORMAT.format(service_id, date, state))

    @staticmethod
    def json_format(dest: str):

        json_default = defaultdict(list)

        with open(config.BACKUP_FILE, "r") as f:
            for line in f.readlines()[1:]:
                service_id, date, state = line.rstrip().split(",")
                new_val = {
                    "date": date,
                    "status": state
                }
                json_default[service_id].append(new_val)
        with open(dest, "w+") as f:
            json.dump(dict(json_default), f, indent=4)

    @staticmethod
    def default_format(dest: str):
        shutil.copyfile(config.BACKUP_FILE, dest)

    @staticmethod
    def merge(src: str):

        with open(config.BACKUP_FILE, "a") as f:
            with open(src, "r") as rfile:
                for line in rfile.readlines()[1:]:
                    f.write(line)


class Logger:
    """
    Deals with saving logs
    """

    def __init__(self):
        pass

    @staticmethod
    def save_to_file(service: str, date: str, status: str):
        """
        Logs poll values into backup file
        :param service: Service id
        :param date: Poll date
        :param status: Poll status
        """
        with open(config.BACKUP_FILE, "a") as f:
            f.write("{},{},{}\n".format(service, date, status))
