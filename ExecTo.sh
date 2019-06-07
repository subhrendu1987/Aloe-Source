#!/bin/bash
CMD=$1
pi=$2
################################
RED='\033[0;31m'
NC='\033[0m' # No Color
###	ADD FINGER PRINTS AND HOST NAMES FOR EACH PI
declare -A ips=()
declare -A ret=()
eval "$(jq '.' hosts_file|sed 's/[:,]//g'| awk 'NR>2 {print last} {last=$0}'| awk '{print "ips["$2"]="  $1}')"
declare -a PIs=()
for pi in "${!ips[@]}";
do 
    PIs+=("$pi")
done
##################################################################
if [[ "$#" -eq 0 ]]; then
	echo "bash ExecTo.sh \"CMD\" \"Rpix\""
	exit 1
fi
##################################################################
if [[ "$#" -lt 3 ]]; then
	OUTPUT_FILE="/dev/tty"
else
	OUTPUT_FILE=$3
fi
##################################################################
echo ${2}":"${CMD} >> $OUTPUT_FILE
echo "**************${2}*****************" >> $OUTPUT_FILE
#Pull configuration from server
#echo "Debug: sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no root@${2} ${CMD}" >> $OUTPUT_FILE

OUTPUT=$((sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no root@${2} ${CMD};if [ $? -eq 0 ]; then echo -e "SUCCESSFULL: $CMD in $pi"; fi )  | tee -a $OUTPUT_FILE)
if [[ $OUTPUT = *"SUCCESSFULL"* ]]; then
	ret[$pi]="SUCCESS"
	echo -e "${RED}EXECUTION_SUCCESSFULL${NC}"
else
	ret[$pi]="FAILURE"
	echo -e "${RED}EXECUTION_ERROR${NC}"
fi	  		
echo "**************DONE ${2} *****************"
#done
#echo "**************Overall Status*****************"
#paste -d"-" <(printf "%s\n" "${!ret[@]}") <(printf "%s\n" "${ret[@]}")
#echo -e "**************${RED} Execution Complete ${NC}*****************"
#**************rpi8*****************
#**************DONE rpi8*****************
