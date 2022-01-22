#!/bin/bash

for ((j=0;j<500;j++));do
{
    for ((i=1;i<4;i++));do
    { 
        if [ $i -eq 1 ];then 
            ssh -t -p 22 nobi@pc324.emulab.net"python3 galera/galera-thread.py -f ${j} -n 1 ; exit"
        elif [ $i -eq 2 ];then 
            ssh -t -p 22 nobi@pc357.emulab.net "python3 galera/galera-thread.py -f ${j} -n 2; exit"
        elif [ $i -eq 3 ];then 
            ssh -t -p 22 nobi@pc322.emulab.net "python3 galera/galera-thread.py -f ${j} -n 3; exit"
        fi
    }&
    done
    wait

    ssh -t -p 22 nobi@pc339.emulab.net "python3 galera/galera-db.py 155.98.39.139; exit"
}
done

scp -r nobi@pc354.emulab.net:/users/nobi/output  /Users/zoe/Workspaces/github/galera/