#!/bin/bash
RED='\033[0;31m'
NC='\033[0m' # No Color
##################################################################################################
###	ADD FINGER PRINTS AND HOST NAMES FOR EACH PI
SERVIP=`python -c 'import socket; print socket.gethostbyname("myip")'`
SERVPORT="7512"
TARGETDIR="/home/pi/flipperRPi3"
#process_id=`/bin/ps -aux| grep "SimpleHTTPServer" | grep -v "grep" | awk '{print $2}'`
#chrlen=${#process_id}
#printf $chrlen","$process_id"\n"
#if [ "$chrlen" -gt 0 ]
#then
#	echo "HTTP server is getting killed"
#	kill -9 $process_id
#fi
#python -m SimpleHTTPServer $SERVPORT > /dev/null &
#process_id=`/bin/ps -aux| grep "SimpleHTTPServer" | grep -v "grep" | awk '{print $2}'`
#WGET="rm -Rf "$TARGETDIR";wget -r --no-parent http://"$SERVIP":"$SERVPORT"/ ; mv "$SERVIP"\:"$SERVPORT" "$TARGETDIR
##################################################################################################
###declare -a PIs=("rpi1" "rpi2" "rpi3" "rpi4")
#declare -A ips=( ["rpi1"]="192.168.2.1" ["rpi2"]="192.168.2.2" ["rpi3"]="192.168.2.3" ["rpi4"]="192.168.2.4" )
declare -A ips
eval "$(jq '.' hosts_file|sed 's/[:,]//g'| awk 'NR>2 {print last} {last=$0}'| awk '{print "ips["$2"]="  $1}')"

###for pi in "${PIs[@]}"
for pi in "${!ips[@]}"
do
	echo "**************$pi*****************"
	### Use once or if configuration is modified
	### Pull configuration from server.
	#sshpass -p 'raspberry' ssh pi@$pi "touch $pi"
	#sshpass -p 'raspberry' ssh pi@$pi "sudo wget http://172.16.112.141/proxy/environment -O /etc/environment"
	#sshpass -p 'raspberry' ssh pi@$pi "sudo wget http://172.16.112.141/proxy/apt.conf -O /etc/apt/apt.conf"
	#sshpass -p 'raspberry' ssh pi@$pi "if grep -q 'source /etc/environment' ~/.bashrc; then echo '.bashrc not modified';else echo 'source /etc/environment' >> test;  fi"
	#sshpass -p 'raspberry' scp -o StrictHostKeyChecking=no LOG/MACREPO.json root@$pi:$TARGETDIR/LOG/MACREPO.json
	echo "************** Code is being pushed*****************"
	### Set bridge IP
	echo ${ips[$pi]}
	echo ${ips[$pi]} | sshpass -p 'raspberry' ssh root@$pi -o StrictHostKeyChecking=no "cat > /home/pi/ip.txt"
	sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no root@$pi "sudo touch /home/pi/${pi};sudo chmod 777 -Rv /home/pi/${pi};mkdir -p ${TARGETDIR}/LOG"
	sshpass -p 'raspberry' scp -r -o StrictHostKeyChecking=no ./*.txt root@$pi:$TARGETDIR/
	echo "**************DONE $pi*****************"
done
kill -9 $process_id
bash rsyncAfile.sh *.sh
bash rsyncAfile.sh *.py
bash rsyncAfile.sh *.json
bash rsyncAfile.sh LOG/MACREPO.json
bash rsyncAfile.sh LOG/nodeInfo.json
bash ExecALL.sh "sudo chmod 777 -R /home/pi/flipperRPi3;sudo chmod 777 -R /home/pi/ip.txt;"
##################################################################################################
echo -e "EXEC: ${RED}cd ../flipperRPi3/ ${NC}"
