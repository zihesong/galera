#!/bin/bash

for ((i=1;i<4;i++));do
{
    if [ $i -eq 1 ];then 
        ssh -t -p 22 nobi@pc357.emulab.net "python3 galera/galera-thread.py -n 1"
        exit
    elif [ $i -eq 2 ];then 
        ssh -t -p 22 nobi@pc265.emulab.net "python3 galera/galera-thread.py -n 2"
        exit
    elif [ $i -eq 3 ];then 
        ssh -t -p 22 nobi@pc328.emulab.net "python3 galera/galera-thread.py -n 3"
        exit
    fi
}&
done
wait

ssh -t -p 22 nobi@pc340.emulab.net "sh galera/galera-pre.sh 155.98.39.140"
exit
