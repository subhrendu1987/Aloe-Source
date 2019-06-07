#!/bin/bash
RED='\033[0;31m'
NC='\033[0m' # No Color
##################################################################################
#declare -A ips=( ["rpi1"]="192.168.2.1" ["rpi2"]="192.168.2.2" ["rpi3"]="192.168.2.3" ["rpi4"]="192.168.2.4" )
declare -A ips
eval "$(jq '.' hosts_file|sed 's/[:,]//g'| awk 'NR>2 {print last} {last=$0}'| awk '{print "ips["$2"]="  $1}')"
echo "" > /tmp/ping.out
echo "------------------------"
for ip in "${!ips[@]}"
do
	echo "------------------------"
	for pi in "${!ips[@]}"
	do
		if [ "$pi" == "$ip" ]
		then
		  	:
		  	#echo "Same IP" 
		else
			OUTPUT=$(bash ExecTo.sh "ping ${ips[$pi]} -c 2" "${ip}" "/tmp/ping.out")
			SUCCESS=$?
			if [[ $OUTPUT = *"EXECUTION_SUCCESSFULL"* ]]
			then
				RTT=$(grep "rtt " /tmp/ping.out)
				#echo "-----------"
				#cat /tmp/ping.out
				#echo "-----------"
				echo -e "${ip} -> ${pi}:\t${RTT}"
			else
				:
				echo -e "${RED}$ip -> $pi: Fail ${NC}"
			fi
			rm /tmp/ping.out
		fi
	done
done

