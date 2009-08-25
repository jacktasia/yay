# jack angers
# jacktasia@gmail.com
# boo

import sys
import java.awt as awt
import javax.swing as swing
import java.lang as lang
import java.lang.System as System
import java.io.File as File

import threading
import dircache
import os
import pickle
import math

from yay_core import YayCore
from tray import YaySystemTray
from yay_gui_core import YayGuiCore

class YayGui(YayCore,YayGuiCore,YaySystemTray):
	def __init__(self):
		self.is_mini = False
		self.normal_size = (220,130)
		self.buildSystemTray()
		self.buildGui()			
		###		
		# get the non-gui part running
		##
		self.start_config() 

	def callPrune(self,event):
		
		options = ("Prune it!",
					"Don't move my files!")
		x = swing.JOptionPane.showOptionDialog(
					None,
					"This will move this image file into a subfolder called '_pruned' This will remove it from the slide show.",
					"Slideshow Speed",
					swing.JOptionPane.YES_NO_OPTION,
					swing.JOptionPane.QUESTION_MESSAGE,
					None,
					options,
					options[1])	
		x = int(x)
		if x == 0:
			self.prune()
		
	def showSpeedDialog(self,event): # bad name..should be setPauseLength or something
		self.setSpeed()
		
	def add_s(self,num,word):
		num = math.floor(num)
		if num == 1:
			return str(num) + " " + word 
		else:
			return str(num) + " " + word + "s"
			
	def pretty_speed(self,s):
		m = 0
		h = 0
		if s > 60:
			m = s/60
		else:
			return self.add_s(s,'second')
		if m > 60:
			h = m/60
		else:
			return self.add_s(m,'minute')
		return self.add_s(h,'hour')

	def setSpeed(self):
		options = ("Normal Change Speed",
					"Advanced Change Speed",
					"No Change")
		x = swing.JOptionPane.showOptionDialog(
					None,
					"Speed is currently: " + self.pretty_speed(self.ticks),
					"Slideshow Speed",
					swing.JOptionPane.YES_NO_CANCEL_OPTION,
					swing.JOptionPane.QUESTION_MESSAGE,
					None,
					options,
					options[2])
					
		x = int(x)
		
		if x == 0:
			self.setNormalSpeed()
		elif x == 1:
			self.setAdvancedSpeed()
		# no changing...
	
	def setNormalSpeed(self):
		opts = ("5 seconds","10 seconds","30 seconds","45 seconds",
				"1 minute",
				"5 minutes","10 minutes","15 minutes","30 minutes",
				"45 minutes","1 hour","2 hours","4 hours","8 hours")
		# above but in seconds for set_speed
		opt_values = (5,10,30,45,
					60,
					300,600,900,1200,
					2700,3600,7200,14400,28800)
					
		x = swing.JOptionPane.showInputDialog(
					None,
					"Stay on each image for:",
					"Set Slideshow Speed Normal",
					swing.JOptionPane.PLAIN_MESSAGE,
					None,
					opts,
					opts[0])
		# i am sure the following can be shorter
		if x is not None and len(x) > 0:
			count = 0
			save = 0
			for i in opts:
				if x == i:
					save = count
					break
				count += 1
			if save != 0:
				self.set_speed(opt_values[save])
				
	def setAdvancedSpeed(self):
		a = swing.JOptionPane.showInputDialog(
                    None,
                   "Stay on each image for how many seconds?",
                   "Set Slideshow Speed Advanced",
                    swing.JOptionPane.PLAIN_MESSAGE,
                    None,
                    None,
                    str(self.ticks))
		
		if a is not None:
			if a.isdigit():
				if int(a) > 28800:
					self.showDialogError("28800 seconds (8 hours) is max")
					self.setSpeed()
				else:	
					self.set_speed(int(a))
			else:
				self.showDialogError("Not a number!")
				self.setSpeed()

		
	def showDialogError(self,msg):
		swing.JOptionPane.showMessageDialog(None,msg,
			"Error: Boo...",
			swing.JOptionPane.ERROR_MESSAGE)

	def callSetDir(self,event):
		self.set_dir()

	def callReload(self,event):
		self.reloadTime()

	def callGoEnter(self,event):
		if event.keyCode == 10:
			self.callGo()

	def callGoClick(self,event):
		self.callGo()

	def callGo(self):
		reqt = self.lblStatus.getText()

		if reqt == 'reload':
			self.reloadTime()		
		elif reqt.find('sec') != -1:
			ticks = int(reqt.split('sec')[0])
			self.set_ticks(ticks)
		elif reqt.find('setdir') != -1:
			self.set_dir()
		elif reqt.find('/') != -1:
			self.goto_img(int(reqt.split('/')[0]))
		else:
			self.goto_img(int(reqt))

	def callLast(self,event):
		self.last()

	def callNext(self,event):
		self.next()

	def getDirectory(self):
		fc = swing.JFileChooser()
		fc.setFileSelectionMode(swing.JFileChooser.DIRECTORIES_ONLY)
		rv = fc.showDialog(None,"Pick")
		if rv == swing.JFileChooser.APPROVE_OPTION:
			return  str(fc.getSelectedFile()).strip() + self.os_sep
		else:
			return self.dir

	def callStart(self,event):
		if self.is_paused:
			self.do_start()
		else:
			self.do_pause()
	
	
	def do_start(self):
		self.doStart()
		self.is_paused = False
		self.btnStart.setText("Pause")
	
	def do_pause(self):
		self.pause()
		self.is_paused = True
		self.btnStart.setText("Start")	
		
	def showFrame(self):
		self.frame.show()
		
	def hideFrame(self):
		self.frame.hide()
	
	def goodbye(self,event):
		self.doExit()
		
	def doExit(self):
		## have them confirm exit...
		System.exit(0)

if __name__ == '__main__':
	y = YayGui()

