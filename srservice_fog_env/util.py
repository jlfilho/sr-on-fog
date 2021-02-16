import logging
import subprocess
import ffmpeg
import json
import base64
import random
import string
import os
import glob

import numpy as np
from io import BytesIO


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


default_conf_video = {
    "144p": ['-map', '0:v', '-s:v', '256x144', '-b:v', '112k','-b:a','96k'],
    "360p": ['-map', '0:v', '-s:v', '640x360', '-b:v', '700k','-b:a','96k'],
    "480p": ['-map', '0:v', '-s:v', '854x480', '-b:v', '1300k','-b:a','96k'],
    "540p": ['-map', '0:v', '-s:v', '960x540', '-b:v', '1600k','-b:a','96k'],
    "720p": ['-map', '0:v', '-s:v', '1280x720', '-b:v', '2800k','-b:a','128k'],
    "1080p": ['-map', '0:v', '-s:v', '1920x1080', '-b:v', '6500k','-b:a','128k'],
    "2K": ['-map', '0:v', '-s:v', '2560x1440', '-b:v', '12000k','-b:a','128k'],
    "4K": ['-map', '0:v', '-s:v', '3840x2160', '-b:v', '25000k','-b:a','128k']
    }

def randomString(stringLength=15):
    """Generate a random string with the combination of lowercase and uppercase letters """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))


def get_video_size(filename):
    logger.info('Getting video size for {!r}'.format(filename))
    probe = ffmpeg.probe(filename)
    video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    width = int(video_info['width'])
    height = int(video_info['height'])
    return width, height


def start_ffmpeg_reader(input_path,fps=30,bufsize=-1):
    logger.info('Starting ffmpeg reader')
    args = [ 'ffmpeg', '-y','-re', '-rtbufsize', "{}".format(bufsize),
            '-i', input_path,
            '-pix_fmt', 'rgb24', '-r',str(fps),  
            '-f', 'rawvideo', '-' ]
    return subprocess.Popen(args, stdout=subprocess.PIPE,bufsize=bufsize)


def assemble_args(representations,args,output_path):
    count = 0
    for res in representations:
        for arg in default_conf_video[res]:
            if '-s' in arg or '-b' in arg:
                args.append(arg+':'+str(count))
            else:
                args.append(arg)
        count+=1
    args.append(output_path)
    return args 


def start_ffmpeg_writer_to_dash(output_path, width, height,representations,bufsize=-1,\
    fps=30,seg_duration=2,frag_duration=1,crf=20):
    logger.info('Starting ffmpeg writer')
    args = ['ffmpeg',
            '-y', '-re', '-rtbufsize', "{}".format(bufsize),
            '-f', 'rawvideo',
            '-c:v', 'rawvideo',
            '-pix_fmt', 'rgb24',
            '-r', str(fps),
            '-s:v', "{}x{}".format(width, height),
            '-i', '-',
            '-r', str(fps),
            '-tune', 'zerolatency',
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-preset', 'ultrafast',
            '-crf','{}'.format(crf),
            '-bf', '1', '-x264opts', 'keyint={}:min-keyint={}:no-scenecut'.format(fps, fps), 
            '-seg_duration', str(seg_duration), 
            '-frag_duration', str(frag_duration), 
            '-sc_threshold', '0', 
            '-use_timeline', '1', 
            '-use_template', '1', 
            '-b_strategy', '0', 
            '-pix_fmt', 'yuv420p', 
            '-init_seg_name', '$RepresentationID$-init.m4s', 
            '-media_seg_name', '$RepresentationID$-$Time$.m4s',
            '-f', 'dash']
    args = assemble_args(representations,args,output_path)
    return subprocess.Popen(args, stdin=subprocess.PIPE,bufsize=0)

def start_ffmpeg_writer_to_file(output_path, width, height,representations,bufsize=-1,\
    fps=30,seg_duration=2,frag_duration=1):
    logger.info('Starting ffmpeg writer')
    args = ['ffmpeg',
            '-y', '-re', '-rtbufsize', "{}".format(bufsize),
            '-f', 'rawvideo',
            '-c:v', 'rawvideo',
            '-pix_fmt', 'rgb24',
            '-r', str(fps),
            '-s:v', "{}x{}".format(width, height),
            '-i', '-',
            '-r', str(fps),
            '-tune', 'zerolatency',
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-preset', 'ultrafast',
            '-f', output_path]
    args = assemble_args(representations,args,output_path)
    return subprocess.Popen(args, stdin=subprocess.PIPE,bufsize=0)


def read_frame(reader, width, height):
    logger.debug('Reading frame')
    # Note: RGB24 == 3 bytes per pixel.
    frame_size = width * height * 3
    in_bytes = reader.stdout.read(frame_size)
    if len(in_bytes) == 0:
        frame = None
    else:
        assert len(in_bytes) == frame_size
        frame = (
            np
            .frombuffer(in_bytes, np.uint8)
            .reshape([height, width, 3])
        )
    return frame

def write_frame(writer, frame):
    logger.debug('Writing frame')
    writer.stdin.write(
        frame
        .astype(np.uint8)
        .tobytes()
    )

def clear_dash(path):
    logger.info('Clearning dash path')
    files = glob.glob(path+'*')
    for f in files:
        os.remove(f)
