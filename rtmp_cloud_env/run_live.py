import sys
import os
import subprocess
import logging
import numpy as np

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

ip = os.popen('ip addr show enp0s31f6').read().split("inet ")[1].split("/")[0]

RUN_TIME = 400  # sec 320
SOURCE = '/home/joao/data/videos_harmonic/1_VENICE_5994_UHD_h264.mp4'
RESOLUTION = "360p"
KEY = 'veneza'

MM_DELAY = 40   # millisec
downlink = "/usr/share/mahimahi/traces/Verizon-LTE-short.down"
uplink = "/usr/share/mahimahi/traces/Verizon-LTE-short.up"

RTMP_SERVER = 'rtmp://'+ip+':1935/live'
RUN_SCRIPT = 'live.py'


def restart_nginx():
    logger.info('Restarting RTPM server')
    stop_command = "sudo /usr/local/nginx/sbin/nginx -s stop"
    proc = subprocess.Popen(stop_command,stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    proc.wait()
    start_command = "sudo /usr/local/nginx/sbin/nginx"
    proc = subprocess.Popen(start_command,stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    proc.wait()


def main():
    restart_nginx()

    logger.debug('mm-delay ' + str(MM_DELAY) + 
        ' mm-link --meter-uplink '  + uplink +' '+   downlink +' ' +
        '/home/joao/anaconda3/envs/tf-gpu/bin/python ' + RUN_SCRIPT + ' ' + ip +
        ' ' + str(RUN_TIME) + ' ' + SOURCE + ' ' + RESOLUTION + ' ' + RTMP_SERVER +
        ' ' + KEY)

    logger.info('Starting live')
    proc = subprocess.Popen('mm-delay ' + str(MM_DELAY) + 
        ' mm-link --meter-uplink '  + uplink +' '+   downlink +' ' +
        '/home/joao/anaconda3/envs/tf-gpu/bin/python ' + RUN_SCRIPT + ' ' + ip +
        ' ' + str(RUN_TIME) + ' ' + SOURCE + ' ' + RESOLUTION + ' ' + RTMP_SERVER +
        ' ' + KEY,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    
    logger.info("Watch the video in URL: "+RTMP_SERVER+'/'+KEY)
    proc.wait()

    (out, err) = proc.communicate()
    
    if out == 'done\n':
        print("Exiting")
    else:
       print("Fail")




if __name__ == '__main__':
	main()