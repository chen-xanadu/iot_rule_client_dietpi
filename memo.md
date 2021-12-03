# apt

python3-pip, python3-venv, git, autossh, lftp, libpcap-dev


# pip

httpx, 

# bash

```shell
git clone https://github.com/nyu-mlab/iot-inspector-local.git

python3 -m venv iot
source ./iot/bin/activate

pip3 install -r src/requirements.txt
sudo python3  ~/iot-inspector-local/src/start_inspector.py
```

# iot_inspector


1. upload fork to github
2. local monitor
3. remote monitor

DietPi Setup

1. `0    : Opt OUT and purge uploaded data`
1. Do you want to adjust the default global software password for               │
│ DietPi-Software installations? 
1. Change existing unix user passwords?
1. │ A serial console is currently enabled, would you like to disable it?         │
1. │    SSH Server           : [OpenSSH Server]                                   │
│    File Server          : [None]                                             │
│    Log System           : [DietPi-RAMlog #1]                                 │
│    Webserver Preference : [Lighttpd]                                         │
│    Desktop Preference   : [LXDE]                                             │
│    Browser Preference   : [None]                                             │
│    User Data Location   : [SD/eMMC | /mnt/dietpi_userdata]                   │

