#!/bin/bash
# Remove all exited controller docker
#docker ps -aq --no-trunc | xargs docker rm
DOCKER_RYU=`sudo docker images |grep "ryu-armv7"|awk -F ' ' '{print $3}'`
#docker run -d -p 3366:6633 -p 8080:8080 -t $DOCKER_RYU /bin/sh -c 'cd ryu; ryu run --observe-links --ofp-tcp-listen-port 6633 ryu/app/gui_topology/gui_topology.py ryu/app/simple_switch_13.py'

docker ps -a | grep Exit | cut -d ' ' -f 1 | xargs sudo docker rm

#docker run -i -p 3366:6633 -p 9000:9000 -p 9001:8080 -t $DOCKER_RYU /bin/sh -c 'ryu/bin/ryu-manager --observe-links --ofp-tcp-listen-port 6633 --wsapi-port 9000 ryu.app.ofctl_rest ryu.app.simple_switch ryu.app.gui_topology.gui_topology.py'

docker run -d -p 3366:6633 -p 9000:9000 -t $DOCKER_RYU /bin/sh -c '/ryu/bin/ryu-manager --observe-links --ofp-tcp-listen-port 6633 --wsapi-port 9000 ryu.app.ofctl_rest ryu.app.simple_switch'

#docker run -d -p 3366:6633 -p 9000:8080 -t $DOCKER_RYU /bin/sh -c 'ryu/bin/ryu-manager --observe-links --ofp-tcp-listen-port 6633 ryu.app.simple_switch ryu.app.gui_topology.gui_topology'

#docker run -i -p 3366:6633 -p 9000:9000 -t $DOCKER_RYU /bin/bash

