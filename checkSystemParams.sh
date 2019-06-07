#!/bin/bash

while true
do
	date >> /home/pi/flipperRPi3/LOG/checkSystemParams.nohup
	memString="$(free | grep Mem)"
	cpuConsum="$(grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}')"
	gpuTemp="$(/opt/vc/bin/vcgencmd measure_temp)"
	cpuTemp="$(sudo cat /sys/class/thermal/thermal_zone0/temp)"

	IFS=' ' read -r -a memArr <<< "${memString}"
	
	echo "Memory Consumption: "${memArr[2]} >> /home/pi/flipperRPi3/LOG/checkSystemParams.nohup
	echo "CPU COnsumption: "$cpuConsum>> /home/pi/flipperRPi3/LOG/checkSystemParams.nohup
	echo ${gpuTemp}>> /home/pi/flipperRPi3/LOG/checkSystemParams.nohup
	echo $((cpuTemp/1000))"'C">> /home/pi/flipperRPi3/LOG/checkSystemParams.nohup
	echo "----">> /home/pi/flipperRPi3/LOG/checkSystemParams.nohup
	sleep 60
done
