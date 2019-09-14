# Tested with Python2 and Python3

# For the syntax, see:
# https://www.unicode.org/L2/L2018/18236-nederhof.pdf

import ply.lex as lex
import ply.yacc as yacc

from uni_struct import Fragment, Horizontal, Vertical, Basic, Overlay, Sign

import re

tokens = (
	'SIGN',
	'VERT',
	'HOR',
	'ST',
	'SB',
	'ET',
	'EB',
	'OVERLAY',
	'BEGIN',
	'END',
)

t_SIGN	= u'[\U00013000-\U0001342e]'
t_VERT	= u'\U00013430'
t_HOR	= u'\U00013431'
t_ST	= u'\U00013432'
t_SB	= u'\U00013433'
t_ET	= u'\U00013434'
t_EB	= u'\U00013435'
t_OVERLAY	= u'\U00013436'
t_BEGIN	= u'\U00013437'
t_END	= u'\U00013438'

def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

lexer = lex.lex(reflags=re.UNICODE)

# fragment
def p_fragment(p):
	'fragment : groups'
	p[0] = Fragment(p[1])

# groups
def p_groups1(p):
	'groups : group'
	p[0] = [p[1]]
def p_groups2(p):
	'groups : group groups'
	p[0] = [p[1]] + p[2]

# group
def p_group1(p):
	'group : vertical_group'
	p[0] = p[1]
def p_group2(p):
	'group : horizontal_group'
	p[0] = p[1]
def p_group3(p):
	'group : basic_group'
	p[0] = p[1]
def p_group4(p):
	'group : sign'
	p[0] = Basic(p[1], None, None, None, None)

# vertical_group
def p_vertical_group(p):
	'vertical_group : vert_subgroup rest_vert_group'
	p[0] = Vertical([p[1]] + p[2])

# rest_vert_group
def p_rest_vert_group1(p):
	'rest_vert_group : VERT vert_subgroup rest_vert_group'
	p[0] = [p[2]] + p[3]
def p_rest_vert_group2(p):
	'rest_vert_group : VERT vert_subgroup'
	p[0] = [p[2]]
	
# br_vertical_group
def p_br_vertical_group(p):
	'br_vertical_group : BEGIN vert_subgroup rest_br_vert_group'
	p[0] = Vertical([p[2]] + p[3])

# rest_br_vert_group
def p_rest_br_vert_group1(p):
	'rest_br_vert_group : VERT vert_subgroup rest_br_vert_group'
	p[0] = [p[2]] + p[3]
def p_rest_br_vert_group2(p):
	'rest_br_vert_group : VERT vert_subgroup END'
	p[0] = [p[2]]
	
# br_flat_vertical_group
def p_br_flat_vertical_group(p):
	'br_flat_vertical_group : BEGIN sign rest_br_flat_vert_group'
	p[0] = [p[2]] + p[3]

# rest_br_flat_vert_group
def p_rest_br_flat_vert_group1(p):
	'rest_br_flat_vert_group : VERT sign rest_br_flat_vert_group'
	p[0] = [p[2]] + p[3]
def p_rest_br_flat_vert_group2(p):
	'rest_br_flat_vert_group : VERT sign END'
	p[0] = [p[2]]

# vert_subgroup
def p_vert_subgroup1(p):
	'vert_subgroup : horizontal_group'
	p[0] = p[1]
def p_vert_subgroup2(p):
	'vert_subgroup : basic_group'
	p[0] = p[1]
def p_vert_subgroup3(p):
	'vert_subgroup : sign'
	p[0] = Basic(p[1], None, None, None, None)

# horizontal_group
def p_horizontal_group1(p):
	'horizontal_group : hor_subgroup rest_hor_group'
	p[0] = Horizontal([p[1]] + p[2])
def p_horizontal_group2(p):
	'horizontal_group : sign rest_hor_group'
	p[0] = Horizontal([Basic(p[1], None, None, None, None)] + p[2])

# rest_hor_group
def p_rest_hor_group1(p):
	'rest_hor_group : HOR hor_subgroup rest_hor_group'
	p[0] = [p[2]] + p[3]
def p_rest_hor_group2(p):
	'rest_hor_group : HOR sign rest_hor_group'
	p[0] = [Basic(p[2], None, None, None, None)] + p[3]
def p_rest_hor_group3(p):
	'rest_hor_group : HOR hor_subgroup'
	p[0] = [p[2]]
def p_rest_hor_group4(p):
	'rest_hor_group : HOR sign'
	p[0] = [Basic(p[2], None, None, None, None)]

# br_horizontal_group
def p_br_horizontal_group1(p):
	'br_horizontal_group : BEGIN hor_subgroup rest_br_hor_group'
	p[0] = Horizontal([p[2]] + p[3])
def p_br_horizontal_group2(p):
	'br_horizontal_group : BEGIN sign rest_br_hor_group'
	p[0] = Horizontal([Basic(p[2], None, None, None, None)] + p[3])

# rest_br_hor_group
def p_rest_br_hor_group1(p):
	'rest_br_hor_group : HOR hor_subgroup rest_br_hor_group'
	p[0] = [p[2]] + p[3]
def p_rest_br_hor_group2(p):
	'rest_br_hor_group : HOR sign rest_br_hor_group'
	p[0] = [Basic(p[2], None, None, None, None)] + p[3]
def p_rest_br_hor_group3(p):
	'rest_br_hor_group : HOR hor_subgroup END'
	p[0] = [p[2]]
def p_rest_br_hor_group4(p):
	'rest_br_hor_group : HOR sign END'
	p[0] = [Basic(p[2], None, None, None, None)]

# br_flat_horizontal_group
def p_br_flat_horizontal_group(p):
	'br_flat_horizontal_group : BEGIN sign rest_br_flat_hor_group'
	p[0] = [p[2]] + p[3]

# rest_br_flat_hor_group
def p_rest_br_flat_hor_group1(p):
	'rest_br_flat_hor_group : HOR sign rest_br_flat_hor_group'
	p[0] = [p[2]] + p[3]
def p_rest_br_flat_hor_group2(p):
	'rest_br_flat_hor_group : HOR sign END'
	p[0] = [p[2]]

# hor_subgroup
def p_hor_subgroup1(p):
	'hor_subgroup : br_vertical_group'
	p[0] = p[1]
def p_hor_subgroup2(p):
	'hor_subgroup : basic_group'
	p[0] = p[1]

# basic_group
def p_basic_group1(p):
	'basic_group : core_group'
	p[0] = Basic(p[1], None, None, None, None)
def p_basic_group2(p):
	'basic_group : insertion_group'
	p[0] = p[1]

# insertion_group
def p_insertion_group1(p):
	'insertion_group : core_group insertion'
	p[0] = Basic(p[1], p[2][0], p[2][1], p[2][2], p[2][3])
def p_insertion_group2(p):
	'insertion_group : sign insertion'
	p[0] = Basic(p[1], p[2][0], p[2][1], p[2][2], p[2][3])

# br_insertion_group
def p_br_insertion_group1(p):
	'br_insertion_group : BEGIN core_group insertion END'
	p[0] = Basic(p[2], p[3][0], p[3][1], p[3][2], p[3][3])
def p_br_insertion_group2(p):
	'br_insertion_group : BEGIN sign insertion END'
	p[0] = Basic(p[2], p[3][0], p[3][1], p[3][2], p[3][3])

# insertion
def p_insertion1(p):
	'insertion : ST in_subgroup opt_sb_insertion opt_et_insertion opt_eb_insertion'
	p[0] = [p[2], p[3], p[4], p[5]]
def p_insertion2(p):
	'insertion : SB in_subgroup opt_et_insertion opt_eb_insertion'
	p[0] = [None, p[2], p[3], p[4]]
def p_insertion3(p):
	'insertion : ET in_subgroup opt_eb_insertion'
	p[0] = [None, None, p[2], p[3]]
def p_insertion4(p):
	'insertion : EB in_subgroup'
	p[0] = [None, None, None, p[2]]

# opt_sb_insertion
def p_opt_sb_insertion1(p):
	'opt_sb_insertion :'
	p[0] = None
def p_opt_sb_insertion2(p):
	'opt_sb_insertion : SB in_subgroup'
	p[0] = p[2]

# opt_et_insertion
def p_opt_et_insertion1(p):
	'opt_et_insertion :'
	p[0] = None
def p_opt_et_insertion2(p):
	'opt_et_insertion : ET in_subgroup'
	p[0] = p[2]

# opt_eb_insertion
def p_opt_eb_insertion1(p):
	'opt_eb_insertion :'
	p[0] = None
def p_opt_eb_insertion2(p):
	'opt_eb_insertion : EB in_subgroup'
	p[0] = p[2]

# in_subgroup
def p_in_subgroup1(p):
	'in_subgroup : br_vertical_group'
	p[0] = p[1]
def p_in_subgroup2(p):
	'in_subgroup : br_horizontal_group'
	p[0] = p[1]
def p_in_subgroup3(p):
	'in_subgroup : br_insertion_group'
	p[0] = p[1]
def p_in_subgroup4(p):
	'in_subgroup : core_group'
	p[0] = Basic(p[1], None, None, None, None)
def p_in_subgroup5(p):
	'in_subgroup : sign'
	p[0] = Basic(p[1], None, None, None, None)

# core_group
def p_core_group(p):
	'core_group : flat_horizontal_group OVERLAY flat_vertical_group'
	p[0] = Overlay(p[1], p[3])

# flat_horizontal_group
def p_flat_horizontal_group1(p):
	'flat_horizontal_group : br_flat_horizontal_group'
	p[0] = p[1]
def p_flat_horizontal_group2(p):
	'flat_horizontal_group : sign'
	p[0] = [p[1]]

# flat_vertical_group
def p_flat_vertical_group1(p):
	'flat_vertical_group : br_flat_vertical_group'
	p[0] = p[1]
def p_flat_vertical_group2(p):
	'flat_vertical_group : sign'
	p[0] = [p[1]]

# sign
def p_sign(p):
	'sign : SIGN'
	p[0] = Sign(p[1])

def p_error(p):
	print('Parsing error')

parser = yacc.yacc()
