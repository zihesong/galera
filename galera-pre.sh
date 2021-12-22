#! /bin/bash

# scp -P 22 /Users/zoooesong/Workspaces/galera-pre.sh nobi@pc479.emulab.net:/users/nobi/galera-data/galera-pre.sh 
# cd galera-data
# sh galera/galera-pre.sh 155.98.39.154

server=$1
rm -r client
ls
python3 galera/galera-db.py ${server}
# sudo mysql -h ${server} -u root -p123456 -e "select * from galera.variables;"