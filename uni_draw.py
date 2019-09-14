# Tested with Python2 and Python3

import math
from PIL import ImageFont

from uni_struct import Fragment, Horizontal, Vertical, Basic, Overlay, Sign

def scaled_font(f, resolution, scale):
	return ImageFont.truetype(f + '.ttf', int(math.floor(scale * resolution)))

def draw_fragment(fragment, x, y, im, f, resolution):
	for g in fragment.groups:
		draw_top(g, x, y, im, f, resolution)

def draw_top(g, x, y, im, f, resolution):
	if isinstance(g, Vertical):
		draw_vertical(g, x, y, im, f, resolution)
	elif isinstance(g, Horizontal):
		draw_horizontal(g, x, y, im, f, resolution)
	elif isinstance(g, Basic):
		draw_basic(g, x, y, im, f, resolution)

def draw_vertical(vert, x, y, im, f, resolution):
	for g in vert.groups:
		if isinstance(g, Horizontal):
			draw_horizontal(g, x, y, im, f, resolution)
		elif isinstance(g, Basic):
			draw_basic(g, x, y, im, f, resolution)

def draw_horizontal(hor, x, y, im, f, resolution):
	for g in hor.groups:
		if isinstance(g, Vertical):
			draw_vertical(g, x, y, im, f, resolution)
		elif isinstance(g, Basic):
			draw_basic(g, x, y, im, f, resolution)

def draw_basic(b, x, y, im, f, resolution):
	if isinstance(b.core, Overlay):
		draw_overlay(b.core, x, y, im, f, resolution)
	elif isinstance(b.core, Sign):
		draw_sign(b.core, x, y, im, f, resolution)
	if b.st:
		draw_top(b.st, x, y, im, f, resolution)
	if b.sb:
		draw_top(b.sb, x, y, im, f, resolution)
	if b.et:
		draw_top(b.et, x, y, im, f, resolution)
	if b.eb:
		draw_top(b.eb, x, y, im, f, resolution)

def draw_overlay(o, x, y, im, f, resolution):
	for g in o.group1:
		draw_sign(g, x, y, im, f, resolution)
	for g in o.group2:
		draw_sign(g, x, y, im, f, resolution)

def draw_sign(g, x, y, im, f, resolution):
	x1 = x + g.x * resolution
	y1 = y + g.y * resolution
	font = scaled_font(f, resolution, g.scale)
	im.text((x1, y1), safe_chr(g.code), font=font, fill='black')

def safe_chr(i):
	try:
		return chr(i)
	except ValueError:
		return unichr(i)
