 #!/bin/bash
#write out current crontab
# crontab -l > CAMMcron
#echo new cron into cron file
# echo "$1 /usr/bin/python3 /data/CAMM.py $2" >> CAMMcron
(crontab -l 2>/dev/null; echo "$1 /usr/bin/python3 /data/CAMM.py $2") | crontab -
#install new cron file
# crontab CAMMcron