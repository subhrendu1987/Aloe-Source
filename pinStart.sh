#!/bin/bash

declare -A ips=()
eval "$(jq '.' hosts_file|sed 's/[:,]//g'| awk 'NR>2 {print last} {last=$0}'| awk '{print "ips["$2"]="  $1}')"
declare -a PIs=()
for pi in "${!ips[@]}";
do 
    PIs+=("$pi")
done


for pi in "${!ips[@]}";do
	#sshpass -p "raspberry" scp -o StrictHostKeyChecking=no -r ~/.bashrc pi@$pi:/home/pi/.bashrc
	#sshpass -p "raspberry" scp -o StrictHostKeyChecking=no -r /etc/environment pi@$pi:/home/pi/environment
	#sshpass -p "raspberry" scp -o StrictHostKeyChecking=no -r /etc/apt/apt.conf pi@$pi:/home/pi/apt.conf
	#sshpass -p "raspberry" ssh -o StrictHostKeyChecking=no pi@$pi "sudo mv /home/pi/apt.conf /etc/apt/apt.conf"
	#sshpass -p "raspberry" ssh -o StrictHostKeyChecking=no pi@$pi "sudo mv /home/pi/environment /etc/environment"
	#sshpass -p "raspberry" scp -v -o StrictHostKeyChecking=no -r ../common/* pi@$pi:/home/pi/flipperRPi3/
	#sshpass -p "raspberry" scp -o StrictHostKeyChecking=no ../DOCKERIMAGE pi@$pi:/home/pi/DOCKER_RYU
	#sshpass -p "raspberry" rsync -avz -e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" --progress ../DOCKERIMAGE pi@$pi:/home/pi/DOCKER_RYU
	sshpass -p "raspberry" scp -o StrictHostKeyChecking=no /home/pi/checkSystemParams.sh pi@${ips[$counter]}:/home/pi/
	sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@${ips[$counter]} "sudo killall -9 checkCoreTemp.sh && rm checkCoreTemp.sh && sudo nohup bash checkSystemParams.sh >> systemHealth.nohup &"
echo $pi
done
echo "All Done"
#######################################################################################################################################################
	#sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@${ips[$counter]} "sudo chown pi -R /home/pi/"
	#sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@${ips[$counter]} "sudo chmod +x /home/pi/"
	#sshpass -p "raspberry" scp -o StrictHostKeyChecking=no /home/pi/start-ovs.sh pi@${ips[$counter]}:/home/pi/
	#sshpass -p "raspberry" scp -o StrictHostKeyChecking=no /home/pi/stop-ovs.sh pi@${ips[$counter]}:/home/pi/
	#sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@${ips[$counter]} "chmod +x flipper/start-ovs.sh"
	#sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@${ips[$counter]} "chmod +x flipper/stop-ovs.sh"
	#sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@${ips[$counter]} "cd flipper && sudo ./stop-ovs.sh"
	#sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@${ips[$counter]} "cd flipper && sudo ./start-ovs.sh"
	#sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@$pi "sudo ifconfig"
	#sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@${ips[$counter]} "rm ip.txt && echo "${br[$counter]}">>ip.txt" 
	#sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@${ips[$counter]} "sudo nohup bash start-ovs.sh&"
	#sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@${ips[$counter]} "sudo ovs-vsctl show"
	#sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@${ips[$counter]} "sudo rmdir LOG/"
	#sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@${ips[$counter]} "mkdir LOG && touch LOG/MACREPO.json"
	#sshpass -p "raspberry" scp -o StrictHostKeyChecking=no -r /home/pi/LOG/ pi@${ips[$counter]}:/home/pi/flipper/
       	#sshpass -p "raspberry" scp -o StrictHostKeyChecking=no /home/pi/args.json pi@${ips[$counter]}:/home/pi/args.json
	#sshpass -p "raspberry" scp -o StrictHostKeyChecking=no /home/pi/flipper/testLabel.py pi@${ips[$counter]}:/home/pi/flipper/testLabel.py
	#sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@${ips[$counter]} "sudo nohup python flipper/StateUpdate.py&"
	#sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@${ips[$counter]} "sudo nohup python flipper/controller_scheduler.py&"
	#sshpass -p "raspberry" scp -o StrictHostKeyChecking=no /home/pi/flipper/controller_scheduler.py pi@${ips[$counter]}:/home/pi/flipper/
	#sshpass -p "raspberry" scp -o StrictHostKeyChecking=no /home/pi/flipper/getRyuData.py pi@${ips[$counter]}:/home/pi/flipper/
	#sshpass -p "raspberry" scp -o StrictHostKeyChecking=no /home/pi/flipper/setRyuData.py pi@${ips[$counter]}:/home/pi/flipper/
	#sshpass -p "raspberry" scp -o StrictHostKeyChecking=no /home/pi/flipper/start_controller.sh pi@${ips[$counter]}:/home/pi/flipper/
	#sshpass -p "raspberry" scp -o StrictHostKeyChecking=no /home/pi/flipper/myLibrary.py pi@${ips[$counter]}:/home/pi/flipper/

