#!/usr/bin/python
'''
Collect Snapshot from all Rpis
'''
import datetime,subprocess,sys,os,json
import time,hashlib
import networkx as nx
import matplotlib.pyplot as plt
from random import randint
import random, re, commands
from time import sleep
from copy import copy
from datetime import datetime
from myLibrary import *
############################################################################
IPDICT=getDictFrom("hosts_file") ### Current directory should contain this file
piList=IPDICT.values()
#piList=['rpi1','rpi2','rpi3','rpi4']
#IPDICT={"192.168.2.1":"rpi1","192.168.2.2":"rpi2","192.168.2.3":"rpi3","192.168.2.4":"rpi4"}
############################################################################
folders="/home/pi/flipperRPi3/"
state_file=folders+"LOG/nodeInfo.json"
neighbor_file=folders+"LOG/neighbor_list.txt"
mac_file="LOG/MACREPO.json"
MACREPO=getDictFrom(mac_file)
############################################################################
def PrintToLog(filename,log_string):
	tstamp = datetime.datetime.utcnow()
	file_handler=open(filename,"a")
	tstamp = datetime.datetime.utcnow()
	log_string="%s\t %s\n"%(tstamp,logtext)
	file_handler.write(log_string)
	file_handler.close()
	return()
############################################################################
def PullFile(pi,Remotefile,Localfile="/tmp/tmp.json"):
	CMD="sshpass -p 'raspberry' scp -r pi@%s:%s %s" %(pi,Remotefile,Localfile)
	#CMD="sshpass -p 'raspberry' ssh pi@%s \"%s\"" %(pi,command)
	proc = subprocess.Popen(CMD,shell=True, stdout=subprocess.PIPE)
	(output, err) = proc.communicate()
	return
############################################################################
def ReCreateTopology(states):
	G=nx.DiGraph()
	G.add_nodes_from(states.keys())
	for n in G.nodes():
		for e in states[n].keys():
			IP=MACREPO[e]
			pi=IPDICT[IP]
			G.add_edge(n,pi)
	return(G)
############################################################################
def RemoteExec(pi,command):
	CMD="sshpass -p 'raspberry' ssh pi@%s \"%s\"" %(pi,command)
	proc = subprocess.Popen(CMD,shell=True, stdout=subprocess.PIPE)
	(output, err) = proc.communicate()
	return((output, err))
############################################################################
while(True):
	collect={}
	for pi in piList:
		print pi
		PullFile(pi,neighbor_file)
		tmp=getDictFrom("/tmp/tmp.json")
		collect[pi]=tmp
	printToLog("NeighborState_log.log",str(collect))
	G=ReCreateTopology(collect)
	nx.draw(G, with_labels = True,node_size=1000)
	#labels={n:n for n in G.nodes()}
	#pos=nx.spring_layout(G)
	#nx.draw_networkx_labels(G,pos,labels)
	#labels=nx.draw_networkx_labels(G,pos=nx.spring_layout(G))
	#plt.draw() 
	plt.show()
	print "Log Printed"
	time.sleep(5)

# Save collect to history with timestamp
