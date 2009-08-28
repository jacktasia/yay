# Copyright (c) 2009 John (Jack) Angers, jacktasia@gmail.com
# Licensed under the terms of the MIT License (see LICENSE.txt)

import os

## TODO
def runit(cmd):
	os.system(cmd)
	print "Ran: %s." % cmd

if __name__ == '__main__':
        os_name = os.name
		# if run with jython, python does this faster faster
        if os_name == 'java':
                import java.lang.System as System
                if System.getProperty('os.name').find('Windows') != -1:
                        os_name = 'nt'
                else:
                        os_name = 'posix'
	if os_name == 'posix':
		rm_cmd = 'rm'
		rmd_cmd = 'rm -r'
		cp_cmd = 'cp'
	elif os_name == 'nt':
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

	runit('%s *.class' % rm_cmd)
	
	runit("javac YayPrefs.java")
	
	runit('java -jar yay.jar')
	#maybe use API to upload directly to "Downloads" section
