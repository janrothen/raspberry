# Cryptocurrency

### check_bitcoin_reachability.py
Checks if bitcoin full node is reachable from outside  

## Prerequisites

python3  
configparser==3.5.0  
python-dateutil==2.7.3  

## Installing

Create symlink to utils in this directory, or imports wont work  
Configure the scripts: config.conf  

Add cryptocurrency script to cron:  
crontab -e  
  
0 17 * * *  /home/pi/raspberry/cryptocurrency/check_bitcoin_reachability.py  
