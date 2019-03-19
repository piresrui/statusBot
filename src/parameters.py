import os

__config_fileName__ = "config.json"
__backup_fileName__ = "backup.json"
__hdr__ = { 'User-Agent' : 'StatusBot v1.0' }
__data__ = {}
__location__ = os.path.realpath( os.path.join(os.getcwd(), os.path.dirname(__file__)))
__config_file_location__ = os.path.join(__location__, __config_fileName__)
__backup_file_location__ = os.path.join(__location__, __backup_fileName__)
__date_format__ = "%Y-%m-%dT%H:%M:%S.%fZ"
__success_message__ = 'All Systems Operational'