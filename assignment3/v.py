import operator

class V(object):
	def __init__(self, *values):
		if (len(values) == 1):
			self._v = list(*values)
		else:
			self._v = list(values)
	
	def __len__(self):
		return len(self._v)
	
	def __check__(self, other):
		if len(other) != len(self._v):
			raise ValueError("vectors are of differing length")
	
	def __add__(self, other):
		self.__check__(other)
		return map(operator.add, self._v, other)
		
	def __sub__(self, other):
		self.__check__(other)
		return map(operator.sub, self._v, other)
		
	def __mul__(self, other):
		self.__check__(other)
		return map(operator.mul, self._v, other)
		
	def __repr__(self):
		return repr(self._v)

	def __str__(self):
		return str(self._v)
		
	def __iter__(self):
		return iter(self._v)
		