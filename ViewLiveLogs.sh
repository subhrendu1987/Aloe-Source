#!/bin/bash
RED='\033[0;31m'
NC='\033[0m' # No Color

FILENAME=$1
echo -e "${RED} $FILENAME ${NC}"
echo -e "${RED} ############################################################################## ${NC}"

gnome-terminal \
	--tab -e "multitail -l 'sshpass -p \"raspberry\" ssh pi@rpi1 \"tail -f $FILENAME\"' -l 'sshpass -p \"raspberry\" ssh pi@rpi2 \"tail -f $FILENAME\"'" \
	--tab -e "multitail -l 'sshpass -p \"raspberry\" ssh pi@rpi3 \"tail -f $FILENAME\"' -l 'sshpass -p \"raspberry\" ssh pi@rpi4 \"tail -f $FILENAME\"'" \
	--tab -e "multitail -l 'sshpass -p \"raspberry\" ssh pi@rpi5 \"tail -f $FILENAME\"' -l 'sshpass -p \"raspberry\" ssh pi@rpi6 \"tail -f $FILENAME\"'" \
	--tab -e "multitail -l 'sshpass -p \"raspberry\" ssh pi@rpi7 \"tail -f $FILENAME\"' -l 'sshpass -p \"raspberry\" ssh pi@rpi8 \"tail -f $FILENAME\"'" \
	--tab -e "multitail -l 'sshpass -p \"raspberry\" ssh pi@rpi9 \"tail -f $FILENAME\"' -l 'sshpass -p \"raspberry\" ssh pi@rpi10 \"tail -f $FILENAME\"'" \
	--tab -e "multitail -l 'sshpass -p \"raspberry\" ssh pi@rpi11 \"tail -f $FILENAME\"' -l 'sshpass -p \"raspberry\" ssh pi@rpi12 \"tail -f $FILENAME\"'" \
	--tab -e "multitail -l 'sshpass -p \"raspberry\" ssh pi@rpi13 \"tail -f $FILENAME\"' -l 'sshpass -p \"raspberry\" ssh pi@rpi14 \"tail -f $FILENAME\"'" 
