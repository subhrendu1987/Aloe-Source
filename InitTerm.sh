#!/bin/bash
CMD=$1
echo $CMD
gnome-terminal \
	--tab -e "sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@rpi1 -t \"cd flipperRPi3;sudo -E bash; set-title\"" \
	--tab -e "sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@rpi2 -t \"cd flipperRPi3;sudo -E bash; set-title\"" \
	--tab -e "sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@rpi3 -t \"cd flipperRPi3;sudo -E bash; set-title\"" \
	--tab -e "sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@rpi4 -t \"cd flipperRPi3;sudo -E bash; set-title\"" \
	--tab -e "sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@rpi5 -t \"cd flipperRPi3;sudo -E bash; set-title\"" \
	--tab -e "sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@rpi6 -t \"cd flipperRPi3;sudo -E bash; set-title\"" \
	--tab -e "sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@rpi7 -t \"cd flipperRPi3;sudo -E bash; set-title\"" \
	--tab -e "sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@rpi8 -t \"cd flipperRPi3;sudo -E bash; set-title\"" \
	--tab -e "sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@rpi9 -t \"cd flipperRPi3;sudo -E bash; set-title\"" \
	--tab -e "sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@rpi10 -t \"cd flipperRPi3;sudo -E bash; set-title\"" \
	--tab -e "sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@rpi11 -t \"cd flipperRPi3;sudo -E bash; set-title\"" \
	--tab -e "sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@rpi12 -t \"cd flipperRPi3;sudo -E bash; set-title\"" \
	--tab -e "sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@rpi13 -t \"cd flipperRPi3;sudo -E bash; set-title\"" \
	--tab -e "sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@rpi14 -t \"cd flipperRPi3;sudo -E bash; set-title\""
