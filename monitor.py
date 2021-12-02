import json
import subprocess
import time
import os
from pathlib import Path

import requests
from crontab import CronTab

import utils
from config import *

user = json.loads(USER_FILE.read_text())

nickname = user['nickname']
token = user['token']


while not utils.is_inspector_ready():
    print('IoT inspector is not ready')
    time.sleep(2)


devices = utils.get_devices_from_server(token)

for device in devices:
    if device['is_monitored']:
        requests.get(INSPECTOR_URL + '/enable_inspection/' + device['id'])
    else:
        requests.get(INSPECTOR_URL + '/disable_inspection/' + device['id'])


