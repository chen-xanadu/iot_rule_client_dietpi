#!/bin/bash

source $HOME/iot-inspector-local/iot/bin/activate
cd $HOME/iot-inspector-local/src


#TODO: wait until Internet is up
while ! ping -c 1 -w 1 -n 18.119.20.148 &> /dev/null
do
  sleep 5
done


sudo $HOME/iot-inspector-local/iot/bin/python3 $HOME/iot-inspector-local/src/start_inspector.py  >$HOME/inspector.log 2>&1