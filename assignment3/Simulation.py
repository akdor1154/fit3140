#!/usr/bin/env python2

from random import randrange
from random import shuffle


class WallError(Exception):
    def __init__(self, wall):
        self.wallHit = wall
    def __str__(self):
        return ("Hit wall: " + str(self.wallHit))


class MazeObject():
    def __init__(self, tile):
        self.tile = tile
    
class Goal(MazeObject):
    def __init__(self):
        pass   

class Robot(MazeObject):
    def __init__(self, tile):
        super(self.__class__, self).__init__(tile=tile)
        self.orientation = 0 #0,1,2,3 = left,right,up,down
        
    def move(self):
        if self.tile.edges[self.orientation] is not None:
            self.tile = self.tile.edges[self.orientation]
        else:
            raise WallError(self.orientation)
    
    #              0    1    2   3
    #edge order: left right up down
    #turn right: left up right down
    #turn left: down right up left
    def turnLeft(self):
        if self.orientaton == 0:
            self.orientation = 3
        elif self.orientation == 1:
            self.orientation = 2
        elif self.orientation == 2:
            self.orientation = 0
        elif self.orientation == 3:
            self.orientation = 1
        
    def turnRight(self):
        if self.orientaton == 0:
            self.orientation = 2
        elif self.orientation == 1:
            self.orientation = 3
        elif self.orientation == 2:
            self.orientation = 1
        elif self.orientation == 3:
            self.orientation = 0
            
    def detectWall(self):
        test = self.tile
        distance = 0
        while test.edges[self.orientation] is not None:
            pass

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
        

if __name__ == '__main__':
    pass