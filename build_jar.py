
import os
JYTHON_PATH = '/home/v/jython2.5.0/'
HOME_PATH = '/home/v/Desktop/yay/'
## TODO
def runit(cmd):
	#a = subprocess.Popen(cmd,shell=True)
	os.system(cmd)
	print "ran: " + cmd



if __name__ == '__main__':
	runit('rm *.class')
	runit('rm yay.jar')
	
	runit('rm ~/Desktop/yar.jar')
	
	runit("javac -classpath jythonlib.jar *.java")
	
	runit("cp jythonlib.jar yay.jar")
	runit("jar ufm yay.jar manifest.txt *.class *.py *.gif")
	
	runit('cp yay.jar ~/Desktop/')
	runit('java -jar ~/Desktop/yay.jar')
	#maybe use API to upload directly to "Downloads" section
