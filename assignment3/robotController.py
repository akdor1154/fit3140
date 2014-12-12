import fcode

class RobotController():
	def __init__(self, robot, maze):
		self.robot = robot
		self.maze = maze
		self.fCode = None
		self.robotEnv = fcode.build_global_env()
		self.robotEnv.update({
			'move':    lambda: Robot.move(self.robot),
			'turn':	   lambda x: self.turn(x),
			'detect-wall': lambda: Robot.move(self.robot),
			'detect-goal': self.detectGoal,
		})
		
	def run(self):
		fcode.eval(self.fCode)
	
	def detectGoal(self):
		self.robot.detectGoal(self.maze)
	
