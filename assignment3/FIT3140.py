#!/usr/bin/env python2
import kivy.app
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
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
	def __init__(self, mazeView, pos=(0,0), **kwargs):
		super(self.__class__, self).__init__(**kwargs)
		self.mazeView = mazeView
		self.robot = mazeView.robot
		self.size = (10,10)
		#self.bind(pos=self.updatePos)
		self.updatePos()
		self.draw()
	
	def updatePos(self):
		self.pos = (self.robot.x * self.mazeView.tileWidth, self.robot.y * self.mazeView.tileHeight)
		#self.draw()
		
	def draw(self):
		with self.mazeView.canvas:
			Color(0,0,1)
			Ellipse(pos=self.pos, size=self.size)

class MazeView(Widget):
	def __init__(self, maze, robot, **kwargs):
		self.mazeSize = 10
		self.maze = maze
		self.robot = robot
		self.tileWidth =  0
		self.tileHeight = 0
		super(self.__class__, self).__init__(**kwargs)
		self.bind(pos=self.updateRect, size=self.updateRect)
		self.robotView = RobotView(self)
	
	def drawMaze(self):
		tileWidth = self.width/self.maze.size
		tileHeight = self.height/self.maze.size
		self.tileWidth = tileWidth # need to keep track of these, but the following code will be very verbose if
		self.tileHeight = tileHeight # we need to have self. everywhere!
		with self.canvas:
			Color(1,1,1)
			Rectangle(pos=self.pos, size=self.size)
			for (j,row) in enumerate(self.maze.maze):
				for (i,tile) in enumerate(row):
					tileBottomLeft = addVectors(self.pos, (i*tileWidth, j*tileHeight))
					tileBottomRight = addVectors(tileBottomLeft, (tileWidth, 0))
					tileTopLeft = addVectors(tileBottomLeft, (0, tileHeight))
					tileTopRight = addVectors(tileBottomLeft, (tileWidth, tileHeight))
					tileCentre = addVectors(tileBottomLeft, (tileWidth/2, tileHeight/2))
					
					m = 5
					tileBottomLeft = addVectors(tileBottomLeft, (m, m))
					tileBottomRight = addVectors(tileBottomRight, (-m, m))
					tileTopLeft = addVectors(tileTopLeft, (m, -m))
					tileTopRight = addVectors(tileTopRight, (-m, -m))
					
					Color(0,0,0)
					lineWidth = 2.0
					if tile.left is None:
						Line(points=tileTopLeft+tileBottomLeft,width=lineWidth)
					if tile.right is None:
						Line(points=tileTopRight+tileBottomRight,width=lineWidth)
					if tile.up is None:
						Line(points=tileTopLeft+tileTopRight,width=lineWidth)
					if tile.down is None:
						Line(points=tileBottomLeft+tileBottomRight,width=lineWidth)
						
					Color(1,0,0,0.2)
					d=20
		self.robotView.draw()

	
	def updateRect(self, instance, value):
		self.drawMaze()
		
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
		self.maze = maze
		self.robotController = robotController
		self.robot = self.robotController.robot
		self.app = kivy.app.App.get_running_app()
		self.fCodeWorkspace = FCodeWorkspace()
		#self.mazeViewFloat = FloatLayout()
		self.mazeView = MazeView(self.maze, self.robot)
		
		#self.mazeViewFloat.add_widget(self.mazeView)
		#self.add_widget(self.fCodeWorkspace)
		
		
		self.workspace = BoxLayout(orientation="vertical", size_hint=(1, .9))#will contain a 'begin' button and label
		self.beginButton = Button(text="Begin", size_hint=(1, .1))#run the tree
		
		self.beginButton.bind(on_press=self.app.runProgram)
		
		self.code = Label()#code is just being shown as text for now, will change in the next version
		self.workspace.add_widget(self.code)
		self.workspace.add_widget(self.beginButton)
		
		self.add_widget(Palette())
		self.add_widget(self.workspace)	
		self.add_widget(self.mazeView)
		

class FIT3140App(kivy.app.App):
	def build(self):
		self.maze = Maze(10)
		self.robot = Robot(self.maze.start, self.maze)
		self.robotController = RobotController(self.robot, self.maze)
		
		self.tree = fTree()#for now there will be only one tree (will change in next version)
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

