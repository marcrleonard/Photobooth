#!/bin/bash

killall gphoto2

# gphoto2 --capture-movie --stdout | /Applications/VLC.app/Contents/MacOS/VLC - > /dev/null 2>&1 &

gphoto2 --capture-movie --stdout | /Applications/VLC.app/Contents/MacOS/VLC --sub-source="marq{marquee=press the green button. 3 pictures will be taken,color=0xFFFFFF}" --marq-position=8 - > /dev/null 2>&1 &

# gphoto2 --capture-movie --stdout | /Applications/VLC.app/Contents/MacOS/VLC --sub-source="marq{marquee=press the green button. 3 pictures will be taken,color=0xFFFFFF}" --marq-position=8 - > /dev/null 2>&1 &


# ffmpeg -f image2 -i Photobooth_%003d.jpg -vf "$filters" -gifflags +transdiff -framerate 9 -vf scale=1296x864 -y out5.gif

#ffmpeg -f image2 -i Photobooth_%003d.jpg -framerate 10 -vf scale=1296x864 -y out1.mp4



#theoretical instagram... 
#ffmpeg -framerate 10 -i Photobooth_%003d.jpg -s 1920x1080 -c:v libx264 -strict experimental -b:a 3000k -vf "fps=24,format=yuv420p" -shortest -y insta_test.mp4



#works... but the size is wrong. 
#ffmpeg -f image2 -framerate 10 -i Photobooth_%003d.jpg -s 1920x1080 -c:v libx264 -strict experimental -b:a 3000k -vf "fps=30,format=yuv420p" -shortest -y insta_test.mp4


# omxplayer fifo.mjpg --live


# --no-rc-show-pos

