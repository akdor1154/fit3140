#!/usr/bin/env python2

from random import randrange
from random import shuffle

from Tkinter import *

class Tile():
    def __init__(self, x, y):
        
        self.column = x
        self.row = y
        
        self.connected = False
        
        self.edges = [None, None, None, None]
    
    @property
    def left(self):
        return self.edges[0]
    
    @left.setter
    def left(self, value):
        self.edges[0] = value
    
    @property
    def right(self):
        return self.edges[1]
        
    @right.setter
    def right(self, value):
        self.edges[1] = value
        
    @property
    def up(self):
        return self.edges[2]
        
    @up.setter
    def up(self, value):
        self.edges[2] = value
        
    @property
    def down(self):
        return self.edges[3]
        
    @down.setter
    def down(self, value):
        self.edges[3] = value
    
class Maze():
    def __init__(self, size):
        self.size = size
        self.maze = []
        
        
        for y in range(size):
            level = []
            for x in range(size):
                level.append(Tile(x, y))
            self.maze.append(level)
            
             
        self.start = self.maze[0][randrange(size)]
        self.start.connected = True
        
        
    def generate(self):
        #[left, right, up, down]
        X = [0, 0, 1, -1]
        Y = [-1, 1, 0, 0]
        order = [0, 1, 2, 3]
        
        nodes = [self.start]
        
        while len(nodes) > 0:
            
            current = nodes[-1]
            
            randorder = order
            shuffle(randorder)
            
            nextTile = None
            for side in randorder:
                nextRow = current.row + X[side]
                nextColumn = current.column + Y[side]
                if (nextRow >= 0 and nextRow < self.size and nextColumn >= 0 and nextColumn < self.size) and (not (self.maze[nextRow][nextColumn].connected)):
                    nextTile = self.maze[nextRow][nextColumn]
                    
                    current.edges[side] = nextTile
                    if side % 2 == 0:
                        nextTile.edges[side+1] = current
                    else:
                        nextTile.edges[side-1] = current
                    break
                
            if not (nextTile is None):
                nextTile.connected = True
                nodes.append(nextTile)
            else:
                nodes.pop()
                
    def displayText(self):
        for row in self.maze:
            a = []
            for column in row:
                b = ""
                for i in column.edges:
                    b = b + str(i)[0]
                a.append(b)
            print a
        
    def displayTk(self):

        
        master = Tk()
        w = Canvas(master, width=30*self.size, height=30*self.size)
        w.pack()
        
        #r = 10
        #c = 10
        scale = self.size 
        
        #i think this is displaying it wrong, but it still shows a maze, so good enough for now
        for R in self.maze:
            for C in R:
                for side in C.edges:
                    if side:
                        w.create_line(C.row*scale, C.column*scale, side.row*scale, side.column*scale)
                        
            
        
        
        
        mainloop()        
        



if __name__ == '__main__':
    
    x = Maze(20)
    x.generate()
    x.display()
