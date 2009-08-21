import java.awt as awt
import javax.swing as swing

## Just testing...should be more generic (passed icon_file,title)

def tryTray():
	tray = awt.SystemTray.getSystemTray()
	popup = awt.PopupMenu()
	icon = awt.Toolkit.getDefaultToolkit().getImage("yay16.png") 

	trayIcon = awt.TrayIcon(icon,"yay", popup)
	tray.add(trayIcon)

if __name__ == '__main__':
	tryTray()
