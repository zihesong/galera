#!/bin/bash

# sh galera-server.sh 1
# scp -P 22 /Users/zoooesong/Workspaces/galera-server.sh nobi@pc479.emulab.net:/users/nobi/galera-data/galera-server.sh   

#change parameter
cluster_name="galera-121"
server1="155.98.39.139"
server2="155.98.39.140"
server3="155.98.39.142"

name1="node-1"
name2="node-2"
name3="node-3"
node=$1

if [ $node -eq 1 ];then 
    server="$server1"
    name="$name1"
elif [ $node -eq 2 ];then 
    server="$server2"
    name="$name2"
elif [ $node -eq 3 ];then 
    server="$server3"
    name="$name3"
fi

sudo apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 0xF1656F24C74CD1D8
sudo add-apt-repository 'deb [arch=amd64] http://nyc2.mirrors.digitalocean.com/mariadb/repo/10.4/ubuntu bionic main'
sudo apt update
sudo apt install mariadb-server

sudo mysql -uroot -e "set password = password("123456"); quit;"
sudo apt install rsync

sudo bash -c 'cat > /etc/mysql/conf.d/galera.cnf' << EOF
[mysqld]
binlog_format=ROW
default-storage-engine=innodb
wsrep_retry_autocommit = 3
innodb_autoinc_lock_mode=2
bind-address=0.0.0.0

# Galera Provider Configuration
wsrep_on=ON
wsrep_provider=/usr/lib/galera/libgalera_smm.so

# Galera Cluster Configuration
wsrep_cluster_name="$cluster_name"
wsrep_cluster_address="gcomm://$server1,$server2,$server3"

# Galera Synchronization Configuration
wsrep_sst_method=rsync

# Galera Node Configuration
wsrep_node_address="$server"
wsrep_node_name="$name"
EOF


sudo systemctl stop mysql
sudo systemctl status mysql
if [ $node -eq 1 ];then 
    sudo galera_new_cluster
    sudo mysql -u root -p123456 -e "SHOW STATUS LIKE 'wsrep_cluster_size'"
    sudo mysql -u root -p123456 -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%.emulab.net' IDENTIFIED BY '123456' WITH GRANT OPTION;"
else 
    sudo systemctl start mysql
    sudo mysql -u root -p123456 -e "SHOW STATUS LIKE 'wsrep_cluster_size'"
fi





