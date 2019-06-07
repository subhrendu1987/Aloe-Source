#!/bin/bash
ret=$(docker ps -q)
if [ -z $ret ]
then
	echo "No Exited docker" 
else
	docker kill $(docker ps -q)
fi
ret=$(docker ps -a -q)
if [ -z $ret ]
then
	echo "No Killed docker" 
else
	docker rm $(docker ps -a -q)
fi
