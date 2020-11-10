# Only tested with Python3

from fontTools.ttLib import TTFont
from PIL import Image, ImageFont, ImageDraw
import json
import math

from uni_format import MARGIN
from uni_signs import *

resolution = 100
first_glyph = int('0x13000', 0)
last_glyph = int('0x1342e', 0)
WHITE = (255,255,255)

def make_fonts(f):
	global font, Ifont, cmap
	font = TTFont(f + '.ttf')
	Ifont = ImageFont.truetype(f + '.ttf', resolution)
	cmap = font['cmap']

def image_width(im):
	for x in range(2*resolution-1, 0, -1):
		for y in range(2*resolution):
			if im.getpixel((x,y)) != WHITE:
				return (x+1)
def image_height(im):
	for y in range(2*resolution):
		for x in range(2*resolution):
			if im.getpixel((x,y)) != WHITE:
				return (2*resolution-(y+1))

def image_st_hit(im, x_center, y_center, w, h, r):
	for x in range(r):
		y = math.sqrt(r*r - x*x)
		if im.getpixel((x_center + x, y_center + y)) != WHITE:
			return True
	return False
def image_st(im, x_center, y_center, w, h):
	m = min(w-x_center, 2*resolution-y_center)
	for r in range(m):
		if image_st_hit(im, x_center, y_center, w, h, r):
			return r
	return m
def image_sb_hit(im, x_center, y_center, w, h, r):
	for x in range(r):
		y = math.sqrt(r*r - x*x)
		if im.getpixel((x_center + x, y_center - y)) != WHITE:
			return True
	return False
def image_sb(im, x_center, y_center, w, h):
	m = min(w-x_center, y_center-(2*resolution-1-h))
	for r in range(m):
		if image_sb_hit(im, x_center, y_center, w, h, r):
			return r
	return m
def image_et_hit(im, x_center, y_center, w, h, r):
	for x in range(r):
		y = math.sqrt(r*r - x*x)
		if im.getpixel((x_center - x, y_center + y)) != WHITE:
			return True
	return False
def image_et(im, x_center, y_center, w, h):
	m = min(x_center+1, 2*resolution-y_center)
	for r in range(min(w,h)):
		if image_et_hit(im, x_center, y_center, w, h, r):
			return r
	return m
def image_eb_hit(im, x_center, y_center, w, h, r):
	for x in range(r):
		y = math.sqrt(r*r - x*x)
		if im.getpixel((x_center - x, y_center - y)) != WHITE:
			return True
	return False
def image_eb(im, x_center, y_center, w, h):
	m = min(x_center+1, y_center-(2*resolution-1-h))
	for r in range(min(w,h)):
		if image_eb_hit(im, x_center, y_center, w, h, r):
			return r
	return m

def image_s(im, y_center, w, h):
	r_high = image_sb(im, 0, y_center-1, w, h)
	r_low = image_st(im, 0, y_center-1, w, h)
	r_high = image_sb(im, 0, y_center+1, w, h)
	r_low = image_st(im, 0, y_center+1, w, h)
	r_high = image_sb(im, 0, y_center, w, h)
	r_low = image_st(im, 0, y_center, w, h)
	r = min(r_high, r_low)
	if y_center-2 >= 2*resolution-h:
		r_high = image_sb(im, 0, y_center-2, w, h)
		r_low = image_st(im, 0, y_center-2, w, h)
		if min(r_high, r_low) > r:
			while True:
				y_center = y_center - 2
				r = min(r_high, r_low)
				r_high = image_sb(im, 0, y_center-1, w, h)
				r_low = image_st(im, 0, y_center-1, w, h)
				if min(r_high, r_low) <= r:
					return (y_center, r)
	if y_center+2 <= 2*resolution-1:
		r_high = image_sb(im, 0, y_center+2, w, h)
		r_low = image_st(im, 0, y_center+2, w, h)
		if min(r_high, r_low) > r:
			while True:
				y_center = y_center + 2
				r = min(r_high, r_low)
				r_high = image_sb(im, 0, y_center+1, w, h)
				r_low = image_st(im, 0, y_center+1, w, h)
				if min(r_high, r_low) <= r:
					break;
	return (y_center, r)
		
def image_e(im, y_center, w, h):
	r_high = image_eb(im, w-1, y_center, w, h)
	r_low = image_et(im, w-1, y_center, w, h)
	r = min(r_high, r_low)
	if y_center > 2*resolution-h:
		r_high = image_eb(im, w-1, y_center-1, w, h)
		r_low = image_et(im, w-1, y_center-1, w, h)
		if min(r_high, r_low) > r:
			while True:
				y_center = y_center - 1
				r = min(r_high, r_low)
				r_high = image_eb(im, w-1, y_center-1, w, h)
				r_low = image_et(im, w-1, y_center-1, w, h)
				if min(r_high, r_low) <= r:
					break;
	if y_center < 2*resolution-1:
		r_high = image_eb(im, w-1, y_center+1, w, h)
		r_low = image_et(im, w-1, y_center+1, w, h)
		if min(r_high, r_low) > r:
			while True:
				y_center = y_center + 1
				r = min(r_high, r_low)
				r_high = image_eb(im, w-1, y_center+1, w, h)
				r_low = image_et(im, w-1, y_center+1, w, h)
				if min(r_high, r_low) <= r:
					break;
	return (y_center, r)

def glyph_image_plain(code):
	im = Image.new('RGB', (2*resolution,2*resolution), WHITE)
	draw = ImageDraw.Draw(im)
	draw.text((0,resolution), chr(code), font=Ifont, fill='black')
	return im
def glyph_image_margin(code):
	im = Image.new('RGB', (2*round(MARGIN*resolution)+2*resolution,2*resolution), WHITE)
	draw = ImageDraw.Draw(im)
	draw.text((round(MARGIN*resolution),resolution), chr(code), font=Ifont, fill='black')
	return im
def glyph_shapes(code):
	im0 = glyph_image_plain(code)
	if code in suppress_margin:
		im1 = im0
		margin = 0
	else:
		im1 = glyph_image_margin(code)
		margin = round(MARGIN*resolution)
	w0 = image_width(im0)
	h = image_height(im0)
	w1 = w0 + 2*margin
	if code in st_lower:
		center, r = image_s(im1, 2*resolution - round(0.8*h), w1, h)
		r_st = adjust_radius_st(r, code)
		st = [-margin/w0, (r_st-margin)/w0, ((center-r_st) - (2*resolution-h))/h, \
				((center+r_st) - (2*resolution-h))/h]
	else:
		r = image_st(im1, 0, 2*resolution-h, w1, h)
		r_st = adjust_radius_st(r, code)
		st = [-margin/w0, (r_st-margin)/w0, 0, r_st/h]
	if code in sb_raise:
		center, r = image_s(im1, 2*resolution-1 - round(0.2*h), w1, h)
		r_sb = adjust_radius_sb(r, code)
		sb = [-margin/w0, (r_sb-margin)/w0, ((center-r_sb) - (2*resolution-h))/h, \
				((center+r_sb) - (2*resolution-h))/h]
	else:
		r = image_sb(im1, 0, 2*resolution-1, w1, h)
		r_sb = adjust_radius_sb(r, code)
		sb = [-margin/w0, (r_sb-margin)/w0, (h-r_sb)/h, 1]
	r = image_et(im1, w1-1, 2*resolution-h, w1, h)
	r_et = adjust_radius_et(r, code)
	et = [(w0+margin-r_et)/w0, (w0+margin)/w0, 0, r_et/h]
	r = image_eb(im1, w1-1, 2*resolution-1, w1, h)
	r_eb = adjust_radius_eb(r, code)
	eb = [(w0+margin-r_eb)/w0, (w0+margin)/w0, (h-r_eb)/h, 1]
	return [w0/resolution, h/resolution, \
		truncate(st), truncate(sb), truncate(et), truncate(eb)]

def adjust_radius_st(r, code):
	if code in st_shallow or r > 0.6 * resolution:
		return r - 0.1 * resolution
	elif r > 0.2 * resolution:
		return r - 0.05 * resolution
	else:
		return r
def adjust_radius_sb(r, code):
	if code in sb_shallow or r > 0.6 * resolution:
		return r - 0.1 * resolution
	elif r > 0.2 * resolution:
		return r - 0.05 * resolution
	else:
		return r
def adjust_radius_et(r, code):
	if code in et_shallow or r > 0.6 * resolution:
		return r - 0.1 * resolution
	elif r > 0.2 * resolution:
		return r - 0.05 * resolution
	else:
		return r
def adjust_radius_eb(r, code):
	if code in eb_shallow or r > 0.6 * resolution:
		return r - 0.1 * resolution
	elif r > 0.2 * resolution:
		return r - 0.05 * resolution
	else:
		return r

def truncate(l):
	return [round(v * 10000) / 10000 for v in l]
	
def analyse(f):
	sizes = {}

	for table in cmap.tables:
		for glyph in table.cmap.keys():
			if first_glyph <= glyph and glyph <= last_glyph and glyph not in sizes:
				sizes[glyph] = glyph_shapes(glyph)

	shape_file = f + '.json'
	try:
		f = open(shape_file, 'w')
		json.dump(sizes, f)
	except FileNotFoundError:
		print(shape_file + ' not found')
