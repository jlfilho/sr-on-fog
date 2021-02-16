import sys
import os
import subprocess
import logging
import numpy as np

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

ip = os.popen('ip addr show enp0s31f6').read().split("inet ")[1].split("/")[0]

KEY = 'veneza'
SOURCE = 'rtmp://'+ip+'/live/'


MM_DELAY = 40   # millisec
downlink = "/usr/share/mahimahi/traces/Verizon-LTE-short.down"
uplink = "/usr/share/mahimahi/traces/Verizon-LTE-short.up"

RUN_SCRIPT = 'srservice.py'


def main():
    logger.debug('mm-delay ' + str(MM_DELAY) + 
        ' mm-link --meter-downlink '  + uplink +' '+   downlink +' ' +
        '/home/joao/anaconda3/envs/tf-gpu/bin/python ' + RUN_SCRIPT + ' ' + SOURCE +' '+ KEY)

    logger.info('Get stream from RTMP Server')

    proc = subprocess.Popen('mm-delay ' + str(MM_DELAY) + 
        ' mm-link --meter-downlink '  + uplink +' '+   downlink +' ' +
        '/home/joao/anaconda3/envs/tf-gpu/bin/python ' + RUN_SCRIPT + ' ' + SOURCE +' '+ KEY,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True) 
    
    
    proc.wait()

    (out, err) = proc.communicate()
    
    if out == 'done\n':
        print("Exiting")
    else:
       print("Fail")


if __name__ == '__main__':
	main()