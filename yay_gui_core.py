# Copyright (c) 2009 John (Jack) Angers, jacktasia@gmail.com
# Licensed under the terms of the MIT License (see LICENSE.txt)

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
		
		self.frame = swing.JFrame('Yay Desktop 0.7')
		self.frame.windowClosing = self.handleShowHide
		self.frame.contentPane.layout = awt.GridLayout(4,2)
		panel = swing.JPanel()
		### 		
		# Menu Bar
		##
		menuBar = swing.JMenuBar()
		fileMenu = swing.JMenu("File")
		editMenu = swing.JMenu("Edit")
		self.countMenu = swing.JMenu("")

		menuItemPrune = swing.JMenuItem("Prune File",actionPerformed=self.callPrune)
		menuItemReload = swing.JMenuItem("Reload Image Folder",actionPerformed=self.callReload)
		menuItemChangeFolder = swing.JMenuItem("Image Folder",actionPerformed=self.callSetDir)
		menuItemSetSpeed = swing.JMenuItem("Slideshow Speed",actionPerformed=self.showSpeedDialog)
		menuHide = swing.JMenuItem("Hide",actionPerformed=self.handleShowHide)
		menuItemQuit = swing.JMenuItem("Exit",actionPerformed=self.goodbye)
		
		editMenu.add(menuItemChangeFolder)
		editMenu.add(menuItemSetSpeed)
		editMenu.addSeparator()
		editMenu.add(menuItemPrune)
		
		fileMenu.add(menuItemReload)
		fileMenu.addSeparator()
		fileMenu.add(menuHide)
		fileMenu.add(menuItemQuit)
		
		menuBar.add(fileMenu)
		menuBar.add(editMenu)
		menuBar.add(self.countMenu)
		self.frame.setJMenuBar(menuBar)
		### 		
		# Top Panel
		##
		self.panelTop = swing.JPanel()
		self.panelTop.layout = awt.GridLayout(1,2)
		self.lblDirectory = swing.JLabel()
		self.panelTop.add(self.lblDirectory)
		self.lblStatus = swing.JTextField("?",3,keyPressed=self.callGoEnter)
		self.panelTop.add(self.lblStatus)
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
