import os
import time
import json
import urllib
import subprocess



TRACE_PATH = '../cooked_traces_mahimahi/' 

with open('./chrome_retry_log', 'w') as f:
	f.write('chrome retry log\n')

os.system('sudo sysctl -w net.ipv4.ip_forward=1')

ip = os.popen('ip addr show enp0s31f6').read().split("inet ")[1].split("/")[0]

#ip_data = {"ip": "192.168.100.20"}
#ip = str(ip_data['ip'])


""" ABR_ALGO = 'BB'
PROCESS_ID = 0
command_BB = 'python run_traces.py ' + TRACE_PATH + ' ' + ABR_ALGO + ' ' + str(PROCESS_ID) + ' ' + ip

ABR_ALGO = 'RB'
PROCESS_ID = 1
command_RB = 'python run_traces.py ' + TRACE_PATH + ' ' + ABR_ALGO + ' ' + str(PROCESS_ID) + ' ' + ip

ABR_ALGO = 'FIXED'
PROCESS_ID = 2
command_FIXED = 'python run_traces.py ' + TRACE_PATH + ' ' + ABR_ALGO + ' ' + str(PROCESS_ID) + ' ' + ip

ABR_ALGO = 'FESTIVE'
PROCESS_ID = 3
command_FESTIVE = 'python run_traces.py ' + TRACE_PATH + ' ' + ABR_ALGO + ' ' + str(PROCESS_ID) + ' ' + ip

ABR_ALGO = 'BOLA'
PROCESS_ID = 4
command_BOLA = 'python run_traces.py ' + TRACE_PATH + ' ' + ABR_ALGO + ' ' + str(PROCESS_ID) + ' ' + ip

ABR_ALGO = 'fastMPC'
PROCESS_ID = 5
command_fastMPC = 'python run_traces.py ' + TRACE_PATH + ' ' + ABR_ALGO + ' ' + str(PROCESS_ID) + ' ' + ip

ABR_ALGO = 'robustMPC'
PROCESS_ID = 6 
command_robustMPC = 'python run_traces.py ' + TRACE_PATH + ' ' + ABR_ALGO + ' ' + str(PROCESS_ID) + ' ' + ip """

ABR_ALGO = 'RL'
PROCESS_ID = 7
command_RL = 'python run_traces.py ' + TRACE_PATH + ' ' + ABR_ALGO + ' ' + str(PROCESS_ID) + ' ' + ip

""" print(command_BB)
proc_BB = subprocess.Popen(command_BB, stdout=subprocess.PIPE, shell=True)
time.sleep(0.1)

print(command_RB)
proc_RB = subprocess.Popen(command_RB, stdout=subprocess.PIPE, shell=True)
time.sleep(0.1)

print(command_FIXED)
proc_FIXED = subprocess.Popen(command_FIXED, stdout=subprocess.PIPE, shell=True)
time.sleep(0.1)
print(command_FESTIVE)
proc_FESTIVE = subprocess.Popen(command_FESTIVE, stdout=subprocess.PIPE, shell=True)
time.sleep(0.1)
print(command_BOLA)
proc_BOLA = subprocess.Popen(command_BOLA, stdout=subprocess.PIPE, shell=True)
time.sleep(0.1)
print(command_fastMPC)
proc_fastMPC = subprocess.Popen(command_fastMPC, stdout=subprocess.PIPE, shell=True)
time.sleep(0.1)
print(command_robustMPC)
proc_robustMPC = subprocess.Popen(command_robustMPC, stdout=subprocess.PIPE, shell=True)
time.sleep(0.1) """
print(command_RL)
proc_RL = subprocess.Popen(command_RL, stdout=subprocess.PIPE, shell=True)
time.sleep(0.1) 

"""print('Processo BB wait')
proc_BB.wait()
print('Processo RB wait')
proc_RB.wait()
print('Processo FIXED wait')
proc_FIXED.wait()
print('Processo FESTIVE wait')
proc_FESTIVE.wait()
print('Processo BOLA wait')
proc_BOLA.wait()
print('Processo fastMPC wait')
proc_fastMPC.wait()
print('Processo robustMPC wait')
proc_robustMPC.wait() """

print('Processo RL wait')
proc_RL.wait() 
