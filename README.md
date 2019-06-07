<pre>
                            |---------rpi1
                            |
server-------- Wlan0--------|---------rpi2
                            |
                            |---------rpi3
                            |
                            |---------rpi4
               Topology
</pre>
-------------------------------------------------------------------------------------
## How to add new rpi[x] ##
### Set ssh key ###
Set-up proxy for the newly connected node and make sure it is configured with proxy. Bypass server proxy for newly connected rpi <br />
Add entry to /etc/hosts with rpi{x} and its wlan IP <br />
Add hosts_file entry for rpi{x} <br />
### Install 'Required Commands' ###
### Change 'InitTerm.sh' ###
### Add 'Set title' to ~/.bashrc ###
### Install docker from script ###
### Install softwares ###
	openvswitch-switch, openvswitch-common, lldpd, fping, sshpass, jq <br />
### Install python libraries ###
	python-daemon, python-termcolor, python-pycurl <br />
	curlify <br />
### Build ryu-docker ###
	Copy image <br />
	load image using <br />
		docker image load -i ryu-armv7.tar <br />
		sudo docker tag d53fe33f37fe ryu-armv7 <br />
### Install python libraries ###
## Consult allCommands.txt for viewing workflow ##
## Required Commands ##
lldp-cli, fping, sshpass, docker, jq

## Required Python Libraries ##
python-daemon, python-termcolor, python-pycurl
### MACREPO.txt ###
Contains MAC and IP dictionary
### pi@rpi[x]:/home/pi/ip.txt ###
Contains bridge IP address. Can be changed from PushCodesToPI.sh file
### pi@rpi[x]:/home/pi/RPI[x] ###
To easy initialization of gnome terminals its title.

## bash PushCodesToPI.sh ##
After updating code run this script to push codes to individual Rasberry Pi. This also updates the ip address associated to the rpi bridges.

## bash ExecALL.sh ##
Run from server. Executes some commands to each pi.
e.g.
```
bash ExecALL.sh "sudo bash /home/pi/flipperRPi3/stop-ovs.sh"
bash ExecALL.sh "sudo bash /home/pi/flipperRPi3/start-ovs.sh"
```
## bash start-ovs.sh ##
Script to start OVS and HTTP Server
```
bash ExecALL.sh "sudo bash /home/pi/flipperRPi3/start-ovs.sh"
```

## bash stop-ovs.sh ##
Script to Stop OVS and HTTP Server
```
bash ExecALL.sh "sudo bash /home/pi/flipperRPi3/stop-ovs.sh"
```
## python CreateMacRepo.py ##
Create LOG/MACREPO.json file. Should be run from server. After running it push the codes.

## test.sh ##
Runs testLabel.py for checking configuration. Not required now.

## bash pingall.sh ##
Pingtests all switches

## bash CheckPiConnectivity.sh ##
Check wlan connectivity of pis


## python CollectSnapShot.py ##
Logs system state information. Run from Outside Server.

### /home/rpi/flipperRPI3/args.json ###
For each pi. Contains Daemon mode (True or False) and number of itarations for StateUpdate and testLabel.
`e.g. {"Daemon": false, "it": 10}`

## python StateUpdate.py ##
Finds local topology and stores it to "LOG/neighbor_list.txt". Don't keep it running for static topology.
e.g. 
```
bash ExecALL.sh "cd /home/pi/flipperRPi3; sudo python StateUpdate.py"
```
## python testLabel.py ##
Checks neighbor states and runs flipper readjustment framework. Updates "LOG/nodeInfo.json". If it throws file missing error, try running StateUpdate.py.

## python controller_scheduler.py ##
Checks own states periodically. Depending on it's state this script invokes `start_controller.sh` or `stop_controller.sh` . 
```
python controller_scheduler.py
```
[Some error]

## sh start_controller.sh ##
Starts docker with ryu. [Some error]

## sh stop_controller.sh ##
Stops docker with ryu. [Some error]

## bash CleanAllDockers.sh ##
Kills and removes all dockers. This is useful if unnecessary dockers are genarated.
```
bash ExecALL.sh "sudo bash /home/pi/flipperRPi3/CleanAllDockers.sh"
```

## Important commands for initialization##
For time sync:
```
bash ExecALL.sh "sudo date -s \"$(wget -qSO- --max-redirect=0 google.com 2>&1 | grep Date: | cut -d' ' -f5-8)Z\""
```


## To Start OVS service (issue command from server): ##
```
bash ExecALL.sh "sudo bash /home/pi/flipperRPi3/stop-ovs.sh"
bash ExecALL.sh "sudo bash /home/pi/flipperRPi3/start-ovs.sh"
```

## Check StateUpdate: ##
```
bash ExecALL.sh "cd /home/pi/flipperRPi3/; nohup sudo python StateUpdate.py &"
```
## Check Controller Running status: ##
```
bash ExecALL.sh "sudo docker ps -a"
```
## python CollectSnapShot.py ##
Validate the states of the pis.

## SOME EXTRA COMMANDS ##
```
bash ExecALL.sh "sudo chmod 777 -Rv /home/pi/flipperRPi3"
bash ExecALL.sh "sudo ovs-ofctl dump-flows br"

```
### Remove lock from apt-get ###
```
sudo rm /var/lib/apt/lists/lock; sudo rm /var/cache/apt/archives/lock; sudo rm /var/lib/dpkg/lock
```
### Opens tabs with ssh login to each pi ###
```
gnome-terminal \
	--tab -e "sshpass -p 'raspberry' ssh pi@rpi1 -t \"cd flipperRPi3;sudo -E bash\"" \
	--tab -e "sshpass -p 'raspberry' ssh pi@rpi2 -t \"cd flipperRPi3;sudo -E bash\"" \
	--tab -e "sshpass -p 'raspberry' ssh pi@rpi3 -t \"cd flipperRPi3;sudo -E bash\"" \
	--tab -e "sshpass -p 'raspberry' ssh pi@rpi4 -t \"cd flipperRPi3;sudo -E bash\""
```
[ Opens tabs with ssh login to each pi]
### Set interface delay and bandwidth ###
```
bash ExecALL.sh "for iface in \$(netstat -i | awk -F ' ' '{print $1}'| grep \"eth\");do sudo tc qdisc show dev \${iface}; done"
bash ExecALL.sh "sudo tc qdisc add dev br root netem delay 100ms 10ms 25%"
bash ExecALL.sh "sudo tc qdisc add dev br parent 1:1 handle 10: tbf rate 1mbit buffer 1600 limit 3000"
bash ExecALL.sh "for iface in \$(netstat -i | awk -F ' ' '{print $1}'| grep \"eth\");do tc qdisc delete dev \${iface} root; echo \${iface}; done"
bash ExecALL.sh "" # Delete delay rules
```
### Set dates to all pi ###
```
bash ExecALL.sh "sudo date -s \"$(wget -qSO- --max-redirect=0 google.com 2>&1 | grep Date: | cut -d' ' -f5-8)Z\""
bash ExecALL.sh "sudo cp /usr/share/zoneinfo/Asia/Kolkata /etc/localtime"
``` 

### Set title ###
[ ### Add this function to ~/.bashrc]
```
source /etc/environment
set-title(){
	ORIG=$PS1
	if [ -z "$1"]
		then TITLE="\e]2;$(echo $(ls /home/pi/rpi*) | cut -d" " -f1 |xargs -n 1 basename)\a"
	else
		TITLE="\e]2;$@\a"
	fi
	PS1=${ORIG}${TITLE}
}
set-title
```
[ Set terminal title with RPI name]
### Rsync ###
rsync options source destination
