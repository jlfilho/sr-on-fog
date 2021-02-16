import sys
import os
import signal
import logging
import subprocess
import numpy as np


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def timeout_handler(signum, frame):
	raise Exception("Timeout")


ip = sys.argv[1]
run_time = sys.argv[2]
source = sys.argv[3]
resolution = sys.argv[4]
rtmp_server = sys.argv[5]
key = sys.argv[6]


# timeout signal
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(int(run_time) + 5)


def start_transmission(source,rtmp_server,key='test', width=640, height=360,fps=30,crf=20,video_bitrate=1000,
    audio_bitrate=128):
    logger.info('Starting video transmission')
    args = ['ffmpeg','-y', '-re', '-i', source,
     '-c:a', 'aac', '-c:v', 'libx264', 
     '-preset', 'veryfast', '-r', '{}'.format(fps),
     '-crf','{}'.format(crf), '-s:v', '{}x{}'.format(width, height),
     '-b:v','{}'.format(video_bitrate),'-b:a','{}'.format(audio_bitrate),'-loop', '-1',
     '-pix_fmt', 'yuv420p',
     '-f', 'flv', rtmp_server+"/"+key]
    return subprocess.Popen(args, stdin=subprocess.PIPE)

default_conf_video = {
    "144p": {"width": 256, "height": 144,"fps": 30,"crf": 20, "video_bitrate": "112k", "audio_bitrate": "96k"},
    "360p": {"width": 640, "height": 360,"fps": 30,"crf": 20, "video_bitrate": "700k", "audio_bitrate": "96k"},
    "480p": {"width": 854, "height": 480,"fps": 30,"crf": 20, "video_bitrate": "1300k", "audio_bitrate": "96k"},
    "540p": {"width": 960, "height": 540,"fps": 30,"crf": 20, "video_bitrate": "1600k", "audio_bitrate": "96k"},
    "720p": {"width": 1280, "height": 720,"fps": 30,"crf": 20, "video_bitrate": "2800k", "audio_bitrate": "128k"},
    "1080p": {"width": 1920, "height": 1080,"fps": 30,"crf": 20, "video_bitrate": "6500k", "audio_bitrate": "128k"},
    "2K": {"width": 2560, "height": 1440,"fps": 30,"crf": 20, "video_bitrate": "12000k", "audio_bitrate": "128k"},
    "4K": {"width": 3840, "height": 2160,"fps": 30,"crf": 20, "video_bitrate": "25000k", "audio_bitrate": "128k"}
}


if __name__ == '__main__':
    try:
        transmission = start_transmission(source,rtmp_server,key=key,**default_conf_video[resolution])
        transmission.wait() 
        # kill abr algorithm server
        transmission.send_signal(signal.SIGINT)
        
        print('done')
    except Exception as e:
        try:
            transmission.send_signal(signal.SIGINT)
            print('fail')
        except:
            pass
        print(e)