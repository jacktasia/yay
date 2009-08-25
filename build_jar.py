# Copyright (c) 2009 John (Jack) Angers, jacktasia@gmail.com
# Licensed under the terms of the MIT License (see LICENSE.txt)

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
	
	runit('rm ~/Desktop/yay.jar')
	
	runit('rm -rf ~/Desktop/cachedir')
	
	runit("javac -classpath jythonlib.jar *.java")
	
	runit("cp jythonlib.jar yay.jar")
	runit("jar ufm yay.jar manifest.txt *.class *.py *.gif")
	
	runit('cp yay.jar ~/Desktop/')
	runit('java -jar ~/Desktop/yay.jar')
	#maybe use API to upload directly to "Downloads" section
