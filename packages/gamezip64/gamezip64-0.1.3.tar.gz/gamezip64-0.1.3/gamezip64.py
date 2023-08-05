#!/usr/bin/env python3
import sys
import subprocess
import importlib.util
import os
import random
import string
_towrite='''
import neopixel
from microbit import *
class Screen:
	def __init__(self,pin,size):self.pin=pin;self.size=size;self.__screen=neopixel.NeoPixel(pin,size**2);self.show=self.__screen.show
	def __setitem__(self,i,v):x,y=i;self.__screen[y*self.size+x]=v
	def __getitem__(self,i):x,y=i;return self.__screen[y*self.size+x]
	def set_background(self,c):
		for i in range(size**2):self[(i%8,i//8)]=c
    def clear(self):self.set_background((0,0,0))
def Component(pin):
	class _Component:
        pin=pin
        def on(self):self.pin.write_digital(1)
        def off(self):self.pin.write_digital(0)
        def hold(self,time=1000):self.on();delay(time);self.off()
    return _Component()
def Input(pin):
	class _Input:
		pin=pin
		def pressed(self):return bool(self.pin.read_digital())
    return _Input()
class Buzzer:
	pin=pin2
	def play(self,music,wait=True,loop=False):music.play(music,self.pin,wait,loop)
	def stop(self):music.stop(self.pin)
	def pitch(self,frequency,duration=-1,wait=True):music.pitch(frequency,duration,self.pin,wait)
motor=Component(pin1)
button_up=Input(pin8)
button_right=Input(pin13)
button_down=Input(pin14)
button_left=Input(pin12)
fire_1=Input(pin15)
fire_2=Input(pin16)
buzzer=Buzzer()
screen=Screen(pin0,8)
'''

if importlib.util.find_spec('uflash')is None:
    sys.stderr.write('FATAL:  module "uflash" not found.\nInstall?? [y/n]')
    a=sys.stdin.readline().strip()
    if a.lower()=='y':
        os.system('pip install uflash')
    else:
        sys.stderr.write('FATAL: module "uflash" was not installed. Aborting.\n')
        sys.exit(1)
    if importlib.util.find_spec('uflash')is None:
        sys.stderr.write('FATAL: module "uflash" could not be installed. Aborting.\n')
        sys.exit(1)
class TempFile:
    def __init__(self):
        self.filename='/tmp/tmp-'+''.join(random.choices(string.hexdigits,k=16))+'.py'
        self.name=self.filename
        self.file=open(self.filename,'w')
        self.closed=False
    def write(self,what):
        self.file.write(what)
        self.file.close()
        self.file=open(self.filename,'a')
    def close(self):
        if self.closed:return
        self.file.close()
        self.closed=True
        #os.remove(self.filename)
def main():
    filename=sys.argv[-1]
    print('Reading file...')
    a=open(filename,'r').read()
    print('Building GameZip plugin...')
    a=_towrite+a
    print('Making tempfile...')
    d=TempFile()
    d.write(a)
    x=d.name
    print(f'TempFile ID:  {x}')
    print(f'Flashing {filename!r}...')
    process=subprocess.Popen(['uflash',x],stderr=subprocess.PIPE,stdout=subprocess.PIPE)
    c=process.wait()
    d.close()
    if c>0:
        sys.stderr.write(f'ERROR: uflash crashed with returncode {c}. Reason: {process.stderr.read().decode()}\n')
        d.close()
        sys.exit(1)
    else:
        print('OK')
        sys.exit(0)
if __name__=='__main__':
    main()
