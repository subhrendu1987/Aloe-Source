#import networkx as nx
import pickle
import os,sys 
import requests,json
from myLibrary import *
import logging
#################################################################
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
#################################################################
# Set local stats using curl
def getCURLData(IP="127.0.0.1",URI="switches"):
	URL="http://%s:9000/stats/%s"%(IP,URI)
	print "URL:"+URL
	response = requests.get(URL)
	if (response.status_code == requests.codes.ok):
		return(response.json())
	else:
		logging.ERROR("URL:"+URL+"\t"+str(response.status_code))
		return(None)
#################################################################
# Get local stats using curl

#################################################################
def main():
	IP=getSelfIP()
	Data={}
	Data["switches"]=getCURLData(IP,"switches")
	Data["desc"]={ dpid: getCURLData(IP,"desc/%s"%(dpid)) for dpid in Data["switches"]}
	Data["flow"]={ dpid: getCURLData(IP,"flow/%s"%(dpid)) for dpid in Data["switches"]}
	Data["portdesc"]={ dpid: getCURLData(IP,"portdesc/%s"%(dpid)) for dpid in Data["switches"]}
	Data["groupdesc"]={ dpid: getCURLData(IP,"groupdesc/%s"%(dpid)) for dpid in Data["switches"]}
	Data["role"]={ dpid: getCURLData(IP,"role/%s"%(dpid)) for dpid in Data["switches"]}
	Data["groupfeatures"]={ dpid: getCURLData(IP,"groupfeatures/%s"%(dpid)) for dpid in Data["switches"]}
	Data["aggregateflow"]={ dpid: getCURLData(IP,"aggregateflow/%s"%(dpid)) for dpid in Data["switches"]}
	Data["table"]={ dpid: getCURLData(IP,"table/%s"%(dpid)) for dpid in Data["switches"]}
	Data["tablefeatures"]={ dpid: getCURLData(IP,"tablefeatures/%s"%(dpid)) for dpid in Data["switches"]}
	# port
	#Data["port"]={ dpid: getCURLData(IP,"port/%s"%(dpid)) for dpid in switches} ## Tabilize using port_no
	# port_no -->queue_id
	#Data["meter"]={ dpid: getCURLData(IP,"meter/%s"%(dpid)) for dpid in switches} ## Tabilize using meter_id
	# meter_id
	Data["group"]={ dpid: getCURLData(IP,"group/%s"%(dpid)) for dpid in Data["switches"]} ## Tabilize using group_id
	pickle.dump( Data, open( "/home/pi/flipperRPi3/ryu_stat_dump.pkl", "wb" ) )
############################################################################
if __name__ == '__main__':
    main()
