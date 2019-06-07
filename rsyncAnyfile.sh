#!/bin/bash
declare -A ips
eval "$(jq '.' /home/user/GIT/flipperRPi3/common/hosts_file|sed 's/[:,]//g'| awk 'NR>2 {print last} {last=$0}'| awk '{print "ips["$2"]="  $1}')"


for fqdn in "${@}"
do
	echo "File sync:"$fqdn
	filename=$(basename "$fqdn")
	for pi in "${!ips[@]}"
	do		
		echo "------------------------------------"
		sshpass -p "raspberry"  rsync -avz -e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" --progress $fqdn pi@$pi:/tmp/$filename
		sshpass -p "raspberry" ssh -o StrictHostKeyChecking=no pi@$pi "sudo mv /tmp/$filename $fqdn"
		echo "Transfered to ->"$pi
	done
done
