 #!/bin/bash
#write out current crontab
crontab -l > CAMMcron
#echo new cron into cron file
echo "$1 /usr/bin/python3 /data/CAMM.py" >> CAMMcron
#install new cron file
crontab CAMMcron