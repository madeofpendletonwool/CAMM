# CAMM aka Collin's Automatic Machine Monitor
 
### Welcome to CAMM!

This little program will continually scan a subnet and keep an active list of computers up to date. It removes anything it's been unable to contact for more than 90 days.
The pioneers used to drive this baby for miles.

A simple way to keep a list up to date is to use a cronjob to kick this script off as often as you'd like. I would recommend running a couple times a day. That way you can collect info from computers that run only at particular times.

Here's an example of how to run the program:

CAMM.py -s <subnetlist> ex. CAMM.py '10.0.0.0/24 192.168.2.0/24' 
Don't forget the quotes. They are a requirment if passing more than one subnet to scan.

You don't have to worry about much of this though because I've dockerized the whole thing which allows for really quick and easy access to the program. The recommended way to use it at this point is to pull using a docker compose file. I've included a compose template to go off. 

### Using CAMM

Go ahead and begin by pulling the repo 
```
git clone https://github.com/madeofpendletonwool/CAMM.git
```
Next, take a look at the files. The ones of note are a dockerfile (used to build the container), the main python program, and a docker compose file (used to setup, pull, and run the container in your environment.)
So the last one is the one you need to make adjustments to. Open up the compose file and these lines are what you need to change
```
      - /your/data/path/data:/data
      - SUBNETS='subnet1 subnet2 subnet3' 
      - RUNTIMER=''0 */6 * * *''
```
First of all, run timer is simply cron syntax for how often you want the program to run. By default I have it set to every 6 hours. Feel free to leave that if you'd like or head over to https://crontab.guru/ and create your own cron for how often you want to run. Just repace that line in the compose file. Leave the two ' in place though. Those are important. 

Next, subnets. That's easy, put as many subnets in as you'd like to scan. Seperate them with spaces. ''10.0.0.0/24 192.168.2.0/24 172.16.0.0/24''. Again, leave the double '.

Last, the volume. This tells the container where to mount the folder to put the scan data. I'd usually do something like /home/user/camm/data. So it would look like this - /home/user/camm/data:/data. Then you can also clone the repo itself into /home/user/camm. That keeps things organized.

Now that you have everything in place simply run 
```
sudo docker-compose up
```
in the same folder that your compose file is located. That's all there is to it. Now wait and keep camm running. It'll keep machines up to date and continually update the Computer_list.txt file with everything it finds. 