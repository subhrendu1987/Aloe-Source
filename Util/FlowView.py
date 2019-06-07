#!/usr/bin/python
from __future__ import print_function
import pickle
import os,sys 
import json
import os.path
import itertools,types
import logging
import StringIO

from myLibrary import *

IPDICT=getDictFrom("hosts_file") ### Current directory should contain this file
piList=IPDICT.values()
mac_file="LOG/MACREPO.json"

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
#################################################################
try:
	MACREPO=getDictFrom(mac_file)
except IOError:
	print( "File not found: ",colored(mac_file, 'green'))
	print( "Run from server: ",colored("python CreateMacRepo.py;bash PushCodesToPI.sh", 'red'))
	sys.exit(1)
#################################################################
def dictUpdate(d,a):
	ret=d
	ret.update(a)
	return(ret)
#################################################################
def simplifyAction(actions,portDict):
	actions1=actions.replace("actions=","").replace("output","")
	if ("LOCAL" in actions1):
		actions1=[actions1]
	else:
		actions1=actions1.split(":")
	ret=[portDict[a][0] for a in actions1 if(len(a) >0)]
	return(ret)
#################################################################
def getAllFlows():
	flows={}
	for pi in piList:
		line=RemoteExec(pi,"sudo ovs-vsctl -- --columns=name,ofport list Interface")
		split_line=[l.split(":") for l in line.split("\n") if len(l)>0]
		portDict={str(int(split_line[i+1][1])):re.findall(r'\"([^]]*)\"', split_line[i][1]) for i in xrange(0,len(split_line),2) if (len(re.findall(r'\"([^]]*)\"', split_line[i][1]))> 0)}
		portDict["LOCAL"]=[split_line[0][1]]
		line=RemoteExec(pi,"sudo ovs-ofctl  dump-flows br")
		tmp=[l.split(" ") for l in line.split("\n") if ((len(l) > 0 ) and  ("NXST_FLOW" not in l))]
		flows[pi]=[{"match":f[len(f)-2],"actions":simplifyAction(f[len(f)-1],portDict)} for f in tmp]
	return(flows)
#################################################################
def UniqueFlowMatches(flows):
	matches={}
	for rpi in flows.keys():
		for f in flows[rpi]:
			ip=[MACREPO[mac] for mac in MACREPO.keys() if(mac in  f["match"])]
			piName= ["rpi"+x.split(".")[3] for x in ip]
			if f["match"] in matches:
				matches["%s-%s"%(f["match"],piName)].append("%s-%s"%(rpi,f["actions"]))
			else:
				matches["%s-%s"%(f["match"],piName)]=["%s-%s"%(rpi,f["actions"])]
		#matches=dictUpdate(matches,{rpi+f["actions"][0]:[f["match"] for f in flows[rpi]]})
		#interfaces=dictUpdate(interfaces,{rpi:[f["actions"] for f in flows[rpi]]})
	#flowsVsRpi={m:[rpi for rpi in matches.keys() if(m in matches[rpi])] for m in set(list(itertools.chain.from_iterable(matches.values())))}
	return(matches)
#################################################################
def PrintFlowTable(uniqueMatch):
	print("-----------------------------------------------------------------")
	for k in uniqueMatch:
		print(colored(k, 'green'),"\t:\t",uniqueMatch[k])
	print("-----------------------------------------------------------------")
	return(0)
#################################################################
def main():
	flows=getAllFlows()
	uniqueMatch=UniqueFlowMatches(flows)
	PrintFlowTable(uniqueMatch)
	return(0)
############################################################################
if __name__ == '__main__':
    main()
