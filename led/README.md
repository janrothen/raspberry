# LED

### check_bitcoin_reachability.py
Checks if bitcoin full node is reachable from outside  


## Prerequisites

python3  
configparser==3.5.0  
python-dateutil==2.7.3  

## Installing

Create symlink to utils in this directory, or imports wont work  
Configure the scripts: config.conf  
  
sudo apt-get install build-essential unzip wget  
PiGPIO can be downloaded and installed via the command chain  
wget http://abyz.co.uk/rpi/pigpio/pigpio.zip && unzip pigpio.zip && cd PIGPIO && sudo make install  
  
Copy led.service to /etc/systemd/system  
