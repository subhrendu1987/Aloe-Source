#import networkx as nx
import pickle
import os,sys 
import requests,json
import os.path
from myLibrary import *
import itertools,types
import logging,pycurl
import curlify
import StringIO
response = StringIO.StringIO()

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
#################################################################
allowed_flow_field=["dpid","cookie","cookie_mask","table_id","idle_timeout","hard_timeout","priority","buffer_id","Buffered","flags","match","actions"]
#################################################################
# Set local stats using curl
def postCURLData(IP="127.0.0.1",URI="",data={}):
	if(URI==""):
		logging.ERROR("Enter URI")
		return(False)
	URL="http://%s:9000/stats/%s"%(IP,URI)
	unnecessary_field=set(data.keys()).difference(set(allowed_flow_field))
	for f in unnecessary_field:
		del data[f]
	print "DEBUG!",data["dpid"],data['match'],data["actions"]
	if (type(data["actions"][0]) is dict):
		pass
	else:
		actions=data["actions"][0].split(":")
		data["actions"]=[{"type":actions[0],"port":actions[1]}]
	#print "DEBUG!:","URL:"+URL,data
	#return(True)
	#CMD=["curl","-X","POST","-d",str(data), URL]
 	CMD="curl -X POST -d \""+ str(data) +"\" " +URL
	result = os.popen(CMD).read()  ### How to check success
	if len(result):
		return(True)
	else:
		logging.warning(result)
		return(False)
#################################################################
# Get local stats using curl
def getCURLData(IP="127.0.0.1",URI="switches"):
	URL="http://%s:9000/stats/%s"%(IP,URI)
	print "URL:"+URL
	response = requests.get(URL)
	logging.warning(curlify.to_curl(response.request)) 
	if (response.status_code == requests.codes.ok):
		return(response.json())
	else:
		logging.ERROR("URL:"+URL+"\t %d"%(response.status_code))
		return(None)
#################################################################
def dictUpdate(d,a):
	ret=d
	ret.update(a)
	return(ret)
#################################################################
def main():
	IP=getSelfIP()
	if (os.path.isfile("/home/pi/flipperRPi3/ryu_stat_dump.pkl")):
		Data=pickle.load( open( "/home/pi/flipperRPi3/ryu_stat_dump.pkl", "rb" ) )
		switches=getCURLData(IP=IP,URI="switches")
		if(Data["switches"]<> switches):
			# remove not connected switches
			pass
		flows=Data["flow"].values()
		dpid_flows=Data["flow"][dpid].values()[0]
		ret=[ [postCURLData(IP,URI="flowentry/add",data=dictUpdate(d,{"dpid":dpid})) for d in Data["flow"][dpid].values()[0]] for dpid in Data["flow"].keys() ]
	else:
		return(0)
############################################################################
if __name__ == '__main__':
    main()

############################################################################
# Extra
#curl -X POST -d '{"dpid": 257,"priority": 32768,"match":{"dl_dst": "00:00:00:00:01:01", "in_port":1},"cookie": 1,"cookie_mask": 1,"table_id": 0,"idle_timeout": 30,"hard_timeout": 30,"flags": 1,"table_id": 0,"actions":[{"type":"OUTPUT","port": 1}]}' http://192.168.2.1:9000/stats/flowentry/add

	# Data={}
	# Data["desc"]={ dpid: }
	# Data["flow"]={ dpid: getCURLData(IP,URI="flow/%s"%(dpid)) for dpid in switches}
	# Data["portdesc"]={ dpid: getCURLData(IP,"portdesc/%s"%(dpid)) for dpid in switches}
	# Data["groupdesc"]={ dpid: getCURLData(IP,"groupdesc/%s"%(dpid)) for dpid in switches}
	# Data["role"]={ dpid: getCURLData(IP,"role/%s"%(dpid)) for dpid in switches}
	# Data["groupfeatures"]={ dpid: getCURLData(IP,"groupfeatures/%s"%(dpid)) for dpid in switches}
	# Data["aggregateflow"]={ dpid: getCURLData(IP,"aggregateflow/%s"%(dpid)) for dpid in switches}
	# Data["table"]={ dpid: getCURLData(IP,"table/%s"%(dpid)) for dpid in switches}
	# Data["tablefeatures"]={ dpid: getCURLData(IP,"tablefeatures/%s"%(dpid)) for dpid in switches}
	# # port
	# #Data["port"]={ dpid: getCURLData(IP,"port/%s"%(dpid)) for dpid in switches} ## Tabilize using port_no
	# # port_no -->queue_id
	# #Data["meter"]={ dpid: getCURLData(IP,"meter/%s"%(dpid)) for dpid in switches} ## Tabilize using meter_id
	# # meter_id
	# Data["group"]={ dpid: getCURLData(IP,"group/%s"%(dpid)) for dpid in switches} ## Tabilize using group_id