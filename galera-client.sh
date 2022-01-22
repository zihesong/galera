#! /bin/bash

# scp -P 22 /Users/zoooesong/Workspaces/galera-client.sh nobi@pc479.emulab.net:/users/nobi/galera-data/galera-client.sh 
# sh galera-client.sh 155.98.39.143
server=$1

sudo apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 0xF1656F24C74CD1D8
sudo add-apt-repository 'deb [arch=amd64] http://nyc2.mirrors.digitalocean.com/mariadb/repo/10.4/ubuntu bionic main'
sudo apt update
sudo apt install mariadb-client

sudo mysql -h ${server} -u root -p123456 -e "SHOW STATUS LIKE 'wsrep_cluster_size'"

