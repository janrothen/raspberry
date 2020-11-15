# BitcoinAudit

https://twitter.com/BitcoinAudit

### run.py
Performs an audit of the total Bitcoin supply and tweets the current
block height and the current total BTC supply.

## Prerequisites
```
python3  
certifi==2020.6.20  
chardet==3.0.4  
future==0.18.2  
idna==2.10  
oauthlib==3.1.0  
python-bitcoinrpc==1.0  
python-twitter==3.5  
requests==2.24.0  
requests-oauthlib==1.3.0  
urllib3==1.25.11
```
## Installing
```
python3 -m venv venv  

pip install python-twitter  
pip install python-bitcoinrpc  
```
Create symlink to utils in this directory, or imports won't work  
Provide required configuration: `config.conf` 

Add the script to cron:  
```
crontab -e  

@daily /home/pi/raspberry/bitcoinaudit/run.py
```
