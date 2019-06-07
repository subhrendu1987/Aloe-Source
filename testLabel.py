#!/usr/bin/python
from __future__ import print_function
import datetime,subprocess,sys,os,json
import time,hashlib
import argparse
from random import randint
from myLibrary import *
import daemon
############################################################################
search_port='3366'
folders="/home/pi/flipperRPi3/"
state_file=folders+"LOG/nodeInfo.json"
log_file=folders+"LOG/log.txt"
mystate={}
interfaceFile="/sys/class/net/%s/operstate"
HISTORY={}
ip_state={}
controller_ip=''
neigborlist=folders+"LOG/neighbor_list.txt"
mac_file=folders+"LOG/MACREPO.json"
############################################################################
try:
	MACREPO=getDictFrom(mac_file)
except IOError:
	PrintLog( "File not found: ",colored(mac_file, 'green'))
	PrintLog( "Run from server: ",colored("python CreateMacRepo.py;bash PushCodesToPI.sh", 'red'))
	sys.exit(1)
try:
	args=getDictFrom("args.json")
except IOError:
	PrintLog( "File not found: ",colored("args,json", 'green'))
	PrintLog( colored("Create sample args.json file", 'red'))
	sys.exit(1)
############################################################################
def updateNeighborList():
	global neighbor
	global I
	global IPs
	global mystate
	try:
		neighbor=getDictFrom(neigborlist) ## Run StateUpdate.py in case of error
	except IOError:
		PrintLog( "File not found: ",colored(neighborlist, 'green'))
		PrintLog( "Run from server: ",colored("bash ExecALL.sh \"cd /home/pi/flipperRPi3; sudo python StateUpdate.py\"", 'red'))
		sys.exit(1)
	
	#I=set(neighbor.keys()).difference(set(MACREPO.keys()))
	#[neighbor.pop(k, None) for k in I]
	#IPs={}
	'''for k in neighbor.keys():
		PrintLog( "Some problems here")
		neighbor[k][neighbor[k].keys()[0]]=MACREPO[k]'''
	mystate=getDictFrom(state_file)
############################################################################
def N_nib(state):
	nibs=[]
	for n in state.keys():
		if(state[n]["Label"]=="NIB"):
			nibs.append(n)
	if len(nibs) > 0:
		return(nibs)
	else:
		return(None)
############################################################################
def state_change(st,mystate):
	mystate["Label"]=st
	putDictTo(state_file,mystate)
	ret=add_to_log("Label=%s"%(st))
	return ret
############################################################################
def max_pri(state):
	max_val=0
	Pri_list= [state[k]["R"] for k in state.keys() if state[k]["Label"]=="Wait" ]
	if len(Pri_list) ==0:
		max_val=None
	else:
		max_val=max(Pri_list)
	return(max_val)
############################################################################
def trial(neighbor,mystate):
	mystate["R"]=random.random()*len(neighbor.values())
	'''if len(neighbor.values())==1:
		mystate["R"]=randint(0,len(neighbor.values()))
	else:
		mystate["R"]=randint(0,len(neighbor.values()))'''
	putDictTo(state_file,mystate)
	return(mystate["R"])
############################################################################
def checkForController(state):
	#if state contains then list controller IP
	ctlrs=[]
	#PrintLog( "Checking the neighborhood for controller.")
	#PrintLog( neighbor)
	for ip in state.keys():
		if(state[ip]['Label']=='NIB'):
			ctlrs.append(ip)
	if(len(ctlrs)>0):
		C=getController()
		changeRequired=True
		for ctlr in ctlrs:
			changeRequired=(False and changeRequired) if ctlr in C else True
		if changeRequired:
			os.system("ovs-vsctl set-controller br tcp:%s:3366"%ctlrs[0])
			PrintLog( "Controller Obtaining Status: ",ctlrs[0])
		return(ctlrs)
	else:
		return None
############################################################################
def createControllerLog():
	return
	#PrintLog( "Itself is controller."
	#file_handle=open(folders+"LOG/controllerMarker.txt","w")
	#file_handle.write('{"Controller":"Yes"}')
	#file_handle.flush()
	#file_handle.close()
############################################################################
def getNeighborStates():
	state={}
	for iface in neighbor.keys():
		ip=neighbor[iface]
		try:
			state[ip]=PullRemoteFile(ip,state_file)
		except:
			PrintLog("ERROR!:\t%s\t%s"%(ip,state_file))
		#state[mac]=PullRemoteFile(ip,state_file)
		#state[mac]=PullRemoteFileWget(ip,state_file)
		#ip_state[ip]=state[mac]
	return(state)
############################################################################
mystate_prev={}
ip_state_prev={}
############################################################################
def execute_Round(state):
	global mystate_prev
	global ip_state_prev
	r=None
	flag=0
	ctlrs=[]
	if((mystate["Label"] == "Switch")and(N_nib(state)==None)): #R1
		ret=state_change("Wait",mystate)
		r=trial(neighbor,mystate)
		PrintLog( colored("R1 -->%f"%(r),"red"))
	elif((mystate["Label"] == "NIB")and(N_nib(state)<>None)):  #R2
		ret=state_change("Switch",mystate)
		### Add ctlr ip
		ctlrs=checkForController(state)
		PrintLog( colored("R2","red") )
	elif((mystate["Label"] == "Wait")and(N_nib(state)<>None)):  #R3
		ret=state_change("Switch",mystate)
		### Add ctlr ip
		ctlrs=checkForController(state)
		PrintLog( colored("R3","red"))
	elif((mystate["Label"] == "Wait")and(N_nib(state)==None)and(max_pri(state)==mystate["R"])):  #R4a
		ret=state_change("Wait",mystate)
		r=trial(neighbor,mystate)
		PrintLog( colored("R4a --> %f "%(r),"red") )
	elif((mystate["Label"] == "Wait")and(N_nib(state)==None)and(max_pri(state)<mystate["R"])):  #R4b
		if(max_pri(state) == None):
			PrintLog( "no neighbor in wait state so I am changing to NIB")
		ret=state_change("NIB",mystate)
		### Add ctlr ip
		PrintLog( colored("R4b","red") )
	else:
		ret=add_to_log("Do Nothing")
		if (mystate["Label"] == "Wait"):
			PrintLog( "CASE: Mylable=Wait")
		if((ip_state_prev <> ip_state) or (mystate_prev <> mystate)):
			PrintLog( colored("States:"+str(ip_state)+" (Own state:"+str(mystate)+")","red"))
			ip_state_prev=ip_state
			mystate_prev=mystate
		if(mystate["Label"] == "Switch"):
			ctlrs=checkForController(state)
		elif(mystate["Label"] == "NIB"):
			myip=getSelfIP()
			if(myip not in getController()):
				os.system("date && ovs-vsctl set-controller br tcp:%s:3366"%myip)
				#PrintLog( "Controller Obtaining Status: ",ctlrs[0])
		print(".",end=" ")
	if ctlrs==None:
		PrintLog( "State switch but no controller found.")
		PrintLog( "This means the round is still in progress")
		PrintLog( "Wait untill converges")
	return(ret,flag)
############################################################################
###                              Initialize                              ###
############################################################################
############################################################################
def main():
	countIdlePeriod=0
	gotController=False
	updateNeighborList()
	state=getNeighborStates()
	try:
		lg=execute_Round(state)
	except Exception as exception:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		PrintLog((exc_type, fname, exc_tb.tb_lineno))
		PrintLog( exception.__class__.__name__)
		PrintLog( "ERROR! execute_Round() "+str(state))
	time.sleep(5)
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
