#!/bin/bash

for ((j=0;j<100;j++));do
{
    for ((i=1;i<4;i++));do
    { 
        if [ $i -eq 1 ];then 
            ssh -t -p 22 nobi@pc204.emulab.net "python3 galera/galera-thread.py -f ${j} -n1 ; exit"
        elif [ $i -eq 2 ];then 
            ssh -t -p 22 nobi@pc202.emulab.net "python3 galera/galera-thread.py -f ${j} -n 2; exit"
        elif [ $i -eq 3 ];then 
            ssh -t -p 22 nobi@pc278.emulab.net "python3 galera/galera-thread.py -f ${j} -n 3; exit"
        fi
    }&
    done
    wait

    ssh -t -p 22 nobi@pc354.emulab.net "python3 galera/galera-db.py 155.98.39.154; exit"
}
done

scp -r nobi@pc354.emulab.net:/users/nobi/output  /Users/zoe/Workspaces/github/galera/