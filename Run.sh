#!/bin/bash
sudo su
####################################################################################
python StateUpdate.py &
python testLabel.py &
python controller_scheduler.py &
####################################################################################
printf "All daemon started\n" 
