# Run ryu as "python ryu run --observe-links ryu/app/gui_topology/gui_topology.py"
# Creates ryu with rest server on 8080 port

import json
import urllib2
switchURL="http://127.0.0.1:9001/v1.0/topology/switches"
linkURL = "http://127.0.0.1:9001/v1.0/topology/links"
response = urllib2.urlopen(switchURL)
data = response.read()
switches = json.loads(data)

response = urllib2.urlopen(linkURL)
data = response.read()
links = json.loads(data)

print switches
print links