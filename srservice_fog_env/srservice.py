import argparse
import sys
import numpy as np
import subprocess
import time 
import signal
import os
import logging

from model import create_model, sr_genarator, scale_lr_imgs, unscale_hr_imgs
from util import start_ffmpeg_reader, start_ffmpeg_writer_to_dash, start_ffmpeg_writer_to_file   
from util import get_video_size, read_frame, write_frame, clear_dash

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


# Create tensorflow model to upscale
model=create_model(scale=2)

# RTMP server address
source = sys.argv[1]
key = sys.argv[2]
input_path = source + key
output_path = r'/var/www/html/dash/'+key+'.mpd'
clear_dash("/var/www/html/dash/")


# Dash configuration
representations = ['360p','540p','720p']
fps = 24
seg_duration = 2
frag_duration = 1
crf = 20

width, height = get_video_size(input_path)
logger.debug("Video Format: {}x{}".format(width, height))
frame_size = width * height * 3
bufsize = 6 * fps * frame_size

try:  

    reader_video = start_ffmpeg_reader(input_path,fps=fps,bufsize=bufsize)
    writer_video = start_ffmpeg_writer_to_dash(output_path, width*2, height*2,representations,bufsize=bufsize,
        fps=fps,seg_duration=seg_duration,frag_duration=frag_duration,crf=crf)


    while True:
        in_frame = read_frame(reader_video, width, height)
        
        if in_frame is None:
            break
        frame_sr = sr_genarator(model,in_frame)
        write_frame(writer_video, frame_sr)
        #write_frame(writer_video, in_frame)

except Exception as e:
	try:
            writer_video.stdin.close()
            reader_video.stdout.close()
	except:
		pass
	print(e)