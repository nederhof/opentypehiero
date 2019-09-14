# Only tested with Python2

import fontforge
import psMat
import os, sys, getopt

from uni_syntax import parser
from uni_format import SEP, format_fragment, width_fragment, width_top
from uni_extract import extract_unique_group_strings
from uni_dimensions import Dimensions

# Holding temporary result of scaling and positioning, before
# copying to target.
SCRATCH = int('0xF0001', 0)

FIRST = int('0xF0000', 0)

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

def create_for_strings(new_name, old_name, strings):
	old = fontforge.open(old_name + '.ttf')
	dim = Dimensions(old_name)
	new = make_font(old)
	i = FIRST
	subs = []
	for s in strings:
		insert_group(new, i, old, dim, s)
		glyph = new[i]
		subs.append((s, i))
		i += 1
	name_sources(new, old, subs)
	for c in CONTROLS:
		name_char(new, old, c)
	new.generate(new_name + '.ttf')
	return subs

def name_sources(new, old, subs):
	sources = set([ord(source) for (sources, _) in subs for source in sources])
	for source in sources:
		name_char(new, old, source)

def name_char(new, old, i):
	old.selection.select(i)
	old.copy()
	new.selection.select(i)
	new.pasteInto()

def create_source(s):
	nums = [ord(c) for c in s]
	return 'u{:05X}'.format(nums[0]) + " " + ''.join(['u{:05X} '.format(i) for i in nums[1:]])

def create_substitution(f, sub):
	(sources, target) = sub
	f.write('sub ' + create_source(sources) + 'by ' + 'u{:05X}'.format(target) + ';\n')

def create_features(new_name, subs):
	f = open(new_name + '.fea', 'w')
	subs0 = [(s,t) for (s,t) in subs if len(s) > 1]
	subs1 = [(s,t) for (s,t) in subs if len(s) == 1]
	f.write('languagesystem DFLT dflt;\n')
	if len(subs0) + len(subs1) > 0:
		f.write('feature liga {\n')
		if len(subs0) > 0:
			f.write('lookup liga0 {\n')
			for sub in subs0:
				create_substitution(f, sub)
			f.write('} liga0;\n')
		if len(subs1) > 0:
			f.write('lookup liga1 {\n')
			for sub in subs1:
				create_substitution(f, sub)
			f.write('} liga1;\n')
		f.write('} liga;\n')
	f.close()

def create_for_files(new_name, old_name, fs):
	strings = extract_unique_group_strings(fs)
	subs = create_for_strings(new_name, old_name, strings)
	create_features(new_name, subs)

def usage():
	print('create_font [-f <infont>] -o <outfont> <infiles>')
	print('<infont>: .ttf file')
	print('<outfont>: .otf file')
	print('<infiles>: .txt or .html files')
	sys.exit(2)

def main(argv):
	try:
		opts, args = getopt.getopt(argv, 'hf:o:', [])
	except getopt.GetoptError:
		usage()
	d = os.path.dirname(os.path.realpath(sys.argv[0]))
	f = d + '/fonts/NewGardinerSMP'
	out = None
	for opt, arg in opts:
		if opt == '-h':
			usage()
		elif opt == '-f':
			f = d + '/fonts/' + arg
		elif opt == '-o':
			out = arg
	if not out:
		usage()
	f = os.path.splitext(f)[0] 
	out = os.path.splitext(out)[0] 
	create_for_files(out, f, args)
	os.system('makeotf -f ' + out + '.ttf -ff ' + out + '.fea -o ' + out + '.otf')

if __name__ == '__main__':
	main(sys.argv[1:])
