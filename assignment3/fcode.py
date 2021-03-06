#!/usr/bin/env python2

# Almost all of the Lispy code has been taken unashamedly from Peter Norvig
# at http://norvig.com/lispy.html. 

import __future__

from error import FIT3140Error

class LispyError(FIT3140Error):
	pass
	
class LispyNameError(NameError, LispyError):
	pass
	
class LispySyntaxError(SyntaxError, LispyError):
	pass

class fBlock():
	#represents a code block (eg. (add x y)  )

	def __init__(self, *args):
		self.function = args[0]
		self.args = args[1:]
		
		self.codeStr = "("
		for arg in args:
			self.codeStr += str(arg)
			self.codeStr += " "
		self.codeStr = self.codeStr[:-1] + ")" #cut off the last extra space and add a closed bracket to the end

		self.code = parse(self.codeStr)
		
		#self.code is the parsed code
		#self.codeStr is the code as text, eg. (add (add 1 1) (subtract 2 1)) 
		

		
class fTree(object):
	#a 'tree' of code; a function
	def __init__(self, env):
		self.blocks = []
		self.env = env
		
	def addBlock(self, block):
		self.blocks.append(block)
		
	def execute(self):
		for block in self.blocks:
			if block == self.blocks[-1]:
				self.blocks = [] #reset the tree
				return eval(block.code, self.env)#the last line of code is what gets returned
			print eval(block.code, self.env)




def tokenize(lispyString):
	"Read a lispy statement into a list of tokens"
	return lispyString.replace('(',' ( ').replace(')', ' ) ').split()
	
def parse(lispyString):
	return buildTree(tokenize(lispyString))

def buildTree(tokens):
	if len(tokens) == 0:
		raise LispySyntaxError('buildTree called on an empty list')
	token = tokens.pop(0)
	if token == '(':
		branch = []
		while tokens[0] != ')':
			branch.append(buildTree(tokens))
		tokens.pop(0) # drop the end )
		return branch
	elif token == ')':
		raise LispySyntaxError('got a ) without a (')
	else:
		return atom(token)

Symbol = str		  # A Scheme Symbol is implemented as a Python str
List   = list		 # A Scheme List is implemented as a Python list
Number = (int, float) # A Scheme Number is implemented as a Python int or float
Env	= dict		 #

def atom(token):
	"read a non-bracket into an atom"
	try: return int(token)
	except ValueError:
		try: return float(token)
		except ValueError:
			return Symbol(token)
			
			

class Procedure(object):
	def __init__(self, parameters, body, env):
		self.parameters, self.body, self.env = parameters, body, env
	def __call__(self, *args):
		return eval(self.body, Env(self.parameters, args, self.env))

class Env(dict):
	def __init__(self, parameters=(), args=(), parent=None):
		self.update(zip(parameters, args))
		self.parent = parent
	#the given code raises a silly exception, this works better because it lets our UI handle it
	#instead of the user's console crashing when they make a typo.
	def find(self, var):
		if (var in self):
			return self
		elif self.parent is not None:
			return self.parent.find(var)
		else:
			raise LispyNameError(var+' is not defined in the current Lispy environment')
		

def build_global_env():
	import operator as op
	env = Env()
	env.update({
		'add':op.add, 'subtract':op.sub, 'multiply':op.mul, 'divide':op.div, 
		'lessthan':op.gt, 'greaterthan':op.lt, 'equals':op.eq, 'modulus':op.mod,
		'comment': lambda x: None,
		'begin':   lambda *x: x[-1],
	})
	return env

global_env = build_global_env()

def eval(tree, env=global_env):
	"evaluate some Lispy in a given environment"
	if isinstance(tree, Symbol):
		return env.find(tree)[tree]
	elif not isinstance(tree, List):
		return tree
	elif tree[0] == 'if':
		(_, test, consequence, alternative) = tree
		exp = (consequence if eval(test, env) else alternative)
		return eval(exp, env)
	elif tree[0] == 'set':
		(_, var, exp) = tree
		env[var] = eval(exp, env)
	elif tree[0] == 'define':
		(_, parameters, body) = tree
		return Procedure(parameters, body, env)
	else:
		head = eval(tree[0], env)
		args = [eval(arg, env) for arg in tree[1:]]
		return head(*args)

def repl(prompt='> '):
	while True:
		val = eval(parse(raw_input(prompt)))
		if val is not None:
			print(treeToString(val))

def treeToString(tree):
	if isinstance(tree, list):
		return '(' + ' '.join(map(treeToString,tree))+')'
	else:
		return str(tree)

"""
testing

x = fBlock("add" ,2,3)
y = fBlock("subtract" ,2,1)
w = fBlock("add", x.codeStr, y.codeStr)
z = fTree()
z.addBlock(x)
z.addBlock(y)
z.addBlock(w)
z.execute()
"""
