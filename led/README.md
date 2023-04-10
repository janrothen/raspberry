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

Create symlink to utils in this directory, or imports won't work.
Configure the scripts: `config.conf`

Follow the pigpio installation instructions:
```
https://abyz.me.uk/rpi/pigpio/download.html
```
or
`sudo apt-get install pigpio`

## Timers

Copy `led.service` to `/etc/systemd/system`  

Create a file in `/etc/cron.d/led` to start/stop the systemd service . 
```
/etc/cron.d $ cat led  
15 19 * * * root /bin/systemctl start led 2>/tmp/error  
30 22 * * * root /bin/systemctl stop led 2>/tmp/error

15 06 * * * root /bin/systemctl start led 2>/tmp/error  
30 08 * * * root /bin/systemctl stop led 2>/tmp/error
```

### Status
```
pi@zero:~ $ systemctl status led.service
● led.service - LED Service
     Loaded: loaded (/etc/systemd/system/led.service; disabled; vendor preset: enabled)
     Active: active (running) since Mon 2023-04-10 13:19:34 CEST; 24s ago
   Main PID: 18876 (python3)
      Tasks: 3 (limit: 415)
        CPU: 14.115s
     CGroup: /system.slice/led.service
             ├─18876 /usr/bin/python3 -u led.py
             ├─21052 sh -c pigs p 17 3
             └─21053 pigs p 17 3
```
