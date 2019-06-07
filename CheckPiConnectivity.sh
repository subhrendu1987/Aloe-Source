#!/bin/bash
RED='\033[0;31m'
NC='\033[0m' # No Color
##################################################################################
#declare -A ips=( ["rpi1"]="192.168.2.1" ["rpi2"]="192.168.2.2" ["rpi3"]="192.168.2.3" ["rpi4"]="192.168.2.4" )
declare -A ips
eval "$(jq '.' hosts_file|sed 's/[:,]//g'| awk 'NR>2 {print last} {last=$0}'| awk '{print "ips["$2"]="  $1}')"

echo "------------------------"
for pi in "${!ips[@]}"
do
	ping $pi -c 2 1>/dev/null 2>/dev/null
	SUCCESS=$?
	if [ $SUCCESS -eq 0 ]
	then
	  echo -e "$pi :\t Connected"
	else
	  :
	  echo -e "${RED}$pi :\t Fail ${NC}"
	fi
done

