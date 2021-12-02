from pathlib import Path

SERVER_DOMAIN = 'wiscshr.com'
SERVER_BASE_URL = 'https://' + SERVER_DOMAIN
SERVER_PK = 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGUuiKmLa4hL3WxW+n9gs+OYxkaxucRXQ/ASOcnt6gWl ubuntu@ip-172-31-47-82'

INSPECTOR_URL = 'http://localhost:46241'

USER_FILE = Path.home() / 'user.json'
DEVICE_DIR = Path.home() / 'devices'

# TODO: set to actual tcpdump dir
TCPDUMP_DIR = Path.home() / 'tcpdumpout'
TSHARK_DIR = Path.home() / 'tsharkout'
UPLOAD_DIR = Path.home() / 'data'

SFTP_UPLOAD_INTERVAL_IN_MINUTES = 30
