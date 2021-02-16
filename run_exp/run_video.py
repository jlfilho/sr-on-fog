import os
import sys
import signal
import subprocess
from time import sleep
from video_session import video_session

# TO RUN: download https://pypi.python.org/packages/source/s/selenium/selenium-2.39.0.tar.gz
# run sudo apt-get install python-setuptools
# run sudo apt-get install xvfb
# after untar, run sudo python setup.py install
# follow directions here: https://pypi.python.org/pypi/PyVirtualDisplay to install pyvirtualdisplay

# For chrome, need chrome driver: https://code.google.com/p/selenium/wiki/ChromeDriver
# chromedriver variable should be path to the chromedriver
# the default location for firefox is /usr/bin/firefox and chrome binary is /usr/bin/google-chrome
# if they are at those locations, don't need to specify


def timeout_handler(signum, frame):
	raise Exception("Timeout")

ip = sys.argv[1]
abr_algo = sys.argv[2]
run_time = int(sys.argv[3])
process_id = sys.argv[4]
trace_file = sys.argv[5]
sleep_time = sys.argv[6]
	
# prevent multiple process from being synchronized
sleep(int(sleep_time))
	
# generate url
url = 'http://' + ip + '/' + 'myindex_' + abr_algo + '.html'
# timeout signal
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(run_time + 30)

chrome_driver = '../chromedriver/ToChrome87/chromedriver_linux64/chromedriver'
default_chrome_user_dir = '../abr_browser_dir/chrome_data_dir'
visibleInVirtualDisplay = False

	
try:
	# start abr algorithm server
	if abr_algo == 'RL':
		command = 'exec /home/joao/anaconda3/envs/tf1.15-gpu/bin/python ../rl_server/rl_server_no_training.py ' + trace_file
	elif abr_algo == 'fastMPC':
		command = 'exec /usr/bin/python ../rl_server/mpc_server.py ' + trace_file
	elif abr_algo == 'robustMPC':
		command = 'exec /usr/bin/python ../rl_server/robust_mpc_server.py ' + trace_file
	else:
		command = 'exec /usr/bin/python ../rl_server/simple_server.py ' + abr_algo + ' ' + trace_file
	print(command) #debug
	proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	sleep(2)

	# start video session
	video_session(url, process_id,run_time, default_chrome_user_dir, chrome_driver,visible = visibleInVirtualDisplay)
	
	# kill abr algorithm server
	proc.send_signal(signal.SIGINT)
	# proc.kill()
	
	print('done')


	
except Exception as e:
	try:
		proc.send_signal(signal.SIGINT)
	except:
		pass
	
	print(e)

