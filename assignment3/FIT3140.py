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


from fcode import fTree, fBlock
from simulation import *
from robotController import RobotController

import __future__

class FCodeWorkspace(Widget):
	
	pass


def addVectors(v1, v2):
	return map(operator.add, v1, v2)


class RobotView(Widget):
	def __init__(self, mazeView, **kwargs):
		super(self.__class__, self).__init__(**kwargs)
		self.mazeView = mazeView
		self.robot = mazeView.robot
		self.size = (1000,1000)
		self.robot.bind(kposition=self.updatePos)
		self.robot.bind(kposition=self.updateOrientation)
		with self.mazeView.canvas:
			Color(0,0,1)
			self.e = Ellipse(pos=self.pos, size=self.size)
	
	def updatePos(self, instance=None, value=(0,0)):
		print("robot is at",self.robot.x,",",self.robot.y)
		self.e.pos = addVectors(
			self.pos, addVectors(
				(0.5*self.mazeView.tileWidth, 0.5*self.mazeView.tileHeight),
				(self.robot.x * self.mazeView.tileWidth, self.robot.y * self.mazeView.tileHeight)
			)
		)
		print(" and just moved to",self.robot.x,",",self.robot.y)
	
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
		
		self.robotView = RobotView(mazeView=self)
		self.layout.add_widget(self.robotView)
		#self.robotView.updatePos()
		
		with self.canvas:
			Color(1,1,1)
			self.background = Rectangle(pos=self.pos, size=self.size)
			
		self.tileLines = [[self.TileView(parent=self) for tile in row] for row in self.maze.maze]
		self.updateLines()

	def updateLines(self):
		for (j,row) in enumerate(self.maze.maze):
			for (i,tile) in enumerate(row):
				t = self.tileLines[i][j]
				tileBottomLeft = addVectors(self.pos, (i*self.tileWidth, j*self.tileHeight))
				tileBottomRight = addVectors(tileBottomLeft, (self.tileWidth, 0))
				tileTopLeft = addVectors(tileBottomLeft, (0, self.tileHeight))
				tileTopRight = addVectors(tileBottomLeft, (self.tileWidth, self.tileHeight))
				tileCentre = addVectors(tileBottomLeft, (self.tileWidth/2, self.tileHeight/2))
				
				m = 5 #margin
				tileBottomLeft = addVectors(tileBottomLeft, (m, m))
				tileBottomRight = addVectors(tileBottomRight, (-m, m))
				tileTopLeft = addVectors(tileTopLeft, (m, -m))
				tileTopRight = addVectors(tileTopRight, (-m, -m))
				
				pointsList = (
						(tileTopLeft+tileBottomLeft, tile.left, t.leftLine),
						(tileTopRight+tileBottomRight, tile.right, t.rightLine),
						(tileTopLeft+tileTopRight, tile.up, t.upLine),
						(tileBottomLeft+tileBottomRight, tile.down, t.downLine)
				)
				
				for (pointsSet, direction, line) in pointsList:
					line.points = pointsSet if direction is None else []
		
	
	def updatePos(self, instance, value):
		self.background.pos = self.pos
		self.updateLines()
	
	def updateSize(self, instance, value):
		self.background.size = self.size
		self.updateLines()
		
	@property
	def tileWidth(self):
		return self.width/self.maze.size
	
	@property
	def tileHeight(self):
		return self.height/self.maze.size
		
class Palette(BoxLayout):
	def __init__(self, **kwargs):
	
		super(self.__class__, self).__init__(**kwargs)
		self.app = kivy.app.App.get_running_app()
		self.orientation="vertical"
		
		argumentSection = BoxLayout()
		
		self.app.arguments = [TextInput(),TextInput(),TextInput(),TextInput(),TextInput()]
		for a in self.app.arguments:
			argumentSection.add_widget(a)
			
				
		self.turnButton = Button(text="turn")
		self.moveButton = Button(text="move")
		self.detectWallButton = Button(text="detect-wall")
		self.detectGoalButton = Button(text="detect-goal")
		self.addButton = Button(text="add")
		self.subButton = Button(text="subtract")
		self.multButton = Button(text="multiply")
		self.divButton = Button(text="divide")
		self.modButton = Button(text="modulus")
		self.equButton = Button(text="equals")
		self.lessButton = Button(text="lessthan")
		self.greatButton = Button(text="greaterthan")
		#self.defButton = Button(text="Define")
		
		
		self.turnButton.bind(on_press=self.app.addBlock)
		self.moveButton.bind(on_press=self.app.addBlock)
		self.detectWallButton.bind(on_press=self.app.addBlock)
		self.detectGoalButton.bind(on_press=self.app.addBlock)
		self.addButton.bind(on_press=self.app.addBlock)
		self.subButton.bind(on_press=self.app.addBlock)
		self.multButton.bind(on_press=self.app.addBlock)
		self.divButton.bind(on_press=self.app.addBlock)
		self.modButton.bind(on_press=self.app.addBlock)
		self.equButton.bind(on_press=self.app.addBlock)
		self.lessButton.bind(on_press=self.app.addBlock)
		self.greatButton.bind(on_press=self.app.addBlock)
		#self.defButton.bind(on_press=self.app.addBlock)
		
		
		
		self.add_widget(argumentSection)
		
		self.add_widget(self.turnButton)
		self.add_widget(self.moveButton)
		self.add_widget(self.detectWallButton)
		self.add_widget(self.detectGoalButton)
		self.add_widget(self.addButton)
		self.add_widget(self.subButton)
		self.add_widget(self.multButton)
		self.add_widget(self.divButton)
		self.add_widget(self.modButton)
		self.add_widget(self.equButton)
		self.add_widget(self.lessButton)
		self.add_widget(self.greatButton)
		#self.x.add_widget(self.defButton)

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

