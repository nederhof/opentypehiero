# Only tested with Python2

import fontforge
import psMat
import os, sys

from uni_syntax import parser
from uni_format import SEP, format_fragment, width_fragment, width_top
from uni_extract import extract_unique_group_strings
from uni_dimensions import Dimensions

# Holding temporary result of scaling and positioning, before
# copying to target.
SCRATCH = int('0xFFFFD', 0)

FIRST_COMPOSITE = int('0xF0000', 0)

FIRST_GLYPH = int('0x13000', 0)
LAST_GLYPH = int('0x1342e', 0)

CONTROLS = [int('0x13430', 0), int('0x13431', 0), int('0x13432', 0), int('0x13433', 0), \
	int('0x13434', 0), int('0x13435', 0), int('0x13436', 0), int('0x13437', 0), int('0x13438', 0)]

def make_font(old):
	d = os.path.dirname(os.path.realpath(sys.argv[0]))
	f = fontforge.open(d + '/fonts/empty.ttf')
	f.encoding = 'UnicodeFull'
	f.ascent = old.ascent
	f.descent = 0
	return f

def insert_sign(new, target, old, source, scale, x, y):
	em = old.ascent
	old.selection.select(source)
	old.copy()
	new.selection.select(SCRATCH)
	new.paste()

	glyph = new[SCRATCH]
	(_,_,w,h) = glyph.boundingBox()
	x_trans = x * em
	y_trans = (1 - y - scale) * em
	glyph.transform(psMat.scale(scale))
	glyph.transform(psMat.translate(x_trans, y_trans))

	new.selection.select(SCRATCH)
	new.copy()
	new.selection.select(target)
	new.pasteInto()

def insert_group(new, target, old, dim, string):
	em = old.ascent
	fragment = parser.parse(string)
	format_fragment(fragment, dim)
	for g in fragment.groups:
		for s in g.signs():
			insert_sign(new, target, old, s.code, s.scale, s.x, s.y)
	nglyph = new[target]
	nglyph.width = (width_fragment(fragment, dim) + SEP) * em
	nglyph.vwidth = (width_fragment(fragment, dim) + SEP) * em

def create_for_strings(new_name, old_name, strings, complement):
	old = fontforge.open(old_name + '.ttf')
	dim = Dimensions(old_name)
	new = make_font(old)
	i = FIRST_COMPOSITE
	subs = []
	closure = close(strings, complement)
	for s in closure:
		codepoints = [ord(sub) for sub in s]
		if len(codepoints) == 1:
			p = codepoints[0] 
			insert_group(new, p, old, dim, s)
		else:
			insert_group(new, i, old, dim, s)
			subs.append((s, i))
			i += 1
	for c in CONTROLS:
		name_char(new, old, c)
	new.generate(new_name + '.ttf')
	return subs

def safe_chr(i):
    try:
        return chr(i)
    except ValueError:
        return unichr(i)

def close(strings, complement):
	if complement:
		ps = range(FIRST_GLYPH, LAST_GLYPH+1)
	else:
		ps = set()
		for s in strings:
			for c in s:
				p = ord(c)
				if FIRST_GLYPH <= p and p <= LAST_GLYPH:
					ps.add(p)
	longer = []
	for s in strings:
		if (len(s) > 1):
			longer.append(s)
	cs = [safe_chr(p) for p in ps]
	cs.extend(longer)
	return cs

def name_char(new, old, i):
	old.selection.select(i)
	old.copy()
	new.selection.select(i)
	new.pasteInto()
	new[i].width = old[i].width
	new[i].vwidth = old[i].width

def create_source(s):
	nums = [ord(c) for c in s]
	return 'u{:05X}'.format(nums[0]) + " " + ' '.join(['u{:05X}'.format(i) for i in nums[1:]]) + ' '

def create_substitution(f, sub):
	(sources, target) = sub
	f.write('sub ' + create_source(sources) + 'by ' + 'u{:05X}'.format(target) + ';\n')

def create_features(new_name, subs):
	f = open(new_name + '.fea', 'w')
	subs_mult = [(s,t) for (s,t) in subs if len(s) > 1]
	ligatures = [t for (s,t) in subs if len(s) > 1]
	f.write('languagesystem DFLT dflt;\n')
	if len(subs_mult) > 0:
		f.write('feature liga {\n')
		f.write('\tscript DFLT;\n')
		f.write('\tlanguage dflt;\n')
		if len(subs_mult) > 0:
			f.write('lookup liga0 {\n')
			for sub in subs_mult:
				create_substitution(f, sub)
			f.write('} liga0;\n')
		f.write('} liga;\n')
	f.close()

def create_for_files(new_name, old_name, fs, complement):
	strings = extract_unique_group_strings(fs)
	subs = create_for_strings(new_name, old_name, strings, complement)
	create_features(new_name, subs)
