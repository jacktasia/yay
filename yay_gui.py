#!/home/v/jython2.5.0/bin/jython
# jack angers
# jacktasia@gmail.com
# boo

import java.awt as awt
import javax.swing as swing
import java.lang as lang
from java.lang import System
from java.io import File

import threading
import dircache
import os
import sys
import pickle
import math

# used in reloadTime filter so only image files are "seen"/counted
def img_only(f):
	exts = ['png','jpg','gif','jpeg','bmp']
	e = f.split('.')
	ext = e[len(e)-1].lower()
	if ext in exts:
		return True

class RunThread(threading.Thread):
	def start_config(self):
		os_name =  System.getProperty('os.name')
		self.os_sep = File.separator	
		self.has_dir = True
		self.ticks = 30 #default
		self.first_start = False
		self.has_started = False
		
		app_name = 'Yay'
		filename = 'config.pkl'
		if os_name == 'Windows':
		    self.config_dir = os.environ["APPDATA"] + self.os_sep + app_name + self.os_sep
		else:
		    self.config_dir = os.path.expanduser("~") + self.os_sep + '.' + app_name + self.os_sep
		self.config_path = self.config_dir + filename #'server_config.ini'
		self.dir = ''
		if not os.path.exists(self.config_dir):
			self.first_start = True
			os.makedirs(self.config_dir)
			self.has_dir = False
			self.create_config_file()
		else:
			try:
				f = open(self.config_path,'rb')
			except IOError:
				print "file doesn't exist"
				self.first_start = True
				self.create_config_file()
	
		self.dir = self.get_config('browse_folder')
		self.ticks = self.get_config('speed')
		
		if self.dir == '':
			## this should be a dialog alert...
			print "quitting"
			sys.exit()
		else:
			print self.dir


		self._stopevent = threading.Event()
		self._sleepperiod = 1.0
		self.cdd_cmd = "gconftool-2 --set /desktop/gnome/background/picture_filename --type=string \"%s\""
		
		threading.Thread.__init__(self,name='GoGo')
		self.file_count = 0;
		self.countsec = 0
		self.is_paused = True
		self.loadup()		
		self.last_off()
		self.updateLabel()

	def create_config_file(self):
		self.set_dir()
		self.set_speed(self.ticks)

	def get_has_dir(self):
		return self.has_dir

	## need like a set_config...so we can have like config['pause_time']
	def set_dir(self):
		dir = self.getDirectory()
		self.set_config('browse_folder',dir)
		self.has_dir = True
		self.dir = dir 
		self.loadup()
		#self.do_change()

	def set_speed(self,s):
		self.set_config('speed',s)
		self.ticks = s
		self.updateLabel()

	def set_config(self,n,v):
		if not self.first_start:
			config = self.get_config()			
		else:
			config = {}
			self.first_start = False
		config[n] = v
		output = open(self.config_path,'wb')
		pickle.dump(config,output)
		output.close()

	def get_config(self,n=None):
		f = open(self.config_path,'rb')
		config = pickle.load(f)
		f.close()
		if n is not None:
			return config[n]
		else:
			return config
	
	def get_dir(self):
		return self.get_config('browse_folder')

	def set_ticks(self,ticks):
		self.ticks = ticks

	def goto_img(self,i):
		if i >= 0 and i < self.workingdir_size + 1:
			self.file_count = i - 1
			self.do_change()
			
	def prune(self):
		was_playing = False
		if not self.is_paused:
			self.do_pause()
			was_playing = True
			
		if not os.path.exists(self.dir + '_pruned'):
			os.makedirs(self.dir + '_pruned')
		os.rename(self.dir + self.workingdir[self.file_count],
				  self.dir + '_pruned/' +  self.workingdir[self.file_count])
		self.reloadTime()
		if was_playing:
			self.do_start()
		self.do_change()
		  

	def last_off(self):
		#this finds out the current desktop and if is the current selected folder...
		cur_path = os.popen("gconftool-2 --get /desktop/gnome/background/picture_filename").read().strip()
		count = 0;
		found = -1
		b = cur_path.split('/')
		cur_path = b[len(b)-1]
		for a in self.workingdir:
			print "%s == %s" % (a,cur_path)
			if a == cur_path:
				found = count
				break
			count += 1
		if found == -1:
			found = 0
		self.file_count = found
		self.do_change()

	def doStart(self):
		if not self.has_started:
			self.has_started = True
			self.start()
		self.do_change()
		
		
	def pause(self):
		if not self.is_paused:

			self.is_paused = True
		else:
			self.is_paused = False

	def run(self):
		while not self._stopevent.isSet():
			self.countsec +=1
			self.updateTicker()
			if self.countsec > self.ticks and not self.is_paused:
				self.next()
				self.countsec = 0
			elif self.is_paused:
				self.countsec = 0
			self._stopevent.wait(self._sleepperiod)
		
	def loadup(self):
		self.file_count = 0
		self.reloadTime()

	def reloadTime(self):
		self.workingdir = filter(img_only,dircache.listdir(self.dir))
		self.workingdir_size = len(self.workingdir)
		msg = "Selected image directory has no images! Please pick again."
		if self.workingdir_size == 0:
			self.showDialogError(msg)
			self.set_dir()
		self.updateLabel()

	def last(self):
		if self.file_count-1 >= 0:
			self.file_count -= 1
		else:
			self.file_count = self.workingdir_size -1
		self.do_change()
			
	def do_change(self):
		self.updateLabel()
		self.countsec = 0
		b = self.cdd_cmd % (self.dir + self.workingdir[self.file_count])
		print "SETTING: " + self.workingdir[self.file_count]
		os.system(b)

	def next(self):
		if self.file_count+1 < self.workingdir_size:
			self.file_count += 1
		else:
			self.loadup()

		self.do_change()
	
	def updateLabel(self):
		self.lblDirectory.setText(str(self.dir))
		m = str(self.file_count+1) + "/" + str(self.workingdir_size)
		self.lblStatus.setText(m)
		self.lblCurrent.setText(self.workingdir[self.file_count])
		### TODO get best time label...like 360 seconds = 5 minutes
		self.btnSpeed.setText(str(self.ticks) + "s")

	def updateTicker(self):
		self.countMenu.setText(str((self.ticks - self.countsec)+1))
		self.countMenu.updateUI()
	
class YayGui(RunThread):
	def __init__(self):
		self.frame = swing.JFrame('Yay Desktop')
		self.frame.windowClosing = self.goodbye
		self.frame.contentPane.layout = awt.GridLayout(4,2)
		panel = swing.JPanel()
		self.is_mini = False
		self.normal_size = (250,175)
		self.mini_size = (210,120)
		### 		
		# Menu Bar
		##
		#dividers up in here? or split across multiple menus on the bar?
		menuBar = swing.JMenuBar()
		fileMenu = swing.JMenu("File")
		editMenu = swing.JMenu("Edit")
		viewMenu = swing.JMenu("View")
		self.countMenu = swing.JMenu("")
		self.menuMiniMode = swing.JMenuItem("Mini Size",actionPerformed=self.callMiniMode)
		menuItemPrune = swing.JMenuItem("Prune File",actionPerformed=self.callPrune)
		menuItemReload = swing.JMenuItem("Reload Image Folder",actionPerformed=self.callReload)
		menuItemChangeFolder = swing.JMenuItem("Change Image Folder",actionPerformed=self.callSetDir)
		menuItemSetSpeed = swing.JMenuItem("Set Slideshow Speed",actionPerformed=self.showSpeedDialog)
		menuItemQuit = swing.JMenuItem("Quit",actionPerformed=self.goodbye)
		
		viewMenu.add(self.menuMiniMode)
		editMenu.add(menuItemSetSpeed)
		editMenu.addSeparator()
		editMenu.add(menuItemPrune)
		fileMenu.add(menuItemChangeFolder)
		fileMenu.add(menuItemReload)
		fileMenu.addSeparator()
		fileMenu.add(menuItemQuit)
		
		menuBar.add(fileMenu)
		menuBar.add(editMenu)
		menuBar.add(viewMenu)
		menuBar.add(self.countMenu)
		self.frame.setJMenuBar(menuBar)
		### 		
		# Top Panel
		##
		self.panelTop = swing.JPanel()
		self.panelTop.layout = awt.GridLayout(1,1)
		self.lblDirectory = swing.JLabel()
		self.panelTop.add(self.lblDirectory)
		panel.add(self.panelTop)
		### 		
		# Slideshow controls
		##
		panelControls = swing.JPanel()
		panelControls.layout = awt.GridLayout(1,3)
		self.btnPrev = swing.JButton('<<',actionPerformed=self.callLast)
		panelControls.add(self.btnPrev)
		self.btnStart = swing.JButton("Start", actionPerformed=self.callStart)
		panelControls.add(self.btnStart)
		self.btnNext = swing.JButton('>>',actionPerformed=self.callNext)
		panelControls.add(self.btnNext)
		panel.add(panelControls)
		### 		
		# Go controls
		##
		panelGo = swing.JPanel()
		panelGo.layout = awt.GridLayout(1,5)
		panelGo.add(swing.JLabel(" "))
		self.lblStatus = swing.JTextField("????????",3,keyPressed=self.callGoEnter)
		panelGo.add(self.lblStatus)
		self.btnGo = swing.JButton('Go',actionPerformed=self.callGoClick)
		panelGo.add(self.btnGo)
		self.btnSpeed = swing.JButton(actionPerformed=self.showSpeedDialog)
		panelGo.add(self.btnSpeed)
		panelGo.add(swing.JLabel(" "))
		panel.add(panelGo)

		###
		# Sep
		##
		self.panelSep = swing.JPanel()
		self.panelSep.add(swing.JSeparator())
		panel.add(self.panelSep)
		### 		
		# Settings controls
		##
		self.panelSettings = swing.JPanel()
		self.panelSettings.layout = awt.GridLayout(1,1)
		self.lblCurrent = swing.JLabel()
		self.panelSettings.add(self.lblCurrent)
		panel.add(self.panelSettings)
				
		
		###		
		# get the non-gui part running
		##
		self.start_config() 
		### 		
		# Slideshow controls
		##
		self.frame.setContentPane(panel)
		self.frame.size = self.normal_size
		self.frame.resizable = False
		self.frame.show()
	

	def callMiniMode(self,event):
		if not self.is_mini:
			self.startMiniMode()
			self.menuMiniMode.setText("Normal Size")
			self.is_mini = True
		else:
			self.endMiniMode()
			self.menuMiniMode.setText("Mini Size")
			self.is_mini = False
 
 
 	def endMiniMode(self):
		print "starting mini mode"
		self.panelTop.setVisible(True)
		self.panelSep.setVisible(True)
		self.panelSettings.setVisible(True)
		self.frame.preferredSize = self.normal_size
		self.frame.pack()
    
	def startMiniMode(self):
		print "starting mini mode"
		self.panelTop.setVisible(False)
		self.panelSep.setVisible(False)
		self.panelSettings.setVisible(False)
		self.frame.preferredSize = self.mini_size
		self.frame.pack()
        
	def callPrune(self,event):
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
	
	def goodbye(self,event):
		sys.exit()

if __name__ == '__main__':
	y = YayGui()

