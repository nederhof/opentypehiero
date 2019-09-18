# Tested with Python2 and Python3

from uni_struct import Fragment, Horizontal, Vertical, Basic, Overlay, Sign

def print_fragment(f):
	print('Fragment')
	indent = '\t'
	for g in f.groups:
		if isinstance(g, Vertical):
			print_vertical_group(g, indent)
		elif isinstance(g, Horizontal):
			print_horizontal_group(g, indent)
		elif isinstance(g, Basic):
			print_basic_group(g, indent)
		else:
			print('WRONG STRUCTURE of Fragment: ' + type(g).__name__)

def print_vertical_group(v, indent):
	print(indent + 'Vertical')
	indent += '\t'
	for g in v.groups:
		if isinstance(g, Horizontal):
			print_horizontal_group(g, indent)
		elif isinstance(g, Basic):
			print_basic_group(g, indent)
		else:
			print('WRONG STRUCTURE of Vertical: ' + type(g).__name__)

def print_horizontal_group(h, indent):
	print(indent + 'Horizontal')
	indent += '\t'
	for g in h.groups:
		if isinstance(g, Vertical):
			print_vertical_group(g, indent)
		elif isinstance(g, Basic):
			print_basic_group(g, indent)
		else:
			print('WRONG STRUCTURE of Horizontal: ' + type(g).__name__)

def print_basic_group(b, indent):
	print(indent + 'Basic')
	indent += '\t'
	if isinstance(b.core, Overlay):
		print_overlay(b.core, indent)
	elif isinstance(b.core, Sign):
		print_sign(b.core, indent)
	else:
		print('WRONG STRUCTURE of Basic: ' + type(b.core).__name__)
	if b.st:
		print_insert_group('ST', b.st, indent)
	if b.sb:
		print_insert_group('SB', b.sb, indent)
	if b.et:
		print_insert_group('ET', b.et, indent)
	if b.eb:
		print_insert_group('EB', b.eb, indent)

def print_insert_group(corner, g, indent):
	print(indent + corner)
	indent += '\t'
	if isinstance(g, Vertical):
		print_vertical_group(g, indent)
	elif isinstance(g, Horizontal):
		print_horizontal_group(g, indent)
	elif isinstance(g, Basic):
		print_basic_group(g, indent)
	else:
		print('WRONG STRUCTURE of insert: ' + type(g).__name__)
	
def print_overlay(g, indent):
	print(indent + 'Overlay')
	indent += '\t'
	print(indent + 'arg1')
	for g1 in g.g1:
		if isinstance(g1, Sign):
			print_sign(g1, indent + '\t')
		else:
			print('WRONG STRUCTURE of Overlay 1: ' + type(g1).__name__)
	print(indent + 'arg2')
	for g2 in g.g2:
		if isinstance(g2, Sign):
			print_sign(g2, indent + '\t')
		else:
			print('WRONG STRUCTURE of Overlay 2: ' + type(g2).__name__)

def print_sign(g, indent):
	print(indent + 'Sign')
