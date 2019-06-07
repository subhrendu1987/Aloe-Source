#!/bin/sh
getPid(){
	pidof=$(ps -aux|grep "testLabel.py"|awk -F ' ' '{print $2}')
	return $pidof
}
kill -9 $
