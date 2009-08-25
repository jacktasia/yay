# Copyright (c) 2009 John (Jack) Angers, jacktasia@gmail.com
# Licensed under the terms of the MIT License (see LICENSE.txt)
import os

def change_desktop(src):
	cmd = "gconftool-2 --set /desktop/gnome/background/picture_filename --type=string \"%s\""	
	
	os.system(cmd % src)
