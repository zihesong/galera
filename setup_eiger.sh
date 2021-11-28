cd /local
git clone https://github.com/zihesong/Eiger-PORT.git

cd Eiger-PORT
./install-dependencies.bash

cd Eiger-PORT
ant

cd tools/stress
ant

cd /local/Eiger-PORT/eiger
ant

cd tools/stress
ant




cd /local/Eiger-PORT/eval-scripts/vicci_dcl_config/

sudo nano 2_in_kodiak

num_dcs=2

cassandra_ips=node1

cassandra_ips=node2

sudo nano 2_clients_in_kodiak

num_dcs=2

cassandra_ips=node3

cassandra_ips=node4

/local/Eiger-PORT/eval-scripts/experiments/latency_throughput.bash 2

cd /local/Eiger-PORT/Eiger-PORT/tools/stress
git pull