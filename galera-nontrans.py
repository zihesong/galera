'''
scp -P 22 /Users/zoooesong/Workspaces/galera-nontrans.py nobi@pc311.emulab.net:/users/nobi/galera-data/galera-nontrans.py
'''

import linecache
import os
import time
import random
import sys
import getopt
import threading
import resource
import re
import mariadb
import numpy as np
import matplotlib.pyplot as plt

wo_rate=0.5
transaction_num = 500
threads_num = 10
node_no=1
autocommit = 0
server_id = ['155.98.39.111','155.98.39.104','155.98.39.114']

try:
    opts, args = getopt.getopt(sys.argv[1:],"hw:t:c:n:a:",["help","wo_rate=","trans_num=","client_num=","node_no=","auto_commit="])
    for opt, arg in opts:
        if opt in ('-w','--wo_rate'):
            wo_rate = float(arg)
        elif opt in ('-t','--trans_num'):
            transaction_num = int(arg)
        elif opt in ('-c','--client_num'):
            threads_num = int(arg)
        elif opt in ('-n','--node_no'):
            node_no = int(arg)
        elif opt in ('-a','--auto_commit'):
            autocommit = int(arg)
        elif opt in ('-h','--help'):
            print("python3 galera-thread.py -w <wo_rate> -t <trans_num> -c <client_num> -n <node_no> -a <auto_commit>")
            sys.exit()
except getopt.GetoptError:
    print("python3 galera-thread.py -w <wo_rate> -t <trans_num> -c <client_num> -n <node_no> -a <auto_commit>")
    sys.exit()
print("Parameters:\nwo_rate = " + str(wo_rate) + "\ntrans_num = " + str(transaction_num) + "\nclient_num = " + str(threads_num) + "\nnode_no = " + str(node_no) + "\nauto_commit = " + str(autocommit))

key_num = 100
e_threshold= 0.005*transaction_num



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
    # def Display_info(self):
    #     if(op_type==True):
    #         print("write," + str(variable) + "," + str(value))
    #     elif(op_type==False):
    #         print("read," + str(variable) + "," + str(value))
    #     else:
    #         print("Error in Operation op_type!")


def uniform_generator(output_path, client, trans, var, rerun_count):
    '''
    output_path: hist file path
    client: client No.
    trans: trans num for each client
    ops: operation num for each trans
    var: key num
    wr: rate of w/r
    '''
    if rerun_count == 0:
        doc = open(output_path+"non_hist_"+str(client)+".txt",'w')
    else:
        doc = open(output_path+"non_hist_"+str(client)+"_"+str(rerun_count)+".txt",'w')
    counter = client * transaction_num
    for t in range (0,trans):
        trans_type = random_pick([0,1],[wo_rate,1-wo_rate])
        if trans_type == 0:
            variable = random.randint(0,var-1)
            counter += 1
            new_op = Operation(True,variable,counter)
            doc.write("write," + str(new_op.variable) + "," + str(new_op.value)+"\n")
        elif trans_type == 1:
            variable = random.randint(0,var-1)
            new_op = Operation(False,variable,0)
            doc.write("read," + str(new_op.variable) + "," + str(new_op.value)+"\n")
        else:
            print("Error in trans_type!")
    doc.close()
    if rerun_count == 0:
        print(output_path+"non_hist_"+str(client)+".txt"+" succeeded.")
    else:
        print(output_path+"non_hist_"+str(client)+"_"+str(rerun_count)+".txt"+" succeeded.")
    


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


def generate_opt(hist_file, trans_num): 
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
    for i in range(trans_num):
        list_trans.append(list_line[i])
    return list_trans


def run_ops(list_of_ops, client_no, start_pos):
    result_ops = []
    server_num = random_pick([0,1,2],[0.34,0.33,0.33])
    server = server_id[server_num]
    print("client_no: "+ str(client_no) + ", server_no: " + str(server))
    connect = mariadb.connect(host=server, user="root",password="123456")
    if autocommit == 0:
        connect.autocommit = False
    else:
        connect.autocommit = True
    e_count = 0
    for i in range(len(list_of_ops)):
        cursor = connect.cursor()
        if autocommit == False:
            cursor.execute("START TRANSACTION;")
        e_flag = False
        op = str.split(list_of_ops[i],',',3)
        key = int(op[1])
        if(op[0] == 'write'):
            val = int(op[2])
            try:
                cursor.execute("UPDATE galera.variables SET val=%d WHERE var=%d;" % (val,key))
                single_op = 'w(' + str(key) + ',' + str(val) + ',' + str(client_no) + ',' + str(start_pos+i) + ',' + str(start_pos+i) + ')'
            except Exception as e:
                print('Error in write: {}'.format(e)) 
                single_op = 'w(' + str(key) + ',' + str(val) + ',' + str(client_no) + ',' + str(start_pos+i) + ',' + str(start_pos+i) + ')'
                print(single_op)
                e_flag = True
        elif(op[0] == 'read'):
            try:
                cursor.execute("SELECT val FROM galera.variables WHERE var=%d;" % key)
                return_val = cursor.fetchall()
                record_val = return_val[0][0]
                single_op = 'r(' + str(key) + ',' + str(record_val) + ',' + str(client_no) + ',' + str(start_pos+i) + ',' + str(start_pos+i) + ')'
            except Exception as e:
                print('Error in read: {}'.format(e)) 
                single_op = 'r(' + str(key) + ',' + str(record_val) + ',' + str(client_no) + ',' + str(start_pos+i) + ',' + str(start_pos+i) + ')'
                print(single_op)
                e_flag = True
        else:
            print("Unknown wrong type op: '%s'" % op[0])
        if autocommit == False:    
            try:
                cursor.execute("COMMIT;")
            except Exception as e:
                print('Error in commit: {}'.format(e)) 
                cursor.execute("ROLLBACK;")
                print(single_op)
                e_flag = True
        connect.commit()
        if e_flag == True:
            state_op = 'op(' + str(i+start_pos) + ',0)'
            e_count += 1
        else:
            state_op = 'op(' + str(i+start_pos) + ',1)'
        result_ops.append(single_op)
        result_ops.append(state_op)
    cursor.close()
    connect.close()
    return result_ops, e_count

def write_result(result,file_path):
    '''
        result_single_history is a three dimensional list
        file is the output path
    '''
    f=open(file_path,"w")
    for n_trans in range(len(result)):
        f.write(result[n_trans]+'\n')
    f.close()
    print(file_path + ' is completed.')


def run_thread(id):
    start_pos = 0
    rerun_count = 0
    client = int((node_no-1)*threads_num+id)
    path = './client/' + str(client) + '/'
    mkdir(path) 
    uniform_generator(path, client, transaction_num, key_num, rerun_count)
    file_path = path + "non_hist_" + str(client) + ".txt"
    hist_list = generate_opt(file_path, transaction_num)
    result_list, error_num = run_ops(hist_list,client,start_pos)
    start_pos += transaction_num
    total_error = error_num
    while(error_num > e_threshold):
        rerun_count += 1
        tmp_error = error_num
        print("Client " + str(client) + " requires extra transactions! Count = " + str(rerun_count))
        extra_path = './client/' + str(client) + '/extra/'
        mkdir(extra_path) 
        uniform_generator(extra_path, client, error_num, key_num, rerun_count)
        extra_file_path = extra_path+"non_hist_"+str(client)+"_"+str(rerun_count)+".txt"
        extra_hist_list = generate_opt(extra_file_path, error_num)
        extra_result_list, error_num = run_ops(extra_hist_list,client,start_pos)
        start_pos += tmp_error
        total_error += error_num
        result_list.extend(extra_result_list)
    summary_line = "total = " + str(start_pos) + ", succeeded = " + str(start_pos-total_error) + ", failed = " + str(total_error)
    result_list.append(summary_line)
    result_path = "./output/non_transaction/result_" + str(client) + ".txt"
    write_result(result_list, result_path)


if __name__ == '__main__':
    threads =[]
    mkdir("./output/non_transaction/") 
    tlock=threading.Lock()
    for i in range(threads_num):
        thread = myThread(i)
        threads.append(thread)

    for i in range(threads_num):
        threads[i].start()
