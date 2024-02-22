#!/bin/bash
while :
do
	ping 172.16.80.29 -c 1 >> /dev/null
	sleep 30
done
