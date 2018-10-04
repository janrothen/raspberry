# Raspberry Stuff

Cryptocurrency related scripts for my Raspberry Pi 3

## Getting Started

### check_bitcoin_reachability.py
Checks if bitcoin full node is reachable from outside  
Sends an alert notification email otherwise  

### check_crown_block_rewards.py
Checks if crown master node is receiving block rewards  
Sends an alert notification email otherwise  

### check_stellar_inflation_payments.py
Checks if stellar lumens address is receiving inflation payments  
Sends an alert notification email otherwise  

## Prerequisites

python3  
sudo pip3 install configparser  
sudo pip3 install python-dateutil  

## Installing

Configure the scripts: config.conf  
Add it to cron:  
crontab -e  
  
0 17 * * *  /home/pi/cron/check_bitcoin_reachability.py  
0 17 * * *  /home/pi/cron/check_crown_block_rewards.py  
0 17 * * *  /home/pi/cron/check_stellar_inflation_payments.py  
