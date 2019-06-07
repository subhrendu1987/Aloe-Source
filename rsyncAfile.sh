#!/bin/bash
declare -A ips
eval "$(jq '.' /home/user/GIT/flipperRPi3/common/hosts_file|sed 's/[:,]//g'| awk 'NR>2 {print last} {last=$0}'| awk '{print "ips["$2"]="  $1}')"

for filename in "${@}"
do
	echo "File sync:"$filename
	for pi in "${!ips[@]}"
	do		
		echo "------------------------------------"
		sshpass -p "raspberry"  rsync -avz -e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" --progress $filename pi@$pi:/home/pi/flipperRPi3/$filename
		echo "Transfered to ->"$pi
	done
done
