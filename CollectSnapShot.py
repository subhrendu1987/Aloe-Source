#!/usr/bin/python
'''
Collect Snapshot from all Rpis
'''
from __future__ import print_function
import datetime,subprocess,sys,os,json
import time,hashlib
from random import randint
import random, re, commands
from time import sleep
from copy import copy
from datetime import datetime
from myLibrary import *
############################################################################
IPDICT=getDictFrom("hosts_file") ### Current directory should contain this file
piList=IPDICT.values()
############################################################################
folders="/home/pi/flipperRPi3/"
state_file=folders+"LOG/nodeInfo.json" # Generated from testLabel 
neigborlist=folders+"LOG/neighbor_list.txt" # Generated from StateUpdate
############################################################################
def PrintToLog(filename,log_string):
	tstamp = datetime.datetime.utcnow()
	file_handler=open(filename,"a")
	tstamp = getTimeStamp()
	log_string="%s\t %s\n"%(tstamp,logtext)
	file_handler.write(log_string)
	file_handler.close()
	return()
############################################################################
previous_log={}
while(True):
	collect={}
	controller={}
	state_color={}
	neighbors={}
	print("LEGENDS:",colored("Switch", 'red'),colored("NIB", 'green'),colored("Wait", 'yellow'))
	print("----------------------------------------------------------------------")
	for pi in piList:
		PullFileScp(pi,state_file)
		tmp=getDictFrom("/tmp/tmp.json")
		collect[pi]=tmp
		state_color[pi]='red' if(tmp['Label']== "Switch") else ('green' if(tmp['Label']== "NIB") else 'yellow')
		line=RemoteExec(pi,"sudo ovs-vsctl show")
		controller[pi]=getController(line)
		PullFileScp(pi,neigborlist)
		tmp=getDictFrom("/tmp/tmp.json")
		neighbors[pi]=[]
		#for mac in tmp.keys():
		#	for iface in tmp[mac].keys():
		#		neighbors[pi].append( "rpi"+tmp[mac][iface].split(".")[3]+"-"+iface)
		for iface in tmp.keys():
			neighbors[pi].append( "rpi"+tmp[iface].split(".")[3]+"-"+iface)
	print("----------------------------------------------------------------------")
	if(collect <> previous_log):
		for pi in state_color.keys():
			print(colored(pi, state_color[pi]),"--->",controller[pi], "\t-->",neighbors[pi])
		print("----------------------------------------------------------------------")
		print("debug:",collect,"\n",previous_log)
		printToLog("State_log.log",str(collect))
		#print "Log Printed"
	else:
		print(" . ")
	print ("[%s ]"%(getTimeStamp()),end="-")
	previous_log=collect
	time.sleep(5)

# Save collect to history with timestamp
