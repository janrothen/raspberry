# Cryptocurrency

### check_bitcoin_reachability.py
Checks if bitcoin full node is reachable from outside  

### check_crown_block_rewards.py
Checks if crown master node is receiving block rewards  

### check_stellar_inflation_payments.py
Checks if stellar lumens address is receiving inflation payments  

## Prerequisites

python3  
configparser==3.5.0  
python-dateutil==2.7.3  

## Installing

Create symlink to utils in this directory, or imports wont work  
Configure the scripts: config.conf  

Add cryptocurrency scripts to cron:  
crontab -e  
  
0 17 * * *  /home/pi/raspberry/cryptocurrency/check_bitcoin_reachability.py  
0 17 * * *  /home/pi/raspberry/cryptocurrency/check_crown_block_rewards.py  
0 17 * * *  /home/pi/raspberry/cryptocurrency/check_stellar_inflation_payments.py  
