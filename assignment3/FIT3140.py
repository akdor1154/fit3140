#!/usr/bin/env python2
import kivy.app
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Line, Ellipse
from kivy.core.window import Window
import operator

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

class FIT3140Ui(BoxLayout):
	def __init__(self, maze, robotController, **kwargs):
		super(self.__class__,self).__init__(**kwargs)
		self.maze = maze
		self.robotController = robotController
		self.robot = self.robotController.robot
		
		self.fCodeWorkspace = FCodeWorkspace()
		self.mazeViewFloat = FloatLayout()
		self.mazeView = MazeView(self.maze, self.robot)
		
		self.mazeViewFloat.add_widget(self.mazeView)
		self.add_widget(self.fCodeWorkspace)
		self.add_widget(self.mazeViewFloat)

class FIT3140App(kivy.app.App):
	def build(self):
		self.maze = Maze(10)
		self.robot = Robot(self.maze.start, self.maze)
		self.robotController = RobotController(self.robot, self.maze)
		return FIT3140Ui(self.maze, self.robotController, size=Window.size)

		

if __name__ == '__main__':
	FIT3140App().run()

