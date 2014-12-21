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
		#draw the robot onto the maze
		super(self.__class__, self).__init__(**kwargs)
		self.mazeView = mazeView
		self.robot = mazeView.robot
		self.robot.bind(kposition=self.updatePos)
		self.robot.bind(korientation=self.updateLine)
		self.ellipseSize = (40,40)
		self.normalColour = (0.4, 0.4, 0.8)
		self.errorColour = (0.8, 0.4, 0.4)
		self.lineColour = (0.9, 0.9, 0.9)
		self.colour = self.normalColour
		self.redraw()
	
	def updatePos(self, instance=None, value=(0,0)):
		#redraw the robot; for when it moves
		self.e.pos = V(self.mazeView.tileWidth, self.mazeView.tileHeight) * (
				(V(self.robot.x, self.robot.y)+V(0.5, 0.5))
		) - V(self.e.size)*V(0.5, 0.5)
		self.updateLine(instance, value)
		
	def updateLine(self, instance=None, value=None):
		#update the robots line (that shows its orientation)
		ellipseCentre = V(self.e.pos)+V(self.e.size)*V(0.5,0.5)
		ellipseDirectionOffsets = [
			V(-self.e.size[0]/2, 0),
			V( self.e.size[0]/2, 0),
			V(0,  self.e.size[1]/2),
			V(0, -self.e.size[1]/2)
		]
		ellipseEnd = ellipseCentre+ellipseDirectionOffsets[self.robot.orientation]
		self.l.points = listOfPoints(ellipseCentre, ellipseEnd)
	
	def redraw(self):
		self.size = self.ellipseSize
		self.mazeView.redraw()
		with self.mazeView.canvas:
			Color(*self.colour)
			self.e = Ellipse(pos=self.pos, size=self.size)
			Color(*self.lineColour)
			self.l = Line(width=4)
		self.updatePos()
	
	def changeColour(self, colour):
		self.colour = colour
		self.redraw()
		

class MazeView(Widget):
	class TileView(object):
		#draw one tile
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
		self.redraw()
		
		self.robotView = RobotView(mazeView=self)
		self.layout.add_widget(self.robotView)
		

	def updateLines(self):
		#for all of the tiles, if there is a wall on any of its sides, draw a line, otherwise don't
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
					
	def redraw(self):
		self.canvas.clear()
		with self.canvas:
			Color(1,1,1)
			self.background = Rectangle(pos=self.pos, size=self.size)
			
		self.tileLines = [[self.TileView(parent=self) for tile in row] for row in self.maze.tiles]
		self.updateLines()
	
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
		#add a function to the palette
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
		
class ErrorDialog(Button):
	def __init__(self, errorMessage, **kwargs):
		super(Button, self).__init__(**kwargs)
		self.errorMessage = errorMessage
		self.text = self.errorMessage
		self.size_hint = (0.9, 0.3)
		self.opacity = 0.6
		self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
	
	def on_press(self):
		app = kivy.app.App.get_running_app()
		app.f.mazeView.robotView.changeColour(app.f.mazeView.robotView.normalColour)
		self.parent.remove_widget(self)
		app.reset()
		
	
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
		self.workspace = FCodeWorkspace()
		self.workspaceLayout.add_widget(self.workspace)
		self.workspaceLayout.add_widget(self.beginButton)
		
		#add all the things to the main screen
		self.add_widget(Palette(workspace=self.workspace))#add the palette
		self.add_widget(self.workspaceLayout)#add the workspace	
		self.add_widget(self.mazeViewFloat)#add the maze
		

class FIT3140App(kivy.app.App):
	def build(self):
		self.maze = Maze(10)
		self.robot = Robot(self.maze.start, self.maze)
		self._robot_start = (self.robot.tile, self.robot.orientation)
		self.robotController = RobotController(self.robot, self.maze)
		#self.tree = fTree(self.robotController.robotEnv)#for now there will be only one tree (will change in next version)
		self.f = FIT3140Ui(self.maze, self.robotController, size=Window.size)
		return self.f
		
	def runProgram(self, button):
		#everything in the workspace gets added to a tree, and then executed
		tree = fTree(self.robotController.robotEnv)
		for fLayout in self.f.workspace.children:
			tree.addBlock(self.f.workspace.buildTree(fLayout))
		try:
			print tree.execute()
		except FIT3140Error as e:
			self.f.mazeView.robotView.changeColour(self.f.mazeView.robotView.errorColour)
			self.errorButton = ErrorDialog(e.message)
			self.f.mazeViewFloat.add_widget(self.errorButton)

	def reset(self):
		(self.robot.tile, self.robot.orientation) = self._robot_start
	
		

if __name__ == '__main__':
	FIT3140App().run()

