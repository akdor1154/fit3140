import kivy.app
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Line, Ellipse
import operator
from maze import Maze

import __future__

class FCodeWorkspace(Widget):
	pass


def addVectors(v1, v2):
	return map(operator.add, v1, v2)

class Robot(Widget):
	pass
	
	
class MazeView(Widget):
	def __init__(self, maze, robot, **kwargs):
		self.mazeSize = 10
		self.maze = maze
		self.robot = robot
		super(self.__class__, self).__init__(**kwargs)
		self.bind(pos=self.updateRect, size=self.updateRect)
	
	def drawMaze(self):
		tileWidth = self.width/self.maze.size
		tileHeight = self.height/self.maze.size
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
					if tile.connected:
						Ellipse(pos=addVectors(tileCentre,(-d/2,-d/2)), size=(d,d))
					
	
	def updateRect(self, instance, value):
		self.drawMaze()

class FIT3140Ui(Widget):
	def __init__(self, maze, robotController, **kwargs):
		super().__init__(**kwargs)
		self.maze = maze
		self.robotController = robotController
		self.robot = robotController.robot
		
		self.boxLayout = BoxLayout(
			pos=self.pos,
			size=root.size,
			padding=2,
			spacing=2
		)
		
		self.fCodeWorkspace = FCodeWorkspace()
		self.mazeViewFloat = FloatLayout()
		self.mazeView = MazeView(self.maze, self.robot)
		
		self.mazeViewFloat.add_widget(self.mazeView)
		
		self.boxLayout.add_widget(self.fCodeWorkspace)
		self.boxLayout.add_widget(self.mazeViewFloat)


class FIT3140App(kivy.app.App):
	def build(self):
		return FIT3140Ui()

		

if __name__ == '__main__':
	FIT3140App().run()

