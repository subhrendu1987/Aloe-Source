'''
Ping test for checking if everything is working fine or not
'''

import datetime,subprocess,sys,os,json
import time,hashlib
from random import randint
from myLibrary import *
############################################################################
hosts=['192.168.2.12','192.168.2.13','192.168.2.37']

CMD="ifconfig"
proc = subprocess.Popen(CMD,shell=True, stdout=subprocess.PIPE)
(output, err) = proc.communicate()

myip=[ ip for ip in hosts if (ip) in output][0]
hosts.remove(myip)
for ip in hosts:
	CMD="ping -c 5 %s"%ip
	proc = subprocess.Popen(CMD,shell=True, stdout=subprocess.PIPE)
	(output, err) = proc.communicate()
	output=output.split("\n")
	print
	

