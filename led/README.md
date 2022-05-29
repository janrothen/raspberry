# LED

### led.py
Switches LED bar on according the time of the day and
with the color specified in config.conf

## Prerequisites
```
python3  
configparser==3.5.0  
python-dateutil==2.7.3  
```
## Installing

Create symlink to utils in this directory, or imports wont work  
Configure the scripts: `config.conf`


```
https://abyz.me.uk/rpi/pigpio/download.html
```
  ## Timers

Copy `led.service` to `/etc/systemd/system`  

File in `/etc/cron.d` to start/stops systemd service  
```
/etc/cron.d $ cat led  
15 19 * * * root /bin/systemctl start led 2>/tmp/error  
30 22 * * * root /bin/systemctl stop led 2>/tmp/error

15 06 * * * root /bin/systemctl start led 2>/tmp/error  
30 08 * * * root /bin/systemctl stop led 2>/tmp/error
```
