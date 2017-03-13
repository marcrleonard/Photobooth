#!/bin/bash
killall gphoto2
ps aux | grep -i VLC | awk '{print $2}' | xargs sudo kill -9
sleep 5
#gphoto2 --capture-image-and-download --keep -F 5 -I 2 --filename=Photobooth_%f.%C.jpg
gphoto2 --capture-image-and-download --keep -F 10 -I 2 --filename=Photobooth_%03n.jpg

#boomarong!!!!
ffmpeg -i Photobooth_%003d.jpg -start_number 011 -vf reverse Photobooth_%003d.jpg && ffmpeg -i Photobooth_%003d.jpg -start_number 021 Photobooth_%003d.jpg && ffmpeg -f image2 -framerate 10 -i Photobooth_%003d.jpg -s 1920x1280 -c:v libx264 -strict experimental -b:a 3000k -vf "fps=24,format=yuv420p" -shortest -y insta_test.mp4

killall gphoto2
/Applications/VLC.app/Contents/MacOS/VLC --loop insta_test.mp4 > /dev/null 2>&1 &
#/Applications/VLC.app/Contents/MacOS/VLC Photobooth* > /dev/null 2>&1 &
sleep 10
ps aux | grep -i VLC | awk '{print $2}' | xargs sudo kill -9
mv Photobooth* Images/
python3 Master_Script.py