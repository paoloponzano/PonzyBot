#!/bin/bash
echo "bot running"
if [ ! -f conf.py ]; then
echo "File conf.py not found.Follow the guide on https://github.com/veetaw/linuxshellbot and create the conf.py" 
fi 
while true; 
 do
  cd /
  cd /home/pi/Desktop/bot
  python3 main.py
  cd /
 done  
