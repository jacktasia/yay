import java.awt as awt
import javax.swing as swing

def tryTray():
	tray = awt.SystemTray.getSystemTray()
	popup = awt.PopupMenu()
	icon = awt.Toolkit.getDefaultToolkit().getImage("yay.png")

	trayIcon = awt.TrayIcon(icon,"yay", popup)
	tray.add(trayIcon)





if __name__ == '__main__':
	tryTray()
