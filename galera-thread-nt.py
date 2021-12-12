'''
scp -P 22 /Users/zoooesong/Workspaces/galera-thread-nt.py nobi@pc817.emulab.net:/users/nobi/galera-data/galera-thread-nt.py

scp -r nobi@pc340.emulab.net:/users/nobi/galera/client  /Users/zoe/Workspaces/github/galera/

scp -r nobi@pc340.emulab.net:/users/nobi/galera/output  /Users/zoe/Workspaces/github/galera/
'''

import linecache
import os
import time
import random
import pandas as pd
import sys
import threading
import resource
import re
import mariadb
import numpy as np
import matplotlib.pyplot as plt

wr_rate = 55
key_num = 100
operation_num = 1
transaction_num = 1000
total_op_num = 1000
threads_num = 5
node_no=1
server_id = ['155.98.36.117','155.98.36.106','155.98.36.118']


def mkdir(path):
	folder = os.path.exists(path)
	if not folder:                   
		os.makedirs(path)            


class myThread(threading.Thread):
    def __init__(self,id):
        threading.Thread.__init__(self)
        self.id = id
        pass
    def run(self):
        run_thread(i)


class Operation:
    op_type = True  #true is write
    variable = 0
    value = 0
    
    def __init__(self, op_type, variable, value):
        self.op_type = op_type
        self.variable = variable
        self.value = value

    def Read(self,variable):
        self.op_type = False
        self.variable = variable
        self.value = 0
    def Write(self,variable,value):
        self.op_type = True
        self.variable = variable
        self.value = value
    def Display_info(self):
        if(op_type==True):
            print("write," + str(variable) + "," + str(value))
        elif(op_type==False):
            print("read," + str(variable) + "," + str(value))
        else:
            print("Error in Operation op_type!")


def uniform_generator(output_path, client, trans, ops, var, wr):
    '''
    output_path: hist file path
    client: client No.
    trans: trans num for each client
    ops: operation num for each trans
    var: key num
    wr: rate of w/r
    '''
    new_hist = [] 
    doc =open(output_path+"hist_"+str(client)+".txt",'w')
    counter = client * total_op_num
    for t in range (0,trans):
        # new_transaction = []
        for op in range (0,ops):
            if wr == 55:
                op_type = random_pick([True,False],[0.5,0.5])
            elif wr == 19:
                op_type = random_pick([True,False],[0.1,0.9])
            elif wr ==91:
                op_type = random_pick([True,False],[0.9,0.1])
            else:
                print('Wrong input wr!')

            if(op_type==False): #READ
                variable = random.randint(0,var-1)
                new_op = Operation(False,variable,0)
            elif(op_type==True):
                variable = random.randint(0,var-1)
                counter += 1
                new_op = Operation(True,variable,counter)
            else:
                print("Error in op_type!")
                # new_op.Display_info()
                    
            if(new_op.op_type==True):
                doc.write("write," + str(new_op.variable) + "," + str(new_op.value)+"\n")
            elif(new_op.op_type==False):
                doc.write("read," + str(new_op.variable) + "," + str(new_op.value)+"\n")
            else:
                print("Error in file Writing!")
    doc.close()
    print(output_path+"hist_"+str(client)+".txt"+" succeeded.")


def random_pick(some_list, probabilities): 
    '''
    randon_pick([true,false],[0.5,0.5])
    '''
    x = random.uniform(0,1) 
    cumulative_probability = 0.0 
    for item, item_probability in zip(some_list, probabilities): 
        cumulative_probability += item_probability 
        if x < cumulative_probability:
               break 
    return item 


def generate_opt(hist_file): 
    fo = open(hist_file, "r")
    print ("Select hist file:", fo.name)
    list_line = []
    for line in fo.readlines():
        line = line.strip()                            
        list_line.append(line)
    fo.close()
    # print(list_line)
    list_trans = []
    op_count=0
    for i in range(0,transaction_num):
        temp_ops = []
        for j in range(0,operation_num):
            temp_ops.append(list_line[op_count])
            op_count += 1
        list_trans.append(temp_ops)
    # print(list_trans[54])
    return list_trans


def run_ops(list_of_ops, client_no):
    op_num = 0
    result_ops = []
    server_num = random_pick([0,1,2],[0.34,0.33,0.33])
    server = server_id[server_num]
    print("client_no: "+ str(client_no) + ", server_no: " + str(server))
    connect = mariadb.connect(host=server, user="root",password="123456")
    # enable Auto-Commit
    connect.autocommit = True
    for i in range(len(list_of_ops)):
        cursor = connect.cursor()
        # cursor.execute("START TRANSACTION;")
        temp_tx_op = []
        e_flag = False
        for j in range(len(list_of_ops[i])):
            op = str.split(list_of_ops[i][j],',',3)
            key = int(op[1])
            if(op[0] == 'write'):
                val = int(op[2])
                try:
                    cursor.execute("UPDATE galera.variables SET val=%d WHERE var=%d;" % (val,key))
                    cursor.execute("SELECT val FROM galera.variables WHERE var=%d;" % key)
                    return_val = cursor.fetchall()
                    record_key = key
                    record_val = return_val[0][0]
                    single_op = 'w(' +  str(record_key) + ',' + str(record_val) + ','+ str(client_no) +','+str(i) +','+ str(op_num)+')'
                    temp_tx_op.append(single_op)
                    op_num += 1
                except Exception as e:
                    print('Error in read: {}'.format(e)) 
                    print(temp_tx_op)
                    e_flag = True
            elif(op[0] == 'read'):
                try:
                    cursor.execute("SELECT val FROM galera.variables WHERE var=%d;" % key)
                    return_val = cursor.fetchall()
                    record_key = key
                    record_val = return_val[0][0]
                    single_op = 'r(' +  str(record_key) +',' + str(record_val) +','+ str(client_no) +','+str(i) +','+ str(op_num)+')'
                    temp_tx_op.append(single_op)
                    # print(single_op)
                    op_num += 1
                except Exception as e:
                    print('Error in write: {}'.format(e)) 
                    print(single_op)
                    e_flag = True
            else:
                print("Unknown wrong type op: '%s'" % op[0])
        # try:
        #     cursor.execute("COMMIT;")
        # except Exception as e:
        #     print('Error in commit: {}'.format(e)) 
        #     cursor.execute("ROLLBACK;")
        #     print(temp_tx_op)
        try:
            connect.commit()
        except Exception as e:
            print('Error in commit: {}'.format(e)) 
            print(temp_tx_op)
            e_flag = True
        if e_flag == True:
            state_op = 'op(' + str(i) + ',' + '0)'
        else:
            state_op = 'op(' + str(i) + ',' + '1)'
        temp_tx_op.append(state_op)
        result_ops.append(temp_tx_op)
    cursor.close()
    connect.close()
    return result_ops

def write_result(result,file_path):
    '''
        result_single_history is a three dimensional list
        file is the output path
    '''
    f=open(file_path,"w")
    for n_trans in range(0,len(result)):
        for n_ops in range(0,len(result[0])):
            try:
                f.write(result[n_trans][n_ops]+'\n')
            except Exception as e:
                print('Error: {}'.format(e)) 
                print(result[n_trans-1:n_trans+1])
    f.close()
    print(file_path + ' is completed.')


def run_thread(id):
    client = int(node_no*threads_num+id)
    path = './client/' + str(client) + '/non-transaction' + str(transaction_num) + '/wr' + str(wr_rate) + '/key' +str(key_num)+ '/'
    mkdir(path) 
    uniform_generator(path, client, transaction_num, operation_num, key_num, wr_rate)
    file_path = path + "hist_" + str(client) + ".txt"
    hist_list = generate_opt(file_path)
    result_list = run_ops(hist_list,client)
    mkdir("./output/non-transaction") 
    result_path = "./output/non-transaction/result_" + str(client) + ".txt"
    write_result(result_list, result_path)


if __name__ == '__main__':
    threads =[]
    tlock=threading.Lock()
    for i in range(threads_num):
        thread = myThread(i)
        threads.append(thread)

    for i in range(threads_num):
        threads[i].start()