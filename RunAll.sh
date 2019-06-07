#!/bin/bash
###	ADD FINGER PRINTS AND HOST NAMES FOR EACH PI
TARGETDIR="/home/pi/flipperRPi3"
declare -A ips=()
eval "$(jq '.' hosts_file|sed 's/[:,]//g'| awk 'NR>2 {print last} {last=$0}'| awk '{print "ips["$2"]="  $1}')"
declare -a PIs=()
for pi in "${!ips[@]}";
do 
    PIs+=("$pi")
done
#echo "${PIs[@]}" # DEBUG
#declare -a PIs=("rpi1" "rpi2" "rpi3" "rpi4")

for pi in "${PIs[@]}"
do
	echo "**************$pi*****************"
	#Pull configuration from server
	sshpass -p 'raspberry' ssh pi@$pi "cd "$TARGETDIR"; sudo bash Run.sh"
	echo "**************DONE $pi*****************"
done
