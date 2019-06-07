#!/usr/bin/python
'''
Kills process from all rpis
'''
from __future__ import print_function
import datetime,subprocess,sys,os,json
import time,hashlib
from random import randint
import random, re, commands
from time import sleep
from copy import copy
from datetime import datetime
from myLibrary import *
import argparse

parser=argparse.ArgumentParser()
parser.add_argument("ProcessName",help="Provide process name/parts to be killed",default="nano",nargs="*")
args=parser.parse_args()
############################################################################
IPDICT=getDictFrom("hosts_file") ### Current directory should contain this file
piList=IPDICT.values()
############################################################################
for pi in piList:
	for pname in args.ProcessName:
		Output=RemoteExec(pi,"ps -ef| grep '%s'"%(pname))
		output_split=Output.split("\n")
		pids=[line.split()[1] for line in output_split if len(line) >0]
		for pid in pids:
			CMD="sudo kill -9 %s"%(pid)
			Output=RemoteExec(pi,CMD)
