import java.awt as awt
import javax.swing as swing
import sys
## Just testing...should be more generic (passed icon_file,title)


class YaySystemTray:
	def buildSystemTray(self):
		tray = awt.SystemTray.getSystemTray()
		self.popup = awt.PopupMenu()
		exitItem = awt.MenuItem("Exit",actionPerformed=self.doExit)
		self.popup.add(exitItem)
		self.popup.add(awt.MenuItem("Hide"))
		icon = awt.Toolkit.getDefaultToolkit().getImage("yay24.png") 
		trayIcon = awt.TrayIcon(icon,"yay", self.popup, mousePressed=self.showTrayMenu)
		tray.add(trayIcon)
		
	def doExit(self,event):
		sys.exit()
		
	def showTrayMenu(self,event):
		print "showing window"

if __name__ == '__main__':
	YaySystemTray()
