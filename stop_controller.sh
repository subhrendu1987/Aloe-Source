#!/bin/bash
# for Rpi-1
DOCKER_RYU=`sudo docker images |grep "ryu-armv7"|awk -F ' ' '{print $3}'`
docker container stop $(docker ps |grep $DOCKER_RYU|awk -F ' ' '{print $1}')
