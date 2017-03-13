import os, platform, glob
from subprocess import Popen, PIPE
from subprocess import call
import sys
from sys import platform
import subprocess




def get_os():
    if platform == "linux" or platform == "linux2":
        print("using Linux Run")
    if platform == "darwin":
        print("using Windows Run")
    if platform == "win32":
        print("using windows Run")

os.system('killall PTPCamera')

def get_Operation():
    os.system('/Users/marcleonard/Desktop/Photobooth/./live_view.sh > /dev/null 2>&1 &')
    input('Press any key to continue!')
    Type_Of_Operation = 'Encode'
    return Type_Of_Operation
Type_Of_Operation = get_Operation()

def take_sequence():
    os.system('/Users/marcleonard/Desktop/Photobooth/./take_sequence.sh')



def type_of_run():
    if Type_Of_Operation == 'Encode':
        take_sequence()
type_of_run()
