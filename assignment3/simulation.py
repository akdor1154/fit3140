#!/usr/bin/env python2

from random import randrange
from random import shuffle

import __future__

class WallError(Exception):
	#error for if the robot crashes into a wall
	def __init__(self, wall):
		self.wallHit = wall
	def __str__(self):
		return ("Hit wall: " + str(self.wallHit))


class MazeObject(object):
	def __init__(self, tile):
		self.tile = tile
	
class Goal(MazeObject):
	def __init__(self):
		pass   

class Robot(MazeObject):
	def __init__(self, tile, maze):
		super(self.__class__, self).__init__(tile=tile)#inherits from MazeObject
		self.orientation = 0 #0,1,2,3 = left,right,up,down
		
		self.maze = maze
		
	def move(self):
		if self.tile.edges[self.orientation] is not None:
			self.tile = self.tile.edges[self.orientation]
		else:
			raise WallError(self.orientation)
	
	#			  0	1	2   3
	#edge order: left right up down
	#turn right: left up right down
	#turn left: down right up left
	#def turnLeft(self):
	def turn(self, n):
		for _ in range(n):
			if self.orientaton == 0:
				self.orientation = 3
			elif self.orientation == 1:
				self.orientation = 2
			elif self.orientation == 2:
				self.orientation = 0
			elif self.orientation == 3:
				self.orientation = 1
	"""	
	def turnRight(self):
		if self.orientaton == 0:
			self.orientation = 2
		elif self.orientation == 1:
			self.orientation = 3
		elif self.orientation == 2:
			self.orientation = 1
		elif self.orientation == 3:
			self.orientation = 0
	"""		
	def detectWall(self):
		test = self.tile
		distance = 0
		while test.edges[self.orientation] is not None:#while there is not a wall, count 1 tile and move to the next tile
			distance +=1
			test = test.edges[self.orientation]
		return distance
			
	def detectGoal(self):
		X = [0, 0, 1, -1]
		Y = [-1, 1, 0, 0]
		
		#^^ the additions you need to make to the current index to move one space, using the direction as the index
		
		nextX = X[self.orientation]
		nextY = Y[self.orientation]
		
		distance = 0
		row = self.tile.row
		column = self.tile.column
		while self.maze[row][column] is not None:
			if self.maze[row][column].goal:
				break
			row += nextX
			column += nextY
		return distance
	
	@property
	def x(self):
		return self.tile.row
	
	@property
	def y(self):
		return self.tile.column

class Tile(object):
	def __init__(self, x, y):
		
		self.object = None
		
		self.column = x
		self.row = y
		
		self.connected = False
		
		self.edges = [None, None, None, None]#[left, right, up, down]
	
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
	
class Maze(object):
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
		
		self.generate()
		
	def generate(self):
		#[left, right, up, down]
		X = [0, 0, 1, -1]
		Y = [-1, 1, 0, 0]
		#^^ the additions you need to make to the current index to move along one edge, with that edge as the index
		randorder = [0, 1, 2, 3]
		nodes = [self.start]
		
		while len(nodes) > 0:
			
			current = nodes[-1]
			
			#randorder = order
			shuffle(randorder)#the order that the edges of the tile will be checked
			
			nextTile = None
			for side in randorder:
				nextRow = current.row + X[side]
				nextColumn = current.column + Y[side]
				#(X/Y)[side] will match up with the direction of side, giving the next tile
				if (nextRow >= 0 and nextRow < self.size and nextColumn >= 0 and nextColumn < self.size) and (not (self.maze[nextRow][nextColumn].connected)):#check if the tile on this side 1) exists, and 2) is not already part of the maze
					nextTile = self.maze[nextRow][nextColumn]
					
					#link the two tiles together
					current.edges[side] = nextTile
					if side % 2 == 0:
						nextTile.edges[side+1] = current
					else:
						nextTile.edges[side-1] = current
					break
				
			if not (nextTile is None):
				#flag the tile as connected, so that we don't loop back to it later, and add it to the stack(nodes)
				nextTile.connected = True
				nodes.append(nextTile)
			else:
				#this will only happen if there were no sides left in the tile to do anything with, so we can pop it off the stack
				nodes.pop()
				
	def displayText(self):
		#for testing purposes only
		#print maze with maze[0] at the top (backwards)
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