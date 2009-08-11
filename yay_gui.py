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
	def __init__(self,lblStatus,dir):
		self.ticks = 5
		self._stopevent = threading.Event()
		self._sleepperiod = 1.0
		self.lblStatus = lblStatus
		self.cdd_cmd = "gconftool-2 --set /desktop/gnome/background/picture_filename --type=string \"%s\""
		self.dir = dir  #'/media/disk/pictures/'
		self.workingdir = dircache.listdir(self.dir)
		self.workingdir_size = len(self.workingdir)
		threading.Thread.__init__(self,name='GoGo')
		self.file_count = 0;
		self.countsec = 0
		self.is_paused = False
		self.first_start = True
		self.last_off()
		self.updateLabel()

	def set_dir(self,dir):
		self.dir = dir
		self.loadup()

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
		
class YayGui:
	def __init__(self):
		### CONFIG
		os_name =  System.getProperty('os.name')
		os_sep = File.separator
		self.os_sep = os_sep		
		app_name = 'Yay'
		filename = 'config.pkl'
		if os_name == 'Windows':
		    self.config_dir = os.environ["APPDATA"] + os_sep + app_name + os_sep
		else:
		    self.config_dir = os.path.expanduser("~") + os_sep + '.' + app_name + os_sep
		self.config_path = self.config_dir + filename #'server_config.ini'
		if not os.path.exists(self.config_dir):
			os.makedirs(self.config_dir)
			self.setDir()
		self.config = self.getDir()
		### GUI
		self.frame = swing.JFrame('Yay')
		self.frame.windowClosing = self.goodbye
		self.frame.contentPane.layout = awt.GridLayout(4,2)
		self.is_paused = True
		panel = swing.JPanel()
		self.btnPrev = swing.JButton('<<',actionPerformed=self.callLast)
		panel.add(self.btnPrev)
		self.btnStart = swing.JButton("Start", actionPerformed=self.callStart)
		panel.add(self.btnStart)
		self.btnNext = swing.JButton('>>',actionPerformed=self.callNext)
		panel.add(self.btnNext)
		self.lblStatus = swing.JTextField("????????",keyPressed=self.callGoEnter)
		panel.add(self.lblStatus)
		self.btnGo = swing.JButton('Go',actionPerformed=self.callGoClick)
		panel.add(self.btnGo)
		self.t = RunThread(self.lblStatus,self.config['browse_folder'])
		self.frame.setContentPane(panel)

		self.frame.size = (339,83)
		self.frame.show()
	
	def setDir(self):
		config = {}
		bf = str(self.getDirectory())
		config['browse_folder'] =  bf.strip() + self.os_sep
		output = open(self.config_path,'wb')
		pickle.dump(config,output)
		output.close()
		return config['browse_folder']
		

	def getDir(self):
		f = open(self.config_path,'rb')
		config = pickle.load(f)
		f.close()
		return config
	
	def callGoEnter(self,event):
		if event.keyCode == 10:
			self.callGo()

	def callGoClick(self,event):
		self.callGo()

	def callGo(self):
		reqt = self.lblStatus.getText()

		if reqt == 'reload':
			self.t.reloadTime()		
		elif reqt.find('sec') != -1:
			ticks = int(reqt.split('sec')[0])
			self.t.set_ticks(ticks)
		elif reqt.find('setdir') != -1:
			dir = self.setDir()
			self.t.set_dir(dir)
			self.frame.pack
		else:
			self.t.goto_img(int(reqt))

	def callLast(self,event):
		self.t.last()

	def callNext(self,event):
		self.t.next()

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
			self.t.doStart()
			self.is_paused = False
			self.btnStart.setText("Pause")

		else:
			self.t.pause()
			self.is_paused = True
			self.btnStart.setText("Start")
	
	def goodbye(self,event):
		sys.exit()

if __name__ == '__main__':
	y = YayGui()

