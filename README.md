# CAMM
## Collin's Automatic Machine Monitor
 
Welcome to CAMM!
(Collin's Automated Machine Monitor)
This little program will continually scan a subnet and keep an active list of computer up to date and remove anything it's been unable to contact for more than 90 days.
The pioneers used to drive this baby for miles.

A simple way to keep a list up to date is to use a cronjob to kick this script off as often as you'd like. I would recommend running a couple times a day. That way you can collect info from computers that run only at particular times.

Here's an example of how to run the program:

CAMM.py -s <subnetlist> ex. CAMM.py '10.0.0.0/24 192.168.2.0/24' 
Don't forget the quotes. They are a requirment if passing more than one subnet to scan.

### Vars
$RUNTIMER 
$SUBNETS