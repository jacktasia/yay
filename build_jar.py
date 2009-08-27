# Copyright (c) 2009 John (Jack) Angers, jacktasia@gmail.com
# Licensed under the terms of the MIT License (see LICENSE.txt)

import os


## TODO
def runit(cmd):
	os.system(cmd)
	print "Ran: %s." % cmd

if __name__ == '__main__':
	if os.name == 'posix':
		rm_cmd = 'rm'
		rmd_cmd = 'rm -r'
		cp_cmd = 'cp'
	elif os.name == 'nt':
		rm_cmd = 'del'
		rmd_cmd = 'rmdir /s /q'
		cp_cmd = 'copy'
	else:
		pass

	runit('%s yay.jar' % rm_cmd)
	runit('%s cachedir' % rmd_cmd)
	
	runit("javac -classpath jythonlib.jar *.java")
	runit("%s jythonlib.jar yay.jar" % cp_cmd)
	runit("jar ufm yay.jar manifest.txt *.class *.py *.gif")

	#runit('%s *.class' % rm_cmd)
	
	runit('java -jar yay.jar')
	#maybe use API to upload directly to "Downloads" section
