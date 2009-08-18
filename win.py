import java.io.File as File
import javax.imageio.ImageIO as ImageIO

import os



def reload_bg():
	print "running rundll"
	c = "RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters"
	os.system(c)
	
def reset_reg(src):
	# ugly hack to get it how we need it
	sep = os.sep + os.sep
	s = src.split('\\')
	b = sep.join(s)
	r = """REGEDIT4

[HKEY_CURRENT_USER\Control Panel\Desktop]
"Wallpaper" = "%s" """ % (b)
	f = open('C:\\test.reg','w')
	f.write(r)
	f.close()
	os.system("regedit /s C:\\test.reg")

def jpg2bmp(src):
	# load jpg
	
	b = bmp_name(src)
	f = File(src)
	image = ImageIO.read(f)
	output = File(b)
	ImageIO.write(image,"bmp",output)
		
def make_bg(src):
	if not bmp_exists(src):
		jpg2bmp(src)
		
	b = bmp_name(src)
	reset_reg(b)
	reload_bg()
		

def bmp_name(f):
	import md5
	m = md5.new()
	m.update(f)
	return "C:\\Windows\\Temp\\" + m.hexdigest() + '.bmp'

def bmp_name_old(src):
	a = src.split('.')
	b = str(a[:len(a)-1][0]) + '.bmp'
	return b
	
def bmp_exists(src):
	return os.path.exists(bmp_name(src))
		
		
if __name__ == '__main__':
	make_bg("C:\\Documents and Settings\\jack\\Desktop\\jayhawk.jpg")
