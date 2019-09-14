# Tested with Python2 and Python3

import math
import os, sys, getopt
from PIL import Image, ImageFont, ImageDraw

from escapes import html
from uni_format import format_fragment, width_fragment
from uni_struct import Fragment, Horizontal, Vertical, Basic, Overlay, Sign
from uni_syntax import parser
from uni_dimensions import Dimensions

def create_image(out, font, size, hiero):
	data = html.unescape(hiero)
	fragment = parser.parse(data)
	if fragment:
		dim = Dimensions(font)
		format_fragment(fragment, dim)
		margin = 2
		WHITE = (255,255,255)
		im = Image.new('RGB', (int(round(width_fragment(fragment, dim) * size)) + margin * 2, \
				size + margin * 2), WHITE)
		draw_fragment(fragment, margin, margin, ImageDraw.Draw(im), font, size)
		im.save(out)
	else:
		print(hiero)
		sys.exit(2)

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

def usage():
	print('create_image [-f <infont>] [-s <fontsize>] -o <outfile> hieroglyphic')
	print('<infont>: .ttf file')
	print('<outfile>: .jpg/.png//.bmp/.tif file')
	print('hieroglyphic: Unicode string')
	sys.exit(2)

def main(argv):
	try:
		opts, args = getopt.getopt(argv, 'hf:s:o:', [])
	except getopt.GetoptError:
		usage()
	d = os.path.dirname(os.path.realpath(sys.argv[0]))
	f = d + '/fonts/NewGardinerSMP'
	s = 20
	out = None
	for opt, arg in opts:
		if opt == '-h':
			usage()
		elif opt == '-f':
			f = d + '/fonts/' + arg
		elif opt == '-s':
			s = int(arg)
		elif opt == '-o':
			out = arg
	if not out:
		usage()
	if len(args) != 1:
		usage()
	f = os.path.splitext(f)[0]
	create_image(out, f, s, args[0])

if __name__ == '__main__':
	main(sys.argv[1:])
