#!/usr/bin/env python2
import kivy.app
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
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

from fcodeui import *
from dragndrop import DragNDropWidget

import __future__

class FCodeWorkspace(FloatLayout):
	
			
	def buildTree(self, root):
		args = []
		args.append(root.fName.fName)
		for arg in root.fArgs:
			try:
				args.append(arg.name)
			except:
				args.append(self.buildTree(arg))
			
		return fBlock(*args)
				


class RobotView(Widget):
	def __init__(self, mazeView, **kwargs):
		super(self.__class__, self).__init__(**kwargs)
		self.mazeView = mazeView
		self.robot = mazeView.robot
		self.size = (40,40)
		self.robot.bind(kposition=self.updatePos)
		self.robot.bind(korientation=self.updateLine)
		with self.mazeView.canvas:
			Color(0.4,0.4,0.8)
			self.e = Ellipse(pos=self.pos, size=self.size)
			Color(0.9,0.9,0.9)
			self.l = Line(width=4)
		self.updatePos()
	
	def updatePos(self, instance=None, value=(0,0)):
		self.e.pos = V(self.mazeView.tileWidth, self.mazeView.tileHeight) * (
				(V(self.robot.x, self.robot.y)+V(0.5, 0.5))
		) - V(self.e.size)*V(0.5, 0.5)
		self.updateLine(instance, value)
		
	def updateLine(self, instance=None, value=None):
		ellipseCentre = V(self.e.pos)+V(self.e.size)*V(0.5,0.5)
		ellipseDirectionOffsets = [
			V(-self.e.size[0]/2, 0),
			V( self.e.size[0]/2, 0),
			V(0,  self.e.size[1]/2),
			V(0, -self.e.size[1]/2)
		]
		ellipseEnd = ellipseCentre+ellipseDirectionOffsets[self.robot.orientation]
		self.l.points = listOfPoints(ellipseCentre, ellipseEnd)
	
		

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
	
class Palette(GridLayout):

	def addFunction(self, name, nArguments):
		b = PaletteButton(name, nArguments, workspace=self.workspace)
		self.buttons.append(b)
		self.add_widget(b)
		
	def __init__(self, workspace, **kwargs):
		#self.workspace = workspace
		self.cols = 3
		self.workspace=workspace
		super(Palette, self).__init__(cols=self.cols, **kwargs)
		self.app = kivy.app.App.get_running_app()
		
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
			("greaterthan", 2),
			
			("if",3),
			("set",2)
		)
		
		list(starmap(self.addFunction, buttonDefinitions))
		
		
class PaletteButton(FName):
	def __init__(self, fName, nArguments, workspace, **kwargs):
		self.nArguments = nArguments
		self.workspace = workspace
		super(PaletteButton, self).__init__(fName=fName, **kwargs)
		
		
	def on_touch_down(self, touch):
		if not self.collide_point(touch.x, touch.y):
			return False
		self.makeFunction()
		
	def makeFunction(self):
		newFunction = FLayout(self.fName, nArguments=self.nArguments, rootLayout=self.workspace)
		self.get_root_window().add_widget(newFunction)
		newFunction._transient = True
		newFunction.touchRelative = (0,0)
		newFunction.dispatch("on_drag_start")
		
	
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
		
		self.workspaceLayout = BoxLayout(orientation="vertical", size_hint=(1, .9))#will contain a 'begin' button and label
		self.beginButton = Button(text="Begin", size_hint=(1, .1))#run the tree
		self.beginButton.bind(on_press=self.app.runProgram)
		self.workspace = FCodeWorkspace()#code is just being shown as text for now, will change in the next version
		self.workspaceLayout.add_widget(self.workspace)
		self.workspaceLayout.add_widget(self.beginButton)
		
		self.add_widget(Palette(workspace=self.workspace))
		self.add_widget(self.workspaceLayout)	
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
		tree = fTree(self.robotController.robotEnv)
		for fLayout in self.f.workspace.children:
			tree.addBlock(self.f.workspace.buildTree(fLayout))
		print tree.execute()

		

if __name__ == '__main__':
	FIT3140App().run()

