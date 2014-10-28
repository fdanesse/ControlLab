gst-launch-1.0 ximagesrc startx=0 endx=800 starty=0 endy=600 ! \
    videoconvert ! x264enc ! rtph264pay ! udpsink host=192.168.1.9 port=5001
