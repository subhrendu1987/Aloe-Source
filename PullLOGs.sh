#!/bin/bash
declare -A ips
eval "$(jq '.' /home/user/GIT/flipperRPi3/common/hosts_file|sed 's/[:,]//g'| awk 'NR>2 {print last} {last=$0}'| awk '{print "ips["$2"]="  $1}')"
## declare -A ips=( ["rpi1"]="192.168.2.1") ## Test
for pi in "${!ips[@]}"
do		
	echo "------------------------------------"
	sshpass -p "raspberry"  rsync -avzr -e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" --progress pi@$pi:/home/pi/flipperRPi3/LOG LOG/
	if [ -d "LOG/$pi" ]; then
		rm -rvf LOG/$pi
	fi
	mv LOG/LOG LOG/$pi
	echo "Transfered to ->"$pi
done
