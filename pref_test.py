from java.util.prefs import *

from java.lang import Object

import YayPrefs;

class PrefTest:
	def __init__(self):
		self.pref = Preferences.userNodeForPackage(YayPrefs().getClass())
		self.pref_defaults = {}
		
	def set(self,n,v):
		self.pref.put(n,v)
		
	def get(self,n):
		return self.pref.get(n,'')
		
		
if __name__ == '__main__':
	p = PrefTest()
	
	c = p.get('color')
	
	if c == '':
		p.set('color','orange')
		print 'set'
	else:
		print c
