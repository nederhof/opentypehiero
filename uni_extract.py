# Tested with Python2 and Python3

from escapes import html
from uni_syntax import parser
import re
import codecs

fragments = []

pattern = re.compile(u'[\U00013000-\U00013438]+')

def extract_fragments_files(fs):
	fragments = []
	for f in fs:
		fragments.extend(extract_fragments_file(f))
	return fragments

def extract_fragments_file(f):
	fragments = []
	try:
		with codecs.open(f, encoding='utf-8') as f:
			while True:
				line = f.readline()
				if not line:
					break
				line = html.unescape(line)
				fragments.extend(pattern.findall(line))
	except IOError:
		print('Cannot read file: ' + f)
	return fragments

def extract_groups(fs):
	fragments = extract_fragments_files(fs)
	groups = []
	for string in fragments:
		fragment = parser.parse(string)
		if fragment:
			groups.extend(fragment.groups)
		else:
			print(string)
	return groups

def bylength(w1, w2):
	return len(w2)-len(w1)

def extract_unique_group_strings(fs):
	groups = extract_groups(fs)
	str_to_group = {}
	for g in groups:
		str_to_group[g.to_string()] = g
	return sorted(str_to_group.keys(), key=len, reverse=True)
