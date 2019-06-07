#!/usr/bin/python
from __future__ import print_function
import datetime,subprocess,sys,os,json
import time,hashlib
from random import randint
import random, re, commands
from time import sleep
from copy import copy
from myLibrary import *
############################################################################
folders="/home/pi/flipperRPi3/"
state_file=folders+"LOG/nodeInfo.json"
neigborlist=folders+"LOG/neighbor_list.txt"
mac_file=folders+"LOG/MACREPO.json"
args=getDictFrom("args.json") ### Current directory should contain this file
############################################################################
try:
	MACREPO=getDictFrom(mac_file)
except IOError:
	PrintLog("File not found: ",colored(mac_file, 'green'))
	PrintLog("Run from server: ",colored("python CreateMacRepo.py;bash PushCodesToPI.sh", 'red'))
	sys.exit(1)
try:
	neighbor=getDictFrom(neigborlist) ## Run StateUpdate.py in case of error
except IOError:
	PrintLog("File not found: ",colored(neighborlist, 'green'))
	PrintLog("Run from server: ",colored("bash ExecALL.sh \"cd /home/pi/flipperRPi3; sudo python StateUpdate.py\"", 'red'))
ip_state={}
############################################################################
def getNeighborStates():
	state={}
	for mac in neighbor.keys():
		ip=neighbor[mac].values()[0]
		state[mac]=PullRemoteFile(ip,state_file)
		#state[mac]=PullRemoteFile(ip,state_file)
		#state[mac]=PullRemoteFileWget(ip,state_file)
		ip_state[ip]=state[mac]
	return(state)
############################################################################
def scheduler():
	CMD="sudo docker images |grep \"ryu-armv7\"|awk -F ' ' '{print $3}'"
	proc = subprocess.Popen(CMD,shell=True, stdout=subprocess.PIPE)
	(IMAGE_ID, err) = proc.communicate()
	CMD="docker ps |grep %s|awk -F ' ' '{print $1}'" %(IMAGE_ID.strip())
	proc = subprocess.Popen(CMD,shell=True, stdout=subprocess.PIPE)
	(CONTAINER_ID, err) = proc.communicate()
	mystate=getDictFrom(state_file)
	if (mystate['Label']=="NIB" and (len(CONTAINER_ID) <> 0)):
		MYIP=getSelfIP()
		#PrintLog("1: Controller already running in <%s>"%(MYIP))
		print(".",end=" ")
		#print("CONTAINER_ID:%s"%(CONTAINER_ID))
		#os.system("ovs-vsctl set-controller br tcp:%s:3366"%(MYIP))
	# Do nothing	Docker already running
	elif(mystate['Label']=="NIB" and (len(CONTAINER_ID) == 0)):	
		# Run docker
		MYIP=getSelfIP()
		PrintLog(colored("2: Start controller <%s>"%(MYIP),"green"))
		os.system("sh start_controller.sh")
		os.system("sudo python setRyuData.py")
	#Controller is already running
	elif(mystate['Label']<>"NIB" and (len(CONTAINER_ID) <> 0)):
		# Shut down controller. Find nearest controller and set ovs
		state=getNeighborStates()
		NIB_mac=[ mac for mac in state.keys() if state[mac]["Label"] == "NIB" ]
		if len(NIB_mac) >0:
			CTLR_IP = MACREPO[NIB_mac[0]]
			PrintLog(colored("3: Initiate controller at <%s>"%(CTLR_IP),"red"))
			os.system("ovs-vsctl set-controller br tcp:%s:3366"%(CTLR_IP))
			os.system("sudo python getRyuData.py")
			os.system("sh stop_controller.sh")
	else:
		pass
		# Docker already inactive
		# Do nothing
	return
############################################################################
def main():
	scheduler()
	sys.stdout.flush()
	sleep(15)
	return
#############################################################################
# For Daemon
#############################################################################
def do_something():
	if ("it" in args.keys())and (isinstance(args["it"],int)):
		for i in xrange(0,args["it"]):
			print( "[%d]"%(i),end=" ")
			sys.stdout.flush()
			main()
	else:
		for _ in infinite_sequence():
			main()
#############################################################################
def run():
	if(args["Daemon"]):
	    with daemon.DaemonContext():
			do_something()
	else:
		do_something()
#############################################################################
if __name__ == "__main__":
    run()
