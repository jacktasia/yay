# jack angers
# jacktasia@gmail.com
# boo

import os

def change_desktop(src):
	cmd = "gconftool-2 --set /desktop/gnome/background/picture_filename --type=string \"%s\""	
	
	os.system(cmd % src)
