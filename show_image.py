import java.awt as awt
from java.io import *
from javax.imageio import ImageIO
from javax.swing import JFrame,JButton

class ShowImage(awt.Panel):

    def __init__(self,img_path):
        self.image = ImageIO.read(File(img_path))

    def paint(self,g):
        g.drawImage(self.image,0,0,None)

class ShowImageViewer:
    def __init__(self):
        self.frame = JFrame("Display Image")

        btn = JButton("Switch",actionPerformed=self.switchPic)
        #self.frame.getContentPane().add(btn)
        self.switchPic('/home/jack/Desktop/mgarvin.jpg')
        self.frame.setSize(500,500)
        self.frame.setVisible(True)

    def callSwitchPic(self,event):
        self.switchPic('/home/jack/Desktop/mteam.jpg')
    
    def switchPic(self,image):
        panel = ShowImage(image)
        self.frame.getContentPane().add(panel)        
        


if __name__ == '__main__':
    ShowImageViewer()
