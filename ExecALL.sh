#!/bin/bash
RED='\033[0;31m'
NC='\033[0m' # No Color
####################################################################################
declare -A ips=()
declare -A ret=()
eval "$(jq '.' hosts_file|sed 's/[:,]//g'| awk 'NR>2 {print last} {last=$0}'| awk '{print "ips["$2"]="  $1}')"
declare -a PIs=()
for pi in "${!ips[@]}";
do 
    PIs+=("$pi")
done
##################################################################
if [[ "$#" -lt 2 ]]; then
	OUTPUT_FILE="/dev/tty"
else
	OUTPUT_FILE=$2
	echo "" > ${OUTPUT_FILE}
fi
##################################################################
CMD=$1
echo -e ${RED}${CMD}${NC}
#comment(){
echo "**************$(date)*****************" >> $OUTPUT_FILE
for pi in "${PIs[@]}"
do
	#OUTPUT=$((sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@$pi $CMD;if [ $? -eq 0 ]; then echo -e "SUCCESSFULL: $CMD in $pi"; fi )  | tee -a $OUTPUT_FILE)
	#echo "Debug: bash ExecTo.sh \"${CMD}\" \"${pi}\" \"${OUTPUT_FILE}\""
	OUTPUT=$(bash ExecTo.sh "${CMD}" "${pi}" "${OUTPUT_FILE}")
	#echo $OUTPUT
	if [[ $OUTPUT = *"EXECUTION_SUCCESSFULL"* ]]; then
		ret[$pi]="SUCCESS"
		echo -e "${RED}EXECUTION_SUCCESSFULL${NC}"
	else
		ret[$pi]="FAILURE"
		echo -e "${RED}EXECUTION_ERROR${NC}"
	fi
	##########################################
	#echo "**************DONE ${pi}*****************" >> $OUTPUT_FILE
	
done
#}
##########################################
echo "**************Overall Status*****************"
paste -d"-" <(printf "%s\n" "${!ret[@]}") <(printf "%s\n" "${ret[@]}")
echo -e "**************${RED} Execution Complete ${NC}*****************"
