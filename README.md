# What is this? #

This script is for tvheadend.
It updates all autorec entries to fix/workaround a bug where recording times (start after/start before) will be ignored after a restart of tvheadend. By updating (without changing) all autorecs, the wrong schedules will disappear.

Bugs:
    https://tvheadend.org/issues/5056 and  https://tvheadend.org/issues/4454

# Installation #

You need python3 (```sudo apt-get install python3```) to run this script.

Run this as hts user (sudo su hts):
```
    cd ~
    git clone https://github.com/arneman/tvh_upd_autorec
    cd tvh_upd_autorec
    /bin/sh ./setup.sh
```    
# Setup #

Before you start, enter your server settings (hostname, username, password) in ```config.json``` file.
Username and password is not mandatory (if your server allows access without auth). In this case, just delete (or ignore) those 2 lines

I've created a cron job on my tv server that is running the script after each reboot (with 30s delay):

Run this as hts user (sudo su hts):
```
crontab -l > mycron
#new cron into cron file
echo "@reboot sleep 30 && python3 ~/tvh_upd_autorec/main.py > /dev/null" >> mycron
#install new cron file
crontab mycron
rm mycron
```

### Credits ###

I'm using the tvh python lib from https://github.com/tvheadend/tvheadend/tree/master/lib/py/tvh
I was inspired by https://github.com/tvheadend/python-htspclient (copied a few lines)

