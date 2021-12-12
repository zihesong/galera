#!/bin/bash

for ((i=1;i<4;i++));do
{
    if [ $i -eq 1 ];then 
        ssh -t -t -p 22 nobi@pc357.emulab.net
    elif [ $i -eq 2 ];then 
        ssh -t -t -p 22 nobi@pc265.emulab.net
    elif [ $i -eq 3 ];then 
        ssh -t -t -p 22 nobi@pc328.emulab.net
    fi
    cd galera
    python3 galera-thread.py -n ${i}
    exit
}&
done
wait

ssh -t -t -p 22 nobi@pc340.emulab.net
sh galera-pre.sh
