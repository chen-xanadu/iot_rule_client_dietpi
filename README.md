# Setup Guide for NanoPi R2S + DietPi OS

## Before shipping to the participant

*What we need to do?*
### 0. DietPi OS Image installation

Download the DietPi image for NanoPi R2S from [https://dietpi.com/docs/hardware/#nanopi-series-friendlyarm](https://dietpi.com/docs/hardware/#nanopi-series-friendlyarm) and flash it to the SD card.


### 1. Configure DietPi OS

First ssh into the DietPi as the root user (username: `root`, password: `dietpi`). Choose the following settings:

- `0    : Opt OUT and purge uploaded data`
- Do you want to adjust the default global software password for DietPi-Software installations? -- `Cancel` 
- Change existing unix user passwords? -- `Cancel`
- A serial console is currently enabled, would you like to disable it? -- `Cancel`
- **Important**: Change the  *SSH Server* to *OpenSSH*:
```
│    SSH Server           : [OpenSSH Server]                                   │
│    File Server          : [None]                                             │
│    Log System           : [DietPi-RAMlog #1]                                 │
│    Webserver Preference : [Lighttpd]                                         │
│    Desktop Preference   : [LXDE]                                             │
│    Browser Preference   : [None]                                             │
│    User Data Location   : [SD/eMMC | /mnt/dietpi_userdata]                   │
```

After DietPi finishes the update, **log out from the current session** and **log in through the *dietpi* user account** (username: `dietpi`, password: `dietpi`) to proceed the steps below. Note that the fingerprint of the NanoPi has changed, so we might need to modify `~/.ssh/known_hosts` on our computer to ssh again.




### 2. Install required packages

```shell
#!/bin/bash

sudo apt update
sudo apt install -y build-essential python3-pip python3-venv python3-dev git vim autossh lftp tcpdump nmap tshark
pip3 install requests python-crontab
```

### 3. Install IoT Inspector local
```shell
cd $HOME
git clone https://github.com/chen-xanadu/iot-inspector-local.git
cd iot-inspector-local
python3 -m venv iot
source ./iot/bin/activate
pip3 install -r ./src/requirements.txt
deactivate
```

### 4. Register with server

Set the server API key to the environment variable `SERVER_API_KEY`
```shell
export SERVER_API_KEY=????
```

Download this repo under the home directory and run `register.py`.
```shell
cd $HOME
git clone https://github.com/chen-xanadu/iot_rule_client_dietpi
python3 ./iot_rule_client_dietpi/register.py
```
If `register.py` runs successfully, it will output a nickname:
```
The nickname for this device is: buckeye
```
Tape the nickname onto the Raspberry Pi box, as it will be used as the id for the device.


### 5. Disable password login (skip this step for debugging devices)

Follow the Step 4 in [https://www.cyberciti.biz/faq/how-to-disable-ssh-password-login-on-linux/](https://www.cyberciti.biz/faq/how-to-disable-ssh-password-login-on-linux/)


### 6. Shutdown/reboot the Pi
```shell
sudo reboot
```



## After the participant gets the device

### 1. Set participant to active

When the Raspberry Pi is shipped, we should set the participant's status to active. One simple way to achieve this is to visit [the server's OpenAPI page](https://wiscshr.com/docs#/default/set_active_user_set_active_post) and execute the `/user.set_active` API.

Once the Raspberry Pi is powered on (by the participant), the IoTInspector (and a few helper script) should be running automatically.

**Please ensure the router is connected to the Internet AND the Raspberry Pi is connected to the router before powering on the Raspberry Pi!**  Sometimes the IoTInspector hangs up (failing to detect any local devices) if no Internet is detected. Reboot the Pi if such issue is encountered.

### 2. Choose which devices to monitor



Visit `https://wiscshr.com/[nickname]` to select which devices to monitor.

*Note:* if most device names are empty, restarting the router usually helps. 
