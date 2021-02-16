# Introduction

This module represents the RTMP server on the cloud and the video stream content source. The RTMP server is deployed with NGINX with the RTMP module.
We implemented a script using FFmpeg that represents the source of the video stream content. To emulate the characteristics of the network we use the Network Emulation Tools Mahimahi.


 ------------            	       ------------  
|source video| ----mahimahi trace---> | rtmp server|
 ------------ 		 	       ------------


# Install NGINX with RTMP Module

NGINX is the RTMP server to which the content generator transmits the video in low resolution.


# Installing the Build Tools

Before compiling NGINX, you need to have some basic build tools installed: autoconf, gcc, git, and make. To download and install them, run the command for your operating system (if it’s not included here, consult the OS vendor documentation).

$ sudo apt update
$ sudo apt install build-essential git


# Installing Dependencies

The NGINX build also requires several dependencies: Perl Compatible Regular Expressions (PCRE), OpenSSL, and zlib for compression.

The easier way to download and install the dependencies is with a package manager. Run the command for your operating system (if it’s not included here, consult the OS vendor documentation).


$ sudo apt install libpcre3-dev libssl-dev zlib1g-dev

# Compiling NGINX with the RTMP Module

To complete the build, you clone the GitHub repositories for RTMP and NGINX, run the NGINX configure command, and then compile NGINX.

$ cd /path/to/build/dir
$ git clone https://github.com/arut/nginx-rtmp-module.git
$ git clone https://github.com/nginx/nginx.git
$ cd nginx
$ ./auto/configure --add-module=../nginx-rtmp-module
$ make
$ sudo make install

# Configuring NGINX

You must configure NGINX to function as an RTMP server which is where the video will be transmitted by the source.
Edit the configuration file </usr/local/nginx/conf/nginx.conf> for the following content. 


worker_processes  auto;
events {
    worker_connections  1024;
}

rtmp {
    server {
        listen 1935;
        chunk_size 4000;

        application live {
            live on;
            interleave on;
            wait_key on;
            wait_video on;

        }
    }
}


# Validating the Configuration and Starting NGINX

It’s always a good idea to validate your NGINX configuration to make sure there are no syntactic errors. Run this command:

$ sudo /usr/local/nginx/sbin/nginx -t
nginx: the configuration file /usr/local/nginx/conf/nginx.conf syntax is ok
nginx: configuration file /usr/local/nginx/conf/nginx.conf test is successful


# Then run this command to start NGINX:

$ sudo /usr/local/nginx/sbin/nginx

# To stop NGINX run:

$ sudo /usr/local/nginx/sbin/nginx -s stop

# Install FFmpeg

Install FFmpeg from source code to include libx264 encode. The FFmpeg is used to encode the video and transmit it to the RTMP server.


First install the packages required for compiling:

sudo apt-get update -qq && sudo apt-get -y install \
  autoconf \
  automake \
  build-essential \
  cmake \
  git-core \
  libass-dev \
  libfreetype6-dev \
  libgnutls28-dev \
  libsdl2-dev \
  libtool \
  libva-dev \
  libvdpau-dev \
  libvorbis-dev \
  libxcb1-dev \
  libxcb-shm0-dev \
  libxcb-xfixes0-dev \
  meson \
  ninja-build \
  pkg-config \
  texinfo \
  wget \
  yasm \
  zlib1g-dev

Install the extras encoders:

sudo apt-get install libx265-dev libnuma-dev
sudo apt-get install libx264-dev
sudo apt-get install libvpx-dev
sudo apt-get install libfdk-aac-dev
sudo apt-get install libmp3lame-dev
sudo apt-get install libv4l-dev


Clone the FFmpeg repository, and then compile it enabling the encode libx264.


$ git clone https://git.ffmpeg.org/ffmpeg.git ffmpeg

$ cd ffmpeg

$ ./configure --enable-gpl --enable-nonfree --enable-version3 --enable-libx264 --enable-libx265 --enable-libvpx --enable-libfdk-aac --enable-libmp3lame  --enable-libv4l2
$ make -j$(nproc)
$ sudo make install

See this link to more information https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu#FFmpeg

# Send video stream over RTMP by FFmpeg 

Configure the necessary parameters in file run_live.py and start a video live run the following script "python run_live.py"

Parameters:

RUN_TIME = 400  # run time in sec
SOURCE = '/home/joao/data/videos_harmonic/1_VENICE_5994_UHD_h264.mp4' # path video
RESOLUTION = "360p" # resolutions acepted 360p, 480p, 540p, 720p, 1080p, 2K and 4K
KEY = 'veneza' # You define a personalized RTMP channel key

MM_DELAY = 40   # Network delay in millisec 
downlink = "/usr/share/mahimahi/traces/Verizon-LTE-short.down" # Path to file in Mahihi format
uplink = "/usr/share/mahimahi/traces/Verizon-LTE-short.up"     # Path to file in Mahihi format


# Watching the streaming with VLC media player

Once video is streaming, you can test that NGINX is correctly serving it using the protocols you have configured. Open the VLC media player and accesses the appropriate URL for playback. In the URLs, NGINX_server is the IP address or hostname of his NGINX server:

$ sudo snap install vlc

Open the VLC player and open the URL network stream

rtmp://NGINX_server:1935/live/$KEY






