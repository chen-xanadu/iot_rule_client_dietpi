import json
import subprocess
import time
from datetime import datetime
from pathlib import Path

import requests

import utils
from config import *


user = json.loads(USER_FILE.read_text())

nickname = user['nickname']
token = user['token']

# wait for user to be set to active
while not utils.is_active(token):
    print('The user \"{}\" is not active'.format(nickname))
    time.sleep(10)

user['is_active'] = True
USER_FILE.write_text(json.dumps(user))


# upload pi's local IP
p = subprocess.run('hostname -I', shell=True, stdout=subprocess.PIPE)
local_ip = p.stdout.decode().strip().split()[0]

utils.update_local_ip(token, local_ip)


# wait for IoTInspector
while not utils.is_inspector_ready():
    print('IoT inspector is not ready')
    time.sleep(2)


# Continue to monitor old devices and scan for new devices
interval = 10
max_interval = 600

while True:

    if utils.is_inspector_ready():
        utils.ping_server(token)
    else:
        continue

    devices = utils.get_devices_from_inspector()

    for device_id, device in devices.items():

        device_attr = {
            'id': device['device_id'],
            'internal_ip': device['device_ip'],
            'mac': device['device_mac'],
            'name': device['dhcp_name'],
            'vendor': device['device_vendor'],
            'is_monitored': device['is_inspected'],
            'last_monitor_timestamp': str(datetime.utcnow())
        }

        resp = requests.post(SERVER_BASE_URL + '/device.add', params={'token': token}, json=device_attr)


    time.sleep(interval)
    interval = interval + 10
    if interval > max_interval:
        interval = max_interval

