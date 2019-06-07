#!/usr/bin/python
from __future__ import print_function
import datetime,subprocess,sys,os,json
import time,hashlib
from random import randint
import random, re, commands
from time import sleep
from copy import copy
import argparse
import daemon
from myLibrary import *
############################################################################
search_port='3366'
folders="/home/pi/flipperRPi3/"
state_file=folders+"LOG/nodeInfo.json"
log_file=folders+"LOG/log.txt"
output={}
interfaceFile="/sys/class/net/%s/operstate"
HISTORY={}
IP="127.0.0.1"
PORT="6633"
HOSTS=['192.168.2.72','192.168.2.73']
mac_file=folders+"LOG/MACREPO.json"
MACREPO=getDictFrom(mac_file)
args=getDictFrom("args.json") ### Current directory should contain this file
############################################################################
def detectInterfaceChange(operstate):
	''' Interface change handler '''
	detect= "No Changes"
	flag=0
	if ("operstate" not in HISTORY.keys()):
		detect= "Initialize"
		flag=1
	elif(hash_dict(HISTORY["operstate"]) <> hash_dict(operstate)):
		detect="Interface change detected"
		flag=1
	HISTORY["operstate"]=operstate
	return(detect,flag)
############################################################################
def detectControllerChange(op):
	''' Controller change handler '''
	flag=0
	isConnected =True if [i.split()[1] for i in op if "is_connected:" in i]==["true"] else False
	detect="No change"
	if ("controller" not in HISTORY.keys()):
		detect= "Initialize"
		flag=1
	elif(HISTORY["controller"]<>isConnected):
		detect="Controller change detected"
		flag=1
	HISTORY["controller"]=isConnected
	return(detect,flag)
############################################################################
def detectChange():
	''' Change events handler'''
	op=os.popen("ovs-vsctl show").read()
	op=op.split("\n")
	detectC,flagC=detectControllerChange(op)
	opTrim=[i.split()[1] for i in op if "Interface" in i]
	IfaceList=[i.replace("\"","") for i in opTrim if "eth" in i]
	CMD="cat %s"%(interfaceFile)
	operstate={}
	for iface in IfaceList:
		operstate[iface]=True if ("up" in os.popen(CMD%(iface)).read()) else False
	detectS,flagS=detectInterfaceChange(operstate)
	add_to_log("ctlr:%s\tiface:%s"%(detectC,detectS))
	#PrintLog("ctlr:%s\tiface:%s"%(detectC,detectS))
	return(flagC or flagS)
############################################################################
def getNeighbors2():
	''' Get neighborlist using ARP and FPING. More correct than getNeighbors()?'''
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
	''' My Mac list '''
	CMD="ifconfig"
	proc = subprocess.Popen(CMD,shell=True, stdout=subprocess.PIPE)
	(out, err) = proc.communicate()
	output_split=out.split("\n")
	listofMac=[j.split()[4] for i,j in enumerate(output_split) if "HWaddr" in j]
	return(listofMac)
#############################################################################
def getNeighbors():
	''' Get neighborlist using LLDP and fping. Sometimes gives error'''
	#selfMacs=get_self_mac()
	CMD="lldpcli show neighbors"
	proc = subprocess.Popen(CMD,shell=True, stdout=subprocess.PIPE)
	(out, err) = proc.communicate()
	#print out
	output_split=out.split("\n")
	listofMacPos=[i for i,j in enumerate(output_split) if "PortID:" in j]
	listofIfacePos=[i for i,j in enumerate(output_split) if "Interface:" in j]
	listofSysname=[i for i,j in enumerate(output_split) if "SysName:" in j]
	neighbor={}
	neighborIPList=[]
	for i,j in enumerate(listofMacPos):
		ifaceLine=output_split[listofIfacePos[i]]
		macLine=output_split[j]
		sysLine=output_split[listofSysname[i]]
		iface=re.split(': |, ',ifaceLine)[1].strip()
		mac=re.split(': |, ',macLine)[1].strip().replace("mac ","")
		SysName=re.split(': |, ',sysLine)[1].strip()
		#print SysName
		if ("eth" in iface):
			neighbor[iface]="192.168.2.%s"%(re.findall(r'\d+', SysName)[0])
			#neighborIPList.append()
	temp={}
	''' Detect neighbor interface and IP (Local topology)'''
	CMD="fping -c 1 -g 192.168.2.0/24 2> /dev/null"
	proc = subprocess.Popen(CMD,shell=True, stdout=subprocess.PIPE)
	(out, err) = proc.communicate()
	out=out.split("\n")
	fpingIP=[l.split(" ")[0] for l in out if (len(l)>0) ]
	IP=commands.getoutput("arp -n|awk '{print $0}'")
	IPs=[l.split()[0] for l in IP.split("\n") if "(incomplete)" not in l]
	neighborIPList=list(set(neighbor.values()).intersection(set(IPs)).intersection(set(fpingIP)))
	neighbor2={k:neighbor[k] for k in neighbor.keys() if neighbor[k] in neighborIPList}
	'''for mac in neighbor.keys():
		try:
			IP=commands.getoutput("arp -n|grep -i %s|awk '{print $1}'"%(mac))
			if IP=="":
				IP=MACREPO[mac]
			temp[neighbor[mac]]=IP
			neighbor[mac]=temp
			temp={}
		except:
			PrintLog("MAC key not found in MACREPO (%s). Something wrong!!!"%(mac))
	'''
	return(neighbor2)
############################################################################
def removeHosts(N):
	for k in N.keys():
		if N[k].values()[0] in HOSTS:
			del N[k]
	return(N)
############################################################################
#class App():
    #def __init__(self):
        #self.stdin_path = '/dev/null'
        #self.stdout_path = '/dev/tty'
        #self.stderr_path = '/dev/tty'
        #self.pidfile_path =  '/tmp/foo.pid'
        #self.pidfile_timeout = 5
############################################################################
def main():
	if detectChange()==1:
		neighbor={}
		neighbor2={}
		neighbor=getNeighbors()
		#neighbor2=getNeighbors2()
		neighbor.update(neighbor2)
		'''for k in neighbor.keys():
			if not(("br" in neighbor[k].keys()[0]) or (("eth" in neighbor[k].keys()[0]))):
				#PrintLog("remove "+k)
				neighbor.pop(k, None)'''
		putDictTo(folders+"LOG/neighbor_list.txt",neighbor)
		t=getTimeStamp()
		PrintLog("%s:\tState updated" %(t))
	else:
		#PrintLog("No need to update neighbor file")
		#print(".",end=" ")
		pass
		#neighbor=getNeighbors()
		#neighbor2=getNeighbors2()
	#neighbor=removeHosts(neighbor)
	#I=set(neighbor.keys()).difference(set(MACREPO.keys()))
	#[neighbor.pop(k, None) for k in I]
	#IPs={}
	#for k in neighbor.keys():
		#neighbor[k][neighbor[k].keys()[0]]=MACREPO[k]
	#PrintLog(neighbor,"\n")
	time.sleep(5)
#############################################################################
#	For Daemon
#############################################################################
def do_something():
	if ("it" in args.keys())and (isinstance(args["it"],int)):
		for i in xrange(0,args["it"]):
			#PrintLog("[%d]"%(i),end=" ")
			print("[%d]"%(i),end=" ")
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
