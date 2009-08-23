# jack angers
# jacktasia@gmail.com
# boo

import java.awt as awt
import javax.swing as swing
import sys

class YaySystemTray:
	def buildSystemTray(self):
		tray = awt.SystemTray.getSystemTray()
		self.popup = awt.PopupMenu()
		exitItem = awt.MenuItem("Exit",actionPerformed=self.callExit)
		self.popup.add(exitItem)
		self.showHideItem = awt.MenuItem("Hide",actionPerformed=self.handleShowHide)
		self.popup.add(self.showHideItem)
		icon = awt.Toolkit.getDefaultToolkit().getImage("yay16.gif") 
		trayIcon = awt.TrayIcon(icon,"yay", self.popup, mousePressed=self.showTrayMenu)
		tray.add(trayIcon)
		
	def callExit(self,event):
		self.doExit()
		
	def showTrayMenu(self,event):
		print "showing window"
		
	def handleShowHide(self,event):
		cur_val = self.showHideItem.getLabel()
		if cur_val == "Hide":
			self.hideFrame()
			self.showHideItem.setLabel("Show")
		elif cur_val == "Show":
			self.showFrame()
			self.showHideItem.setLabel("Hide")
		

if __name__ == '__main__':
	YaySystemTray()
