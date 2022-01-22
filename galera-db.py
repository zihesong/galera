'''
scp -P 22 /Users/zoooesong/Workspaces/galera-db.py nobi@pc479.emulab.net:/users/nobi/galera-data/galera-db.py
python3 galera/galera-db.py 155.98.39.143
'''

import os,sys
import mariadb


server = sys.argv[1]
key = 20

connect = mariadb.connect(host=server, user="root",password="123456")
# Disable Auto-Commit
connect.autocommit = False

cursor = connect.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS galera;")
cursor.execute("DROP TABLE IF EXISTS galera.variables;")
cursor.execute("CREATE TABLE IF NOT EXISTS galera.variables (var BIGINT(64) UNSIGNED NOT NULL PRIMARY KEY, val BIGINT(64) UNSIGNED NOT NULL);")

for i in range(0, key):
    cursor.execute("INSERT INTO galera.variables (var, val) values (%d, 0);" % i)

connect.commit()

cursor.close()
connect.close()
