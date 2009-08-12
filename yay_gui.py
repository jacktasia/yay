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

class RunThread(threading.Thread):
	def start_config(self):
		os_name =  System.getProperty('os.name')
		self.os_sep = File.separator	
		self.has_dir = True
		
		app_name = 'Yay'
		filename = 'config.pkl'
		if os_name == 'Windows':
		    self.config_dir = os.environ["APPDATA"] + self.os_sep + app_name + self.os_sep
		else:
		    self.config_dir = os.path.expanduser("~") + self.os_sep + '.' + app_name + self.os_sep
		self.config_path = self.config_dir + filename #'server_config.ini'
		if not os.path.exists(self.config_dir):
			os.makedirs(self.config_dir)
			self.has_dir = False
			self.set_dir()
		self.config = self.get_dir()
		self.dir = self.config['browse_folder']

		self.ticks = 5
		self._stopevent = threading.Event()
		self._sleepperiod = 1.0
		self.cdd_cmd = "gconftool-2 --set /desktop/gnome/background/picture_filename --type=string \"%s\""
		
		threading.Thread.__init__(self,name='GoGo')
		self.file_count = 0;
		self.countsec = 0
		self.is_paused = False
		self.first_start = True
		#should just call loadup or similar DRY..shoudl be listing image files
		self.workingdir = dircache.listdir(self.dir)
		self.workingdir_size = len(self.workingdir)
		self.last_off()
		self.updateLabel()

	def get_has_dir(self):
		return self.has_dir

	## need like a set_config...so we can have like config['pause_time']
	def set_dir(self):
		config = {}
		dir = str(self.getDirectory()).strip() + self.os_sep
		config['browse_folder'] =  dir 
		output = open(self.config_path,'wb')
		pickle.dump(config,output)
		output.close()
		self.has_dir = True
		self.dir = dir 
		self.loadup()
		#self.do_change()

	def get_dir(self):
		f = open(self.config_path,'rb')
		config = pickle.load(f)
		f.close()
		return config

	def set_ticks(self,ticks):
		self.ticks = ticks

	def goto_img(self,i):
		if i >= 0 and i < self.workingdir_size + 1:
			print "setting"
			self.file_count = i - 1
			self.do_change()

	def last_off(self):
		#this finds out the current desktop and if is the current selected folder...
		cur_path = os.popen("gconftool-2 --get /desktop/gnome/background/picture_filename").read().strip()
		count=0;
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
		if self.first_start:
			self.start()
			self.do_change()
			self.first_start = False
		else:
			self.is_paused = False
		
	def pause(self):
		if not self.is_paused:

			self.is_paused = True
		else:
			self.is_paused = False

	def run(self):
		while not self._stopevent.isSet():
			self.countsec +=1
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
		self.workingdir = dircache.listdir(self.dir)
		self.workingdir_size = len(self.workingdir)
		self.updateLabel()

	def last(self):
		if self.file_count-1 > 0:
			self.file_count -= 1
		else:
			self.file_count = self.workingdir_size -1
		self.do_change()
			
	def do_change(self):
		self.updateLabel()
		self.countsec = 0
		b = self.cdd_cmd % (self.dir + self.workingdir[self.file_count])
		print b
		os.system(b)

	def next(self):
		if self.file_count+1 < self.workingdir_size:
			self.file_count += 1
		else:
			self.loadup()

		self.do_change()
	
	def updateLabel(self):
		m = str(self.file_count+1) + "/" + str(self.workingdir_size)
		self.lblStatus.setText(m)
	
class YayGui(RunThread):
	def __init__(self):
		self.frame = swing.JFrame('Yay')
		self.frame.windowClosing = self.goodbye
		self.frame.contentPane.layout = awt.GridLayout(4,2)
		self.is_paused = True
		panel = swing.JPanel()
		###
		menuBar = swing.JMenuBar()
		editMenu = swing.JMenu("File");
		menuItemSettings = swing.JMenuItem("Settings",actionPerformed=self.showSettings) # will actually start it
		menuItemReload = swing.JMenuItem("Reload Folder",actionPerformed=self.callReload)
		menuItemChangeFolder = swing.JMenuItem("Change Folder",actionPerformed=self.callSetDir)

		editMenu.add(menuItemReload)	
		editMenu.add(menuItemChangeFolder);	
		editMenu.add(menuItemSettings)
		menuBar.add(editMenu)
		self.frame.setJMenuBar(menuBar);
		###
		self.btnPrev = swing.JButton('<<',actionPerformed=self.callLast)
		panel.add(self.btnPrev)
		self.btnStart = swing.JButton("Start", actionPerformed=self.callStart)
		panel.add(self.btnStart)
		self.btnNext = swing.JButton('>>',actionPerformed=self.callNext)
		panel.add(self.btnNext)
		self.lblStatus = swing.JTextField("????????",7,keyPressed=self.callGoEnter)
		panel.add(self.lblStatus)
		self.btnGo = swing.JButton('Go',actionPerformed=self.callGoClick)
		panel.add(self.btnGo)
		self.start_config()
		self.frame.setContentPane(panel)

		self.frame.size = (339,90)
		self.frame.resizable = False
		self.frame.show()
	
	def showSettings(self,event): # bad name..should be setPauseLength or something
		print "settings"
		swing.JOptionPane.showInputDialog(
                    None,
                   "How many seconds before changing background?",
                    swing.JOptionPane.PLAIN_MESSAGE,
                    None,
                    None,
                    "4")

	
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
			return fc.getSelectedFile()
		else:
			return self.getDirectory()

	def callStart(self,event):
		if self.is_paused:
			self.doStart()
			self.is_paused = False
			self.btnStart.setText("Pause")

		else:
			self.pause()
			self.is_paused = True
			self.btnStart.setText("Start")
	
	def goodbye(self,event):
		sys.exit()

if __name__ == '__main__':
	y = YayGui()

