#!/usr/bin/python
"""
Detect Neighbor Topology using lldp and arp. Not in use
"""
import os, sys, argparse, random, re, subprocess, commands
#from subprocess import Popen, PIPE, call
from time import sleep
#import termcolor as T
from copy import copy
import re
import json
#############################################################################
IP="127.0.0.1"
PORT="6633"
#############################################################################
def getNeighbors2():
        ''' Get neighbor list using fping and ARP'''
        CMD="fping -c 1 -g 192.168.2.0/24 2> /dev/null"
        proc = subprocess.Popen(CMD,shell=True, stdout=subprocess.PIPE)
        (out, err) = proc.communicate()
        #print out
        output_split=out.split("\n")
        listofIPs=[i.split(" ")[0] for i in (output_split) if i.split(" ")[0] <> ""]
        CMD2="arp -n |grep \"192.168.2\" | grep \"ether\""
        proc2 = subprocess.Popen(CMD2,shell=True, stdout=subprocess.PIPE)
        (out2, err2) = proc2.communicate()
        output2_split=out2.split("\n")
        neighbor={i.split()[2]:{i.split()[4] :i.split()[0]} for i in output2_split if len(i)>1 }
        return(neighbor)
#############################################################################
def get_self_mac():
        CMD="ifconfig"
        proc = subprocess.Popen(CMD,shell=True, stdout=subprocess.PIPE)
        (out, err) = proc.communicate()
        output_split=out.split("\n")
        listofMac=[j.split()[4] for i,j in enumerate(output_split) if "HWaddr" in j]
        return(listofMac)
#############################################################################
def getNeighbors():
        ''' Get neighbor list using lldpcli'''
        selfMacs=get_self_mac()
        CMD="lldpcli show neighbors"
        proc = subprocess.Popen(CMD,shell=True, stdout=subprocess.PIPE)
        (out, err) = proc.communicate()
        #print out
        output_split=out.split("\n")
        listofMacPos=[i for i,j in enumerate(output_split) if "PortID:" in j]
        listofIfacePos=[i for i,j in enumerate(output_split) if "Interface:" in j]
        neighbor={}
        for i,j in enumerate(listofMacPos):
                ifaceLine=output_split[listofIfacePos[i]]
                macLine=output_split[j]
                iface=re.split(': |, ',ifaceLine)[1].strip()
                mac=re.split(': |, ',macLine)[1].strip().replace("mac ","")
                if ("eth" in iface and mac not in selfMacs):
                        neighbor[mac]=iface
        temp={}
        neighbor2=getNeighbors2()
        #os.system("fping -c 1 -g 192.168.2.0/24 2> /dev/null > /dev/null")
        for mac in neighbor.keys():
	        IP=commands.getoutput("arp -n|grep -i %s|awk '{print $1}'"%(mac))
	        if IP=="":
	        	
	        temp[neighbor[mac]]=IP
	        neighbor[mac]=temp
	        temp={}
	return(neighbor)
############################################################################
neighbor=getNeighbors()
#neighbor2=getNeighbors2()
file_handler=open("neighbor_list.txt","wb")
json.dump(neighbor, file_handler)
file_handler.flush()
file_handler.close()


