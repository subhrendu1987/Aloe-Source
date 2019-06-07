import datetime,subprocess,sys,os,json
import time,hashlib
from random import randint
import random, re, commands
import requests,json
from time import sleep
from myLibrary import *
############################################################################
#piList=['rpi1','rpi2','rpi3','rpi4']
IPDICT=getDictFrom("hosts_file") ### Current directory should contain this file
piList=IPDICT.values()
############################################################################
folders="/home/pi/flipperRPi3/"
state_file=folders+"LOG/nodeInfo.json"
#log=folders+"LOG/controllerMarker.txt"
############################################################################
def getCtlrData(ctlr,stats_cmd):
	URL="http://%s:9000/stats/%s"%(ctlr,stats_cmd)
	print "URL:"+URL
	data = requests.get(URL)
	return(data.json())
############################################################################
def getIPFromHostName(ctlr):
	CMD="grep %s /etc/hosts | awk '{print $1}'"%(ctlr)
	proc = subprocess.Popen(CMD,shell=True, stdout=subprocess.PIPE)
	(IP, err) = proc.communicate()
	return(IP)
############################################################################
ctlr_list=[];collect={}
for pi in piList:
	PullFileScp(pi,state_file)
	tmp=getDictFrom("/tmp/tmp.json")
	collect[pi]=tmp
ctlr_list=[k for k in collect.keys() if(collect[k]['Label']== "NIB")]
ctlr_ip=[getIPFromHostName(ctlr).strip() for ctlr in ctlr_list]

#data=getCtlrData(ctlr_ip[0],"switches")
#data=getCtlrData(ctlr_ip[0],"flow/1")
############################################################################
print ("--------------------[%s ]----------------"%(getTimeStamp()))