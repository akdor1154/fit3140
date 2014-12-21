#!/usr/bin/env python2
import kivy.app
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Line, Ellipse
from kivy.core.window import Window
import operator

from itertools import starmap

from v import V, listOfPoints
from fcode import fTree, fBlock
from simulation import *
from robotController import RobotController

import __future__

class FCodeWorkspace(Widget):
	
	pass


class RobotView(Widget):
	def __init__(self, mazeView, **kwargs):
		super(self.__class__, self).__init__(**kwargs)
		self.mazeView = mazeView
		self.robot = mazeView.robot
		self.size = (10,10)
		self.robot.bind(kposition=self.updatePos)
		self.robot.bind(kposition=self.updateOrientation)
		with self.mazeView.canvas:
			Color(0,0,1)
			self.e = Ellipse(pos=self.pos, size=self.size)
		self.updatePos()
	
	def updatePos(self, instance=None, value=(0,0)):
		print("robot is at",self.robot.x,",",self.robot.y)
		print("position: ",self.e.pos, self.mazeView.pos)
		self.e.pos = V(self.mazeView.tileWidth, self.mazeView.tileHeight) * (
				(V(self.robot.x, self.robot.y)+V(0.5, 0.5))
		)
		print("position: ",self.e.pos,self.mazeView.pos)
	
	def updateOrientation(self, instance, value):
		pass
		

class MazeView(Widget):
	class TileView(object):
		lineWidth = 2.0
		lineColour = (0,0,0)
		def __init__(self, parent, leftLinePoints = [], rightLinePoints = [], upLinePoints = [], downLinePoints = []):
			with parent.canvas:
				Color(0,0,0)
				self.leftLine = Line(points=leftLinePoints, width=self.lineWidth)
				self.rightLine = Line(points=rightLinePoints, width=self.lineWidth)
				self.upLine = Line(points=upLinePoints, width=self.lineWidth)
				self.downLine = Line(points=downLinePoints, width=self.lineWidth)

	def __init__(self, maze, robot, layout, **kwargs):
		Widget.__init__(self, **kwargs)
		
		self.mazeSize = 10
		self.maze = maze
		self.robot = robot
		self.layout = layout
		
		self.bind(pos=self.updatePos, size=self.updateSize)
		
		#self.robotView.updatePos()
		
		with self.canvas:
			Color(1,1,1)
			self.background = Rectangle(pos=self.pos, size=self.size)
			
		self.robotView = RobotView(mazeView=self)
		self.layout.add_widget(self.robotView)
			
		self.tileLines = [[self.TileView(parent=self) for tile in row] for row in self.maze.tiles]
		self.updateLines()

	def updateLines(self):
		for (i,row) in enumerate(self.maze.tiles):
			for (j,tile) in enumerate(row):
				t = self.tileLines[i][j]
				tileBottomLeft = V(self.pos) + V(i*self.tileWidth, j*self.tileHeight)
				tileBottomRight = tileBottomLeft + V(self.tileWidth, 0)
				tileTopLeft = tileBottomLeft + V(0, self.tileHeight)
				tileTopRight = tileBottomLeft + V(self.tileWidth, self.tileHeight)
				tileCentre = tileBottomLeft + V(self.tileWidth/2, self.tileHeight/2)
				
				m = 5 #margin
				tileBottomLeft = tileBottomLeft + V(m, m)
				tileBottomRight = tileBottomRight + V(-m, m)
				tileTopLeft = tileTopLeft + V(m, -m)
				tileTopRight = tileTopRight + V(-m, -m)
				
				pointsList = (
						(listOfPoints(tileTopLeft,tileBottomLeft), tile.left, t.leftLine),
						(listOfPoints(tileTopRight,tileBottomRight), tile.right, t.rightLine),
						(listOfPoints(tileTopLeft,tileTopRight), tile.up, t.upLine),
						(listOfPoints(tileBottomLeft,tileBottomRight), tile.down, t.downLine)
				)
				
				for (pointsSet, direction, line) in pointsList:
					line.points = pointsSet if direction is None else []
		
	
	def updatePos(self, instance, value):
		self.background.pos = self.pos
		self.robotView.updatePos()
		self.updateLines()
	
	def updateSize(self, instance, value):
		self.background.size = self.size
		self.robotView.updatePos()
		self.updateLines()
		
	@property
	def tileWidth(self):
		return self.width/self.maze.size
	
	@property
	def tileHeight(self):
		return self.height/self.maze.size
	
class Palette(BoxLayout):

	def addFunction(self, name, nArguments):
		b = Button(text=name)
		b.nArguments = nArguments
		b.bind(on_press=self.app.addBlock)
		self.buttons.append(b)
		self.add_widget(b)
		
	def __init__(self, **kwargs):
	
		super(self.__class__, self).__init__(**kwargs)
		self.app = kivy.app.App.get_running_app()
		self.orientation="vertical"
		
		argumentSection = BoxLayout()
		
		self.app.arguments = [TextInput(),TextInput(),TextInput(),TextInput(),TextInput()]
		for a in self.app.arguments:
			argumentSection.add_widget(a)
		
		self.buttons = []
		
		buttonDefinitions = (
			("turn", 1),
			("move", 0),
			("detect-wall", 0),
			("detect-goal", 0),
			("add", 2),
			("subtract", 2),
			("multiply", 2),
			("divide", 2),
			("modulus", 2),
			("equals", 2),
			("lessthan", 2),
			("greaterthan", 2)
		)
		
		list(starmap(self.addFunction, buttonDefinitions))
		
		self.add_widget(argumentSection)
		

class FIT3140Ui(BoxLayout):
	def __init__(self, maze, robotController, **kwargs):
	
		super(self.__class__,self).__init__(**kwargs)
		self.app = kivy.app.App.get_running_app()
		
		self.maze = maze
		self.robotController = robotController
		self.robot = self.robotController.robot
		
		self.mazeViewFloat = RelativeLayout()
		self.mazeView = MazeView(self.maze, self.robot, self.mazeViewFloat)
		self.mazeViewFloat.add_widget(self.mazeView)
		
		self.workspace = BoxLayout(orientation="vertical", size_hint=(1, .9))#will contain a 'begin' button and label
		self.beginButton = Button(text="Begin", size_hint=(1, .1))#run the tree
		self.beginButton.bind(on_press=self.app.runProgram)
		self.code = Label()#code is just being shown as text for now, will change in the next version
		self.workspace.add_widget(self.code)
		self.workspace.add_widget(self.beginButton)
		
		self.add_widget(Palette())
		self.add_widget(self.workspace)	
		self.add_widget(self.mazeViewFloat)
		

class FIT3140App(kivy.app.App):
	def build(self):
		self.maze = Maze(10)
		self.robot = Robot(self.maze.start, self.maze)
		self.robotController = RobotController(self.robot, self.maze)
		self.tree = fTree(self.robotController.robotEnv)#for now there will be only one tree (will change in next version)
		self.f = FIT3140Ui(self.maze, self.robotController, size=Window.size)
		return self.f
		
	def runProgram(self, button):
		try:
			self.f.code.text = "result= \n" + str(self.tree.execute())
		except:
			self.tree.execute()
			
	def addBlock(self, button):
		a = fBlock(button.text, self.arguments[0].text, self.arguments[1].text, self.arguments[2].text, self.arguments[3].text, self.arguments[4].text)
		self.tree.addBlock(a)
		self.f.code.text += "\n" + str(a.code)

		

if __name__ == '__main__':
	FIT3140App().run()

