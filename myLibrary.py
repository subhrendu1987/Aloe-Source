#from __future__ import print_function
import datetime,subprocess,sys,os,json
import time,hashlib
from random import randint
import random, re, commands
from time import sleep
from copy import copy
from termcolor import colored
import inspect,socket
############################################################################
folders="/home/pi/flipperRPi3/"
log_file=folders+"LOG/log.txt"
############################################################################
def getSelfIP():
	f= open('/home/pi/ip.txt');ip = f.readlines()[0].strip()
	return(ip)
############################################################################
def PrintLog(m,end="\n"):
	ip=getSelfIP();
	print("[%s]<%s @ %s> %s"%(getTimeStamp(),str(inspect.stack()[1][1]),ip,m))
	return
############################################################################
def infinite_sequence():
	while True:
		yield True 
############################################################################
def hash_dict(d):
    return hashlib.sha1(json.dumps(d, sort_keys=True)).hexdigest()
############################################################################
def getTimeStamp():
	tstamp = str(datetime.datetime.now())
	return(tstamp)
############################################################################
def printToLog(filename,logtext):
	file_handler=open(filename,"a")
	tstamp = getTimeStamp()
	log_string="%s\t %s\n"%(tstamp,logtext)
	file_handler.write(log_string)
	file_handler.close()
	return
############################################################################
def add_to_log(log):
	file_handler=open(log_file,"a")
	tstamp = getTimeStamp()
	log_string="%s\t %s\n"%(tstamp,log)
	file_handler.write(log_string)
	file_handler.close()
	return log_string
############################################################################
def getDataFrom(filename):
	file_handler=open(filename,"r")
	variable=[l.strip() for l in file_handler]
	file_handler.close()
	return(variable)
############################################################################
def getDictFrom(filename):
	file_handler=open(filename,"r")
	variable=json.load(file_handler)
	file_handler.close()
	return(variable)
############################################################################
def putDictTo(filename,variable):
	file_handler=open(filename,"w")
	json.dump(variable, file_handler)
	file_handler.flush()
	file_handler.close()
	return
############################################################################
def getController(out=None):
	if(out == None):
		CMD="sudo ovs-vsctl show"
		proc = subprocess.Popen(CMD,shell=True, stdout=subprocess.PIPE)
		(out, err) = proc.communicate()
	out=out.split("\n")
	ctlrLine=[l.replace("\"","") for l in out if "Controller" in l][0]
	return(ctlrLine)
############################################################################
def RemoteExec(node,command):
	CMD="sshpass -p \"raspberry\" ssh -o StrictHostKeyChecking=no pi@%s \"%s\""%(node,command)
	print(CMD)
	proc = subprocess.Popen(CMD,shell=True, stdout=subprocess.PIPE)
	(out, err) = proc.communicate()
	if err:
		print("SSHPASS:Err-%s"%(err))
	return(out)
############################################################################
def PullFileScp(pi,Remotefile,Localfile="/tmp/tmp.json"):
	CMD="sshpass -p 'raspberry' scp -o StrictHostKeyChecking=no -o ConnectTimeout=3 -r pi@%s:%s %s" %(pi,Remotefile,Localfile)
	#print CMD
	proc = subprocess.Popen(CMD,shell=True, stdout=subprocess.PIPE)
	(output, err) = proc.communicate()
	return
############################################################################
def PullRemoteFile(ip,filename):
	CMD="sshpass -p \"raspberry\" scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no pi@%s:%s /tmp/tmp.json" %(ip,filename)		#print "DEBUG:%s"%(CMD)
	#print CMD
	proc = subprocess.Popen(CMD,shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	(out, err) = proc.communicate()
	os.system("cat /tmp/tmp.json")
	if((len(err) ==0) or ("Warning" in err)):
		variable = getDictFrom("/tmp/tmp.json")
	else:
		print("SSH Error! "+err)
		variable=None
	return(variable)
############################################################################
def PullRemoteFileWget(ip,filename,port=8080):
	tmp_file="/tmp/tmp.json"
	CMD="wget http://%s:%d/%s -O %s"%(ip,port,"LOG/"+os.path.basename(filename),tmp_file)
	proc = subprocess.Popen(CMD,shell=True, stdout=subprocess.PIPE)
	(out, err) = proc.communicate()
	#ret=os.system(CMD)
	if(ret==0):
		variable = getDictFrom(tmp_file)
		os.system("rm %s"%(tmp_file))
		return(variable)
	else:
		return(None)
############################################################################
