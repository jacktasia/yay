
import sys
import java.awt as awt
import javax.swing as swing
import java.lang as lang
import java.lang.System as System
import java.io.File as File

import threading
import dircache
import os
import pickle
import math


class YayGuiCore:

	def buildGui(self):
		
		self.frame = swing.JFrame('Yay Desktop')
		self.frame.windowClosing = self.handleShowHide
		self.frame.contentPane.layout = awt.GridLayout(4,2)
		panel = swing.JPanel()
		### 		
		# Menu Bar
		##
		#dividers up in here? or split across multiple menus on the bar?
		menuBar = swing.JMenuBar()
		fileMenu = swing.JMenu("File")
		editMenu = swing.JMenu("Edit")
		viewMenu = swing.JMenu("View")
		self.countMenu = swing.JMenu("")
		self.menuMiniMode = swing.JMenuItem("Mini Size",actionPerformed=self.callMiniMode)
		menuItemPrune = swing.JMenuItem("Prune File",actionPerformed=self.callPrune)
		menuItemReload = swing.JMenuItem("Reload Image Folder",actionPerformed=self.callReload)
		menuItemChangeFolder = swing.JMenuItem("Change Image Folder",actionPerformed=self.callSetDir)
		menuItemSetSpeed = swing.JMenuItem("Set Slideshow Speed",actionPerformed=self.showSpeedDialog)
		menuHide = swing.JMenuItem("Hide",actionPerformed=self.handleShowHide)
		menuItemQuit = swing.JMenuItem("Exit",actionPerformed=self.goodbye)
		
		viewMenu.add(self.menuMiniMode)
		editMenu.add(menuItemSetSpeed)
		editMenu.addSeparator()
		editMenu.add(menuItemPrune)
		fileMenu.add(menuItemChangeFolder)
		fileMenu.add(menuItemReload)
		fileMenu.addSeparator()
		fileMenu.add(menuHide)
		fileMenu.add(menuItemQuit)
		
		menuBar.add(fileMenu)
		menuBar.add(editMenu)
		menuBar.add(viewMenu)
		menuBar.add(self.countMenu)
		self.frame.setJMenuBar(menuBar)
		### 		
		# Top Panel
		##
		self.panelTop = swing.JPanel()
		self.panelTop.layout = awt.GridLayout(1,1)
		self.lblDirectory = swing.JLabel()
		self.panelTop.add(self.lblDirectory)
		panel.add(self.panelTop)
		### 		
		# Slideshow controls
		##
		panelControls = swing.JPanel()
		panelControls.layout = awt.GridLayout(1,3)
		self.btnPrev = swing.JButton('<<',actionPerformed=self.callLast)
		panelControls.add(self.btnPrev)
		self.btnStart = swing.JButton("Start", actionPerformed=self.callStart)
		panelControls.add(self.btnStart)
		self.btnNext = swing.JButton('>>',actionPerformed=self.callNext)
		panelControls.add(self.btnNext)
		panel.add(panelControls)
		### 		
		# Go controls
		##
		panelGo = swing.JPanel()
		panelGo.layout = awt.GridLayout(1,5)
		panelGo.add(swing.JLabel(" "))
		self.lblStatus = swing.JTextField("????????",3,keyPressed=self.callGoEnter)
		panelGo.add(self.lblStatus)
		self.btnGo = swing.JButton('Go',actionPerformed=self.callGoClick)
		panelGo.add(self.btnGo)
		self.btnSpeed = swing.JButton(actionPerformed=self.showSpeedDialog)
		panelGo.add(self.btnSpeed)
		panelGo.add(swing.JLabel(" "))
		panel.add(panelGo)

		###
		# Sep
		##
		self.panelSep = swing.JPanel()
		self.panelSep.add(swing.JSeparator())
		panel.add(self.panelSep)
		### 		
		# Settings controls
		##
		self.panelSettings = swing.JPanel()
		self.panelSettings.layout = awt.GridLayout(1,1)
		self.lblCurrent = swing.JLabel()
		self.panelSettings.add(self.lblCurrent)
		panel.add(self.panelSettings)
		
		self.frame.setContentPane(panel)
		self.frame.size = self.normal_size
		self.frame.resizable = False
		self.frame.show()
