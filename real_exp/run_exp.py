import sys
import os
import subprocess
import numpy as np


RUN_SCRIPT = 'run_video.py'
RANDOM_SEED = 42
RUN_TIME = 280  # sec
ABR_ALGO = ['fastMPC', 'robustMPC', 'BOLA', 'RL']
REPEAT_TIME = 60


def main():

	np.random.seed(RANDOM_SEED)

	with open('./chrome_retry_log', 'wb') as log:
		log.write('chrome retry log\n'.encode())
		log.flush()

		for rt in xrange(REPEAT_TIME):
			np.random.shuffle(ABR_ALGO)
			for abr_algo in ABR_ALGO:

				while True:
					print(abr_algo+" - "+str(rt))
					script = 'python ' + RUN_SCRIPT + ' ' + \
							  abr_algo + ' ' + str(RUN_TIME) + ' ' + str(rt)
					
					proc = subprocess.Popen(script,
							  stdout=subprocess.PIPE, 
							  stderr=subprocess.PIPE, 
							  shell=True)

					(out, err) = proc.communicate()
					if out == 'done\n':
						print("done")
						break
					else:
						log.write((abr_algo + '_' + str(rt) + '\n'))
						log.write(out + '\n')
						print(abr_algo + '_' + str(rt))
						print(out)
						log.flush()



if __name__ == '__main__':
	main()
