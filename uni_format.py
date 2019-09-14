# Tested with Python2 and Python3

from uni_struct import Fragment, Horizontal, Vertical, Basic, Overlay, Sign
from uni_dimensions import Dimensions
from uni_signs import *

# EM distance between signs before scaling
SEP = 0.05
# margin added on left and right sides if there are insertions
MARGIN = 0.1

def format_fragment(fragment, dim):
	x = 0.0
	for g in fragment.groups:
		scale_top(g, None, 1.0, dim)
		format_top(g, x, x + width_top(g, dim), 0.0, 1.0, dim)
		x += width_top(g, dim) + SEP

def format_top_group(g, dim):
	scale_top(g, None, 1.0, dim)
	format_top(g, 0.0, width_top(g, dim), 0.0, 1.0, dim)

def format_top(g, x0, x1, y0, y1, dim):
	if isinstance(g, Vertical):
		format_vertical(g, x0, x1, y0, y1, dim)
	elif isinstance(g, Horizontal):
		format_horizontal(g, x0, x1, y0, y1, dim)
	elif isinstance(g, Basic):
		format_basic(g, x0, x1, y0, y1, dim)

def format_vertical(vert, x0, x1, y0, y1, dim):
	h_buf = ((y1-y0) - height_vertical(vert, dim)) / (len(vert.groups) - 1)
	y = y0
	for g in vert.groups:
		if isinstance(g, Horizontal):
			h = height_horizontal(g, dim)
			format_horizontal(g, x0, x1, y, y+h, dim)
		elif isinstance(g, Basic):
			h = height_basic(g, dim)
			format_basic(g, x0, x1, y, y+h, dim)
		y = y+h + vert.scale * SEP + h_buf

def format_horizontal(hor, x0, x1, y0, y1, dim):
	w_buf = ((x1-x0) - width_horizontal(hor, dim)) / (len(hor.groups) - 1)
	x = x0
	for g in hor.groups:
		if isinstance(g, Vertical):
			w = width_vertical(g, dim)
			format_vertical(g, x, x+w, y0, y1, dim)
		elif isinstance(g, Basic):
			w = width_basic(g, dim)
			format_basic(g, x, x+w, y0, y1, dim)
		x = x+w + hor.scale * SEP + w_buf

def format_basic(b, x0, x1, y0, y1, dim):
	w = width_basic(b, dim)
	h = height_basic(b, dim)
	w_buf = (x1-x0)-w
	h_buf = (y1-y0)-h
	x0 += w_buf/2
	y0 += h_buf/2
	x1 = x0 + w
	y1 = y0 + h
	if isinstance(b.core, Overlay):
		m1 = MARGIN * scale_from_basic(b) if b.st or b.sb else 0.0
		m2 = MARGIN * scale_from_basic(b) if b.et or b.eb else 0.0
		if b.st:
			format_top(b.st, x0, x0 + width_top(b.st, dim),
				y0, y0 + height_top(b.st, dim), dim)
		if b.sb:
			format_top(b.sb, x0, x0 + width_top(b.sb, dim),
				y1 - height_top(b.sb, dim), y1, dim)
		if b.et:
			format_top(b.et, x1, x1 - width_top(b.et, dim),
				y0, y0 + height_top(b.et, dim), dim)
		if b.eb:
			format_top(b.eb, x1, x1 - width_top(b.eb, dim),
				y1 - height_top(b.eb, dim), y1, dim)
		format_overlay(b.core, x0 + m1, x1 - m2, y0, y1, dim)
	elif isinstance(b.core, Sign):
		(st_x1, st_x2, st_y1, st_y2) = dim.code_st(b.core.code)
		(sb_x1, sb_x2, sb_y1, sb_y2) = dim.code_sb(b.core.code)
		(et_x1, et_x2, et_y1, et_y2) = dim.code_et(b.core.code)
		(eb_x1, eb_x2, eb_y1, eb_y2) = dim.code_eb(b.core.code)
		xmin = 0.0
		xmax = 1.0
		ymin = 0.0
		ymax = 1.0
		if b.st:
			xmin = min(xmin, st_x1)
			ymin = min(ymin, st_y1)
		if b.sb:
			xmin = min(xmin, sb_x1)
			ymax = max(ymax, sb_y2)
		if b.et:
			xmax = max(xmax, et_x2)
			ymin = min(ymin, et_y1)
		if b.eb:
			xmax = max(xmax, eb_x2)
			ymax = max(ymax, eb_y2)
		if b.st:
			x = x0 + (st_x1 - xmin) * width_sign(b.core, dim)
			y = y0 + (st_y1 - ymin) * height_sign(b.core, dim)
			if b.core.code in st_lower:
				y += ((st_y2 - st_y1) * height_sign(b.core, dim) - height_top(b.st, dim)) / 2
				format_top(b.st, x, x + width_top(b.st, dim), y, y + height_top(b.st, dim), dim)
			else:
				w_st = (st_x2 - st_x1) * width_sign(b.core, dim)
				h_st = (st_y2 - st_y1) * height_sign(b.core, dim)
				format_top(b.st, x, x + w_st, y, y + h_st, dim)
		if b.sb:
			x = x0 + (sb_x1 - xmin) * width_sign(b.core, dim)
			y = y0 + (sb_y2 - ymin) * height_sign(b.core, dim)
			if b.core.code in sb_raise:
				y -= ((sb_y2 - sb_y1) * height_sign(b.core, dim) - height_top(b.sb, dim)) / 2
				format_top(b.sb, x, x + width_top(b.sb, dim), y - height_top(b.sb, dim), y, dim)
			else:
				w_sb = (sb_x2 - sb_x1) * width_sign(b.core, dim)
				h_sb = (sb_y2 - sb_y1) * height_sign(b.core, dim)
				format_top(b.sb, x, x + w_sb, y - h_sb, y, dim)
		if b.et:
			x = x0 + (et_x2 - xmin) * width_sign(b.core, dim)
			y = y0 + (et_y1 - ymin) * height_sign(b.core, dim)
			w_et = (et_x2 - et_x1) * width_sign(b.core, dim)
			h_et = (et_y2 - et_y1) * height_sign(b.core, dim)
			# format_top(b.et, x - width_top(b.et, dim), x, y, y + height_top(b.et, dim), dim)
			format_top(b.et, x - w_et, x, y, y + h_et, dim)
		if b.eb:
			x = x0 + (eb_x2 - xmin) * width_sign(b.core, dim)
			y = y0 + (eb_y2 - ymin) * height_sign(b.core, dim)
			w_eb = (eb_x2 - eb_x1) * width_sign(b.core, dim)
			h_eb = (eb_y2 - eb_y1) * height_sign(b.core, dim)
			# format_top(b.eb, x - width_top(b.eb, dim), x, y - height_top(b.eb, dim), y, dim)
			format_top(b.eb, x - w_eb, x, y - h_eb, y, dim)
		format_sign(b.core, x0 - xmin * width_sign(b.core, dim), 
				x0 + (1-xmin) * width_sign(b.core, dim), 
				y0 - ymin * height_sign(b.core, dim),
				y0 + (1-ymin) * height_sign(b.core, dim), dim)

def format_overlay(o, x0, x1, y0, y1, dim):
	w_buf = (x1-x0) - sum([width_sign(g, dim) for g in o.group1])
	x = x0 + w_buf/2
	for g in o.group1:
		w = width_sign(g, dim)
		format_sign(g, x, x+w, y0, y1, dim)
		x = x+w
	h_buf = (y1-y0) - sum([height_sign(g, dim) for g in o.group2])
	y = y0 + h_buf/2
	for g in o.group2:
		h = height_sign(g, dim)
		format_sign(g, x0, x1, y, y+h, dim)
		y = y+h

def format_sign(g, x0, x1, y0, y1, dim):
	w_buf = (x1-x0)-width_sign(g, dim)
	h_buf = (y1-y0)-height_sign(g, dim)
	g.x = x0 + w_buf/2
	g.y = y0 + h_buf/2 - (1.0-dim.code_height(g.code)) * g.scale

def scale_top(g, w, h, dim):
	if isinstance(g, Vertical):
		scale_vertical(g, w, h, dim)
	elif isinstance(g, Horizontal):
		scale_horizontal(g, w, h, dim)
	elif isinstance(g, Basic):
		scale_basic(g, w, h, dim)

def scale_vertical(vert, w, h, dim):
	vert.scale = 1.0
	for g in vert.groups:
		if isinstance(g, Horizontal):
			scale_horizontal(g, 1.0, None, dim)
		elif isinstance(g, Basic):
			scale_basic(g, 1.0, None, dim)
	w1 = width_vertical(vert, dim)
	h1 = height_vertical(vert, dim)
	f = 1.0
	if w:
		f = min(f, w / w1)
	if h:
		f = min(f, h / h1)
	scale_down_vertical(vert, f)
	
def scale_horizontal(hor, w, h, dim):
	hor.scale = 1.0
	for g in hor.groups:
		if isinstance(g, Vertical):
			scale_vertical(g, None, 1.0, dim)
		elif isinstance(g, Basic):
			scale_basic(g, None, 1.0, dim)
	w1 = width_horizontal(hor, dim)
	h1 = height_horizontal(hor, dim)
	f = 1.0
	if w:
		f = min(f, w / w1)
	if h:
		f = min(f, h / h1)
	scale_down_horizontal(hor, f)

def scale_basic(b, w, h, dim):
	if isinstance(b.core, Overlay):
		scale_overlay(b.core, None, None, dim)
	elif isinstance(b.core, Sign):
		scale_sign(b.core, None, None, dim)
	w1 = width_basic(b, dim)
	h1 = height_basic(b, dim)
	if isinstance(b.core, Overlay):
		w_st = w_sb = w_et = w_eb = w1 / 4 
		h_st = h_sb = h_et = h_eb = h1 / 4 
	elif isinstance(b.core, Sign):
		(st_x1, st_x2, st_y1, st_y2) = dim.code_st(b.core.code)
		w_st = (st_x2 - st_x1) * width_sign(b.core, dim)
		h_st = (st_y2 - st_y1) * height_sign(b.core, dim)
		(sb_x1, sb_x2, sb_y1, sb_y2) = dim.code_sb(b.core.code)
		w_sb = (sb_x2 - sb_x1) * width_sign(b.core, dim)
		h_sb = (sb_y2 - sb_y1) * height_sign(b.core, dim)
		(et_x1, et_x2, et_y1, et_y2) = dim.code_et(b.core.code)
		w_et = (et_x2 - et_x1) * width_sign(b.core, dim)
		h_et = (et_y2 - et_y1) * height_sign(b.core, dim)
		(eb_x1, eb_x2, eb_y1, eb_y2) = dim.code_eb(b.core.code)
		w_eb = (eb_x2 - eb_x1) * width_sign(b.core, dim)
		h_eb = (eb_y2 - eb_y1) * height_sign(b.core, dim)
	if b.st:
		scale_top(b.st, w_st, h_st, dim)
	if b.sb:
		scale_top(b.sb, w_sb, h_sb, dim)
	if b.et:
		scale_top(b.et, w_et, h_et, dim)
	if b.eb:
		scale_top(b.eb, w_eb, h_eb, dim)
	f = 1.0
	if w:
		f = min(f, w / w1)
	if h:
		f = min(f, h / h1)
	scale_down_basic(b, f)

def scale_overlay(o, w, h, dim):
	for g in o.group1:
		scale_sign(g, None, None, dim)
	for g in o.group2:
		scale_sign(g, None, None, dim)
	w1 = width_overlay(o, dim)
	h1 = height_overlay(o, dim)
	f = 1.0
	if w:
		f = min(f, w / w1)
	if h:
		f = min(f, h / h1)
	scale_down_overlay(o, f)

def scale_sign(g, w, h, dim):
	g.scale = 1.0
	w1 = width_sign(g, dim)
	h1 = height_sign(g, dim)
	f = 1.0
	if w:
		f = min(f, w / w1)
	if h:
		f = min(f, h / h1)
	scale_down_sign(g, f)

def scale_down_top(g, f):
	if isinstance(g, Vertical):
		scale_down_vertical(g, f)
	elif isinstance(g, Horizontal):
		scale_down_horizontal(g, f)
	elif isinstance(g, Basic):
		scale_down_basic(g, f)

def scale_down_vertical(v, f):
	v.scale *= f
	for g in v.groups:
		if isinstance(g, Horizontal):
			scale_down_horizontal(g, f)
		elif isinstance(g, Basic):
			scale_down_basic(g, f)

def scale_down_horizontal(h, f):
	h.scale *= f
	for g in h.groups:
		if isinstance(g, Vertical):
			scale_down_vertical(g, f)
		elif isinstance(g, Basic):
			scale_down_basic(g, f)

def scale_down_basic(b, f):
	if isinstance(b.core, Overlay):
		scale_down_overlay(b.core, f)
	elif isinstance(b.core, Sign):
		scale_down_sign(b.core, f)
	if b.st:
		scale_down_top(b.st, f)
	if b.sb:
		scale_down_top(b.sb, f)
	if b.et:
		scale_down_top(b.et, f)
	if b.eb:
		scale_down_top(b.eb, f)

def scale_down_overlay(o, f):
	for g in o.group1:
		scale_down_sign(g, f)
	for g in o.group2:
		scale_down_sign(g, f)

def scale_down_sign(g, f):
	g.scale *= f

def scale_from_basic(b):
	if isinstance(b.core, Overlay):
		return scale_from_overlay(b.core)
	elif isinstance(b.core, Sign):
		return b.core.scale
	
def scale_from_overlay(o):
	return o.group1[0].scale

def width_fragment(fragment, dim):
	widths = [width_top(g, dim) for g in fragment.groups]
	return sum(widths) + max(0, len(widths)-1) * SEP

def width_top(g, dim):
	if isinstance(g, Vertical):
		return width_vertical(g, dim)
	elif isinstance(g, Horizontal):
		return width_horizontal(g, dim)
	elif isinstance(g, Basic):
		return width_basic(g, dim)
	
def width_vertical(v, dim):
	ws = []
	for g in v.groups:
		if isinstance(g, Horizontal):
			ws.append(width_horizontal(g, dim))
		elif isinstance(g, Basic):
			ws.append(width_basic(g, dim))
	return max(ws)

def width_horizontal(h, dim):
	ws = []
	for g in h.groups:
		if isinstance(g, Vertical):
			ws.append(width_vertical(g, dim))
		elif isinstance(g, Basic):
			ws.append(width_basic(g, dim))
	return sum(ws) + (len(h.groups)-1) * SEP * h.scale

def width_basic(b, dim):
	if isinstance(b.core, Overlay):
		m1 = MARGIN if b.st or b.sb else 0.0
		m2 = MARGIN if b.et or b.eb else 0.0
		return width_overlay(b.core, dim) + (m1 + m2) * scale_from_basic(b)
	elif isinstance(b.core, Sign):
		xmin = 0.0
		xmax = 1.0
		if b.st:
			(st_x1, _, _, _) = dim.code_st(b.core.code)
			xmin = min(xmin, st_x1)
		if b.sb:
			(sb_x1, _, _, _) = dim.code_sb(b.core.code)
			xmin = min(xmin, sb_x1)
		if b.et:
			(_, et_x2, _, _) = dim.code_et(b.core.code)
			xmax = max(xmax, et_x2)
		if b.eb:
			(_, eb_x2, _, _) = dim.code_eb(b.core.code)
			xmax = max(xmax, eb_x2)
		return (xmax - xmin) * width_sign(b.core, dim)
		
def width_overlay(o, dim):
	w1 = sum([width_sign(g, dim) for g in o.group1])
	w2 = max([width_sign(g, dim) for g in o.group2])
	return max(w1,w2)

def width_sign(g, dim):
	return g.scale * dim.code_width(g.code)
		
def height_top(g, dim):
	if isinstance(g, Vertical):
		return height_vertical(g, dim)
	elif isinstance(g, Horizontal):
		return height_horizontal(g, dim)
	elif isinstance(g, Basic):
		return height_basic(g, dim)
	
def height_vertical(v, dim):
	hs = []
	for g in v.groups:
		if isinstance(g, Horizontal):
			hs.append(height_horizontal(g, dim))
		elif isinstance(g, Basic):
			hs.append(height_basic(g, dim))
	return sum(hs) + (len(v.groups)-1) * SEP * v.scale

def height_horizontal(h, dim):
	hs = []
	for g in h.groups:
		if isinstance(g, Vertical):
			hs.append(height_vertical(g, dim))
		elif isinstance(g, Basic):
			hs.append(height_basic(g, dim))
	return max(hs)

def height_basic(b, dim):
	if isinstance(b.core, Overlay):
		return height_overlay(b.core, dim)
	elif isinstance(b.core, Sign):
		ymin = 0.0
		ymax = 1.0
		if b.st:
			(_, _, st_y1, _) = dim.code_st(b.core.code)
			ymin = min(ymin, st_y1)
		if b.sb:
			(_, _, sb_y1, _) = dim.code_sb(b.core.code)
			ymin = min(ymin, sb_y1)
		if b.et:
			(_, _, _, et_y2) = dim.code_et(b.core.code)
			ymax = max(ymax, et_y2)
		if b.eb:
			(_, _, _, eb_y2) = dim.code_eb(b.core.code)
			ymax = max(ymax, eb_y2)
		return (ymax - ymin) * height_sign(b.core, dim)

def height_overlay(o, dim):
	h1 = max([height_sign(g, dim) for g in o.group1])
	h2 = sum([height_sign(g, dim) for g in o.group2])
	return max(h1,h2)

def height_sign(g, dim):
	return g.scale * dim.code_height(g.code)
