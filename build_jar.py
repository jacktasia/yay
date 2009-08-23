
import subprocess

JYTHON_PATH = '/home/v/jython2.5.0/'
HOME_PATH = '/home/v/Desktop/yay/'
## TODO
def runit(cmd):
	a = subprocess.Popen(cmd,shell=True)
	print "ran: " + cmd


if __name__ == '__main__':
	runit('rm *.class')
	runit("javac -classpath jythonlib.jar *.java")
	runit("cp jythonlib.jar yay.jar")
	runit("jar ufm yay.jar manifest.txt *.class *.py *.gif")
	#maybe use API to upload directly to "Downloads" section
