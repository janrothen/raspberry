# BitcoinAudit

https://twitter.com/BitcoinAudit

### run.py
Performs an audit of the total Bitcoin supply and tweets the current
block height and the current total BTC supply.

## Prerequisites
```
python3  
pip3
```
Other requirements will be installed from [requirements.txt](requirements.txt).

## Installing
```
python3 -m venv venv  
pip3 install -r requirements.txt  
```
Create symlink to utils in this directory, or imports won't work  
Provide required configuration: `config.conf` 

Add the script to cron:  
```
crontab -e  

@daily /home/pi/raspberry/bitcoinaudit/run.py
```
