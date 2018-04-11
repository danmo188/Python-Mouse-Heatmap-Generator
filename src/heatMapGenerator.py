from win32api import GetSystemMetrics
import win32api
from datetime import datetime
from pynput import mouse
import threading
import numpy
from tkinter import *
import matplotlib.pyplot as plt

stopFlag = False
lock = threading.Lock()
resolutionx = GetSystemMetrics(0)
resolutiony = GetSystemMetrics(1)

#how many times per second will the program read the mouse positon
READ_RATE = 0.1

viablex = 64
viabley = 36


#heatmap = [[0 for x in range(viablex)] for y in range(viabley)]
heatmap = []

def printheatmap():
	print(numpy.matrix(heatmap))

def click(x, y, button, pressed):
	global stopFlag
	stopFlag = True
	printheatmap()
	return False
	


def startcollection():
	global stopFlag
	global status
	
	if not stopFlag:
		threading.Timer(READ_RATE,startcollection).start()
	lock.acquire()
	try:
		x,y = win32api.GetCursorPos()
		x = x // (resolutionx // viablex)
		y = y // (resolutiony // viabley)
		val = heatmap[y][x]
		heatmap[y][x] = val + 1
	finally:
		lock.release()

def heatmaptofile():
	global heatmap
	numpy.savetxt('heatmap.dmo',heatmap,fmt='%d')
	plt.clf()
	plt.title("my map")
	plt.ylabel('y')
	plt.xlabel('x')
	plt.imshow(heatmap)
	plt.show()

def stopcollection():
	global stopFlag
	global status
	
	stopFlag = True

#initialize heatmap data structure
def initheatmap():
	for i in range(viabley):
		heatmap.append([])
		for j in range(viablex):
			heatmap[i].append(0)

def changeRate(rate):
	global READ_RATE
	newrate = rate
	if rate[0] == '.':
		newrate = '0' + rate
	READ_RATE = float(rate)

def main():
	global stopFlag
	global status
	display = Tk()
	ratelabel = Label(display,text='Rate (per sec)')

	
	rate = Entry(display)
	buttonStart = Button(display,text='START',fg='blue',command=startcollection)
	buttonStop = Button(display,text='STOP',fg='green',command=stopcollection)
	buttonPrint = Button(display,text='Print Results to File',fg='red',command=heatmaptofile)
	buttonSubmit = Button(display,text='Submit',fg='purple',command= lambda: changeRate(rate.get()))
	
	ratelabel.grid(row=0)
	rate.grid(row=0,column=1)
	buttonSubmit.grid(row=0,column=2)
	buttonStart.grid(row=1,column=0)
	buttonStop.grid(row=1,column=1)
	buttonPrint.grid(row=1,column=2)
	
		
	initheatmap()
	display.title('Heatmap Generator')
	display.mainloop()
   
main()