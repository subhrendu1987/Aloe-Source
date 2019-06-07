#!/usr/bin/python
"""
Set rpiX as pi names, and run this code for generation of LOG/MACREPO.json. After generation, run PushCodeToPI with initilization.
"""
import datetime,subprocess,sys,os,json
import time,hashlib
from random import randint
import random, re, commands
from time import sleep
from copy import copy
from myLibrary import *
############################################################################
search_port='3366'
mac_file="LOG/MACREPO.json"
IPDICT=getDictFrom("hosts_file") ### Current directory should contain this file
piList=IPDICT.values()

#pilist=["rpi1","rpi2","rpi3","rpi4"]
HOSTS=['192.168.2.72','192.168.2.73']
############################################################################
def remove_item_from_list(l,item):
        clean_l=[ x for x in l if x <> item]
        return(clean_l)
############################################################################
def get_mac_list(lines):
        output_split=lines.split("\n")
        listofMac=remove_item_from_list(output_split,"")
        return(listofMac)
############################################################################
def getIP(lines):
	lines= lines.split("\n")
	inet=[ line for line in lines if ("inet" in line) ][0].strip()
	ip=re.findall( r'[0-9]+(?:\.[0-9]+){3}', inet )
	if(len(ip) <3):
		return(None)
	else:
		return(ip[0])
#############################################################################
def main():
	MACREPO={}
	for pi in piList:
		print "*****\t %s \t*****"%(pi)
		#lines=RemoteExec(pi,"tail -n +1 /sys/class/net/*/address")
		lines=RemoteExec(pi,"cat /sys/class/net/*/address")
		if (lines<> ''):
			macs=get_mac_list(lines)
			PullFileScp(pi,"/home/pi/ip.txt")
			ip=getDataFrom("/tmp/tmp.json")[0]
			#lines=RemoteExec(pi,"sudo ifconfig br")
			#ip=getIP(lines)
			if ip <> None:
				for mac in macs:
					if (mac == "00:00:00:00:00:00"):
						pass
					elif (mac in MACREPO.keys()) and (MACREPO[mac] <> ip) :
						print "MAC Duplicate Error: %s in %s and %s"%(mac,MACREPO[mac],ip)
						if(type(a)==type([])):
							MACREPO[mac]=[MACREPO[mac]]
						MACREPO[mac].append(ip)
					else:
						MACREPO[mac]=ip
			else:
				print("ERROR: IP NOT FOUND")
				sys.exit(1)
		else:
			print("ERROR: SSH ERROR/ MAC NOT FOUND")
			pass
			#sys.exit(1)
		print "*****\t %s \t*****"%(pi)
	putDictTo(mac_file,MACREPO)
	return
#############################################################################
if __name__ == '__main__':
    main()
