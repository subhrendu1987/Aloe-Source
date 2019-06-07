#!/bin/bash

bash ExecALL.sh "cd /home/pi/flipperRPi3/; nohup sh -c \"echo ' ' && date && sudo python StateUpdate.py\" >> LOG/StateUpdate.nohup &"
sleep 10
bash ExecALL.sh "cd /home/pi/flipperRPi3/; nohup sh -c \"echo ' ' && date && sudo python testLabel.py\" >> LOG/testLabel.nohup &"
sleep 60
bash ExecALL.sh "cd /home/pi/flipperRPi3/; nohup sh -c \"echo ' ' && date && sudo python controller_scheduler.py\" >> LOG/controller_scheduler.nohup &"

