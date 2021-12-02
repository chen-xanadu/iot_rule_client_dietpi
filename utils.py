import json
import subprocess
from pathlib import Path

import requests

from config import *




def is_active(token: str):
    try:
        resp = requests.get(SERVER_BASE_URL + '/user.is_active', params={'token': token})
        return resp.json()['is_active']
    except:
        return False


def ping_server(token: str):
    try:
        requests.post(SERVER_BASE_URL + '/user.ping', params={'token': token})
    except:
        pass



def update_local_ip(token: str, local_ip: str):
    resp = requests.post(SERVER_BASE_URL + '/user.update', params={'token': token, 'internal_ip': local_ip})


def is_inspector_ready():
    try:
        resp = requests.get(INSPECTOR_URL + '/is_ready')
        return resp.json()['status'] == 'OK'
    except:
        return False


def get_devices_from_inspector():
    resp = requests.get(INSPECTOR_URL + '/get_device_list')
    try:
        return resp.json()
    except:
        return {}


def get_devices_from_server(token: str):
    try:
        resp = requests.get(SERVER_BASE_URL + '/device.list', params={'token': token})
        return resp.json()
    except:
        return []

