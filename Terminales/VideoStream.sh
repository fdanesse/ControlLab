gst-launch-0.10 ximagesrc startx=0 endx=800 starty=0 endy=600 ! \
    ffmpegcolorspace ! x264enc ! udpsink host=192.168.1.8 port=5001
