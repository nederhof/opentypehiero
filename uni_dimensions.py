# Tested with Python2 and Python3

import json

class Dimensions:
	def __init__(self, font):
		with open(font + '.json') as f:
			self.shapes = json.load(f)

	def code_width(self, code):
		if self.shapes[str(code)]:
			return self.shapes[str(code)][0]
		else:
			print('Cannot find ' + code)
		
	def code_height(self, code):
		if self.shapes[str(code)]:
			return self.shapes[str(code)][1]
		else:
			print('Cannot find ' + code)

	def code_st(self, code):
		if self.shapes[str(code)]:
			square = self.shapes[str(code)][2]
			return tuple(square)
		else:
			print('Cannot find ' + code)
		
	def code_sb(self, code):
		if self.shapes[str(code)]:
			square = self.shapes[str(code)][3]
			return tuple(square)
		else:
			print('Cannot find ' + code)
		
	def code_et(self, code):
		if self.shapes[str(code)]:
			square = self.shapes[str(code)][4]
			return tuple(square)
		else:
			print('Cannot find ' + code)
		
	def code_eb(self, code):
		if self.shapes[str(code)]:
			square = self.shapes[str(code)][5]
			return tuple(square)
		else:
			print('Cannot find ' + code)
	
