import json
import subprocess
import os
from pathlib import Path

import requests
from crontab import CronTab

from config import *


# Generate ssh key
ssh_dir = Path.home() / '.ssh'
sk = ssh_dir / 'id_ed25519'
pk = ssh_dir / 'id_ed25519.pub'

if not sk.is_file():
    subprocess.run('ssh-keygen -q -t ed25519 -N "" -f "{}"'.format(sk), shell=True)


# Add server public key
authorized_keys = ssh_dir / 'authorized_keys'
authorized_keys.write_text(SERVER_PK + '\n')
authorized_keys.chmod(0o600)


# Register with server
SERVER_API_KEY = os.getenv('SERVER_API_KEY')

resp = requests.post(SERVER_BASE_URL + '/user.add', params={'api_key': SERVER_API_KEY}, files={'pk': pk.open('rb')})

user_data = resp.json()

if 'id' not in user_data:
    print('Register error')
    exit()


# Save user data
USER_FILE.write_text(json.dumps(user_data))

print('The nickname for this device is: {}'.format(user_data["nickname"]))


# Create directories
DEVICE_DIR.mkdir(parents=True, exist_ok=True)
TCPDUMP_DIR.mkdir(parents=True, exist_ok=True)
TSHARK_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# Format cron job commands
nickname = user_data['nickname']
ssh_port = user_data['ssh_port']

autossh_cmd = 'autossh -M 0 -o "StrictHostKeyChecking no" -o "ServerAliveInterval 10" -o "ServerAliveCountMax 3" -fN -R ' \
              '{}:localhost:22 {}@{}'.format(ssh_port, nickname, SERVER_DOMAIN)


upload_script = Path(__file__).resolve().parent / 'upload_data.sh'
upload_cmd = upload_script.read_text()
upload_cmd = upload_cmd.format(user=nickname, server=SERVER_DOMAIN, data_dir=UPLOAD_DIR, interval=60*SFTP_UPLOAD_INTERVAL_IN_MINUTES)
upload_script.write_text(upload_cmd)
upload_script.chmod(0o755)


inspector_script = Path(__file__).resolve().parent / 'start_inspector.sh'
inspector_script.chmod(0o755)

tcpdump_script = Path(__file__).resolve().parent / 'init_tcpdump.sh'
tcpdump_cmd = tcpdump_script.read_text()
tcpdump_cmd = tcpdump_cmd.format(tcpdump_dir=TCPDUMP_DIR, tshart_dir=TSHARK_DIR, upload_dir=UPLOAD_DIR)
tcpdump_script.write_text(tcpdump_cmd)
tcpdump_script.chmod(0o755)

initialize_script = Path(__file__).resolve().parent / 'initialize.py'


debug_script = Path(__file__).resolve().parent / 'debug.sh'
debug_script.chmod(0o755)

# Set cron job
with CronTab(user=os.getlogin()) as cron:
    cron.remove_all()

    autossh_job = cron.new(command=autossh_cmd)
    autossh_job.every_reboot()

    inspector_job = cron.new(command=str(inspector_script))
    inspector_job.every_reboot()
    
    tcpdump_job = cron.new(command=str(tcpdump_script))
    tcpdump_job.every_reboot()

    initialize_job = cron.new(command='python3 ' + str(initialize_script))
    initialize_job.every_reboot()

    upload_job = cron.new(command=str(upload_script))
    upload_job.every_reboot()

    debug_job = cron.new(command=str(debug_script))
    debug_job.every().hour()
