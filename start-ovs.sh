#!/bin/bash
#ps -aux|grep python
#pID=`ps -ef|grep "python -m SimpleHTTPServer"|awk -F ' ' 'NR==1{print $2}'`
#kill -9 $pID
#python -m SimpleHTTPServer 8080 > /dev/null &
IP=$(cat "/home/pi/ip.txt")
inames=$(ip -o link show | awk '{if (NR!=1) {print substr($2, 1, length($2)-1)}}' |grep "eth*"|grep -v "veth*")
#inames=$(ip -o link show | sed -rn '/^[0-9]+: eth/{s/.: ([^:]*):.*/\1/p}')
ID=$( echo $IP|awk -F'.' '{print $4}')
ID=$(expr $ID + 0)
##################################################################################
#comment(){
if [ $ID == 0 ]
then
	printf "Invalid IP address assigned. Change bridge IP."
else
	ID=$( printf '%02d' $ID )
fi
# Leave eth0 as it is
for iface in $inames
do
	sudo ifconfig $iface down
	ifaceno=$(echo $iface| grep -o '[0-9:]*')
	ifaceno=$(expr $ifaceno + 1)
	ifaceno=$( printf '%02d' $ifaceno )
	HWaddr="00:00:00:00:"$ID":"$ifaceno
	sudo ifconfig $iface hw ether $HWaddr
	sudo ifconfig $iface up
	echo 'MAC changed'$HWaddr
done
#}
#################################################################################
sudo ovs-vsctl show |grep "Bridge br"
if [ $? -eq 0 ]
then
	echo "Bridge exists"
	#/etc/init.d/openvswitch-switch restart
else
	ovs-vsctl add-br br
fi
#################################################################################
ports=$(ovs-vsctl)
for iface in $inames
do
	if [[ ${ports} = *"${iface}"* ]]; then
		echo "${iface} already in bridge"
	else
		ovs-vsctl add-port br $iface
		echo "$iface port added:$?"
	fi
	ip addr flush dev $iface
	echo "$iface dev flushed:$?"
done
#ovs-vsctl set bridge br protocols=OpenFlow10,OpenFlow12,OpenFlow13
#sudo ip link set dev br up
ifconfig br $IP
sudo ovs-vsctl set bridge br stp_enable=true
ovs-vsctl set-controller br tcp:192.168.2.1:3366
echo "Starting ovs $(date)" >> /home/pi/onReboot.txt
ovs-vsctl show
