import fcode

class RobotController(object):
	def __init__(self, robot, maze):
		self.robot = robot
		self.robot.controller = self
		self.maze = maze
		self.fCode = None
		self.robotEnv = fcode.build_global_env()
		self.robotEnv.update({
			'move':    self.robot.move,
			'turn':	   lambda x: self.robot.turn(x),
			'detect-wall': self.robot.detectWall,
			'detect-goal': self.robot.detectGoal,
		})
		
	def run(self):
		fcode.eval(self.fCode)
	
	
