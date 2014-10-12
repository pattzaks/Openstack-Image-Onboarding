from error_map import *

class CliError(Exception): pass

class InvalidArgumentsException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class OperationError(Exception):
	def __init__(self, err):
		self.err=err
		self.errmsg=ErrorMap[err]
	def __str__ (self):
		return repr (self.errmsg)
