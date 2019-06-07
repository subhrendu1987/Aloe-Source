#!/bin/bash
#pID=`ps -ef|grep "python -m SimpleHTTPServer"|awk -F ' ' 'NR==1{print $2}'`
#kill -9 $pID

inames=$(ovs-vsctl show|grep Port | grep -v "Port br"|awk '{print substr($2, 2, length($2)-2)}')
#inames=$(ip -o link show | awk '{if (NR!=1) {print substr($2, 1, length($2)-1)}}' |grep "eth*" |grep -v "veth*")
#inames=$(ip -o link show | sed -rn '/^[0-9]+: eth/{s/.: ([^:]*):.*/\1/p}')
#ovs-vsctl del-br br
for iface in $inames
do
        ovs-vsctl --if-exists del-port br $iface
        ip addr flush dev $iface
        echo "$iface:$?"
done
echo "Stopping ovs $(date)" >> /home/pi/onReboot.txt
