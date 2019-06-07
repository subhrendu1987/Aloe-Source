#!/bin/bash
CTLR_IP=$1
CTLR_IF=iface of ($CTLR_IP)
CTLR_PORT=ovs-vsctl get Interface $CTLR_IF ofport
#ovs-ofctl add-flow br nw_dst=$CTLR_IP,actions=output:$CTLR_PORT # for hidden flow creation in case of in-band controll

