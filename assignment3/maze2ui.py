#!/usr/bin/env python2

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Line, Ellipse
import operator
from maze2 import Maze
import __future__

def addVectors(v1, v2):
    return map(operator.add, v1, v2)


class MazeWidget(Widget):
    def __init__(self, mazeSize=20):
        self.maze = Maze(mazeSize)
        self.maze.generate()
        super(self.__class__, self).__init__()
        self.drawMaze()
        self.bind(pos=self.updateRect, size=self.updateRect)
    
    def drawMaze(self):
        tileWidth = self.width/self.maze.size
        tileHeight = self.height/self.maze.size
        with self.canvas:
            Color(1,1,1)
            Rectangle(pos=self.pos, size=self.size)
            for (i,row) in enumerate(self.maze.maze):
                for (j,tile) in enumerate(row):
                    tileTopLeft = addVectors(self.pos, (i*tileWidth, j*tileHeight))
                    tileTopRight = addVectors(tileTopLeft, (tileWidth, 0))
                    tileBottomLeft = addVectors(tileTopLeft, (0, tileHeight))
                    tileBottomRight = addVectors(tileTopLeft, (tileWidth, tileHeight))
                    tileCentre = addVectors(tileTopLeft, (tileWidth/2, tileHeight/2))
                    
                    Color(0,0,0)
                    if tile.left is not None:
                        Line(points=tileTopLeft+tileBottomLeft)
                    if tile.right is not None:
                        Line(points=tileTopRight+tileBottomRight)
                    if tile.up is not None:
                        Line(points=tileTopLeft+tileTopRight)
                    if tile.down is not None:
                        Line(points=tileBottomLeft+tileBottomRight)
                        
                    Color(1,0,0,0.2)
                    d=20
                    if tile.connected:
                        Ellipse(pos=addVectors(tileCentre,(-d/2,-d/2)), size=(d,d))
                    
    
    def updateRect(self, instance, value):
        self.drawMaze()

class MazeDisplayApp(App):
    def build(self):
        self.m = MazeWidget()
        return self.m

if __name__ == '__main__':
    MazeDisplayApp().run()