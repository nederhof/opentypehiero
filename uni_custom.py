# Only tested with Python2

import re
import codecs
import HTMLParser

parser = HTMLParser.HTMLParser()

def normalize(s):
	return parser.unescape(s)

def process_custom_file(custom_file):
	subs = []
	try:
		with codecs.open(custom_file, encoding='utf-8') as f:
			while True:
				line = f.readline()
				if not line:
					break
				mapping = re.split('\s+', line.strip())
				if len(mapping) != 2:
					print('Strange line in custom file:' + line)
					sys.exit(1)
				source_string = normalize(mapping[0])
				if len(source_string) <= 1:
					print('Source string in custom file should have length >= 2:' + line)
					sys.exit(1)
				target_string = normalize(mapping[1])
				subs.append((source_string, target_string))
	except IOError:
		print('Cannot read file: ' + custom_file)
	return subs

def extract_custom_groups(custom_file):
	if custom_file is None:
		return []
	else:
		return process_custom_file(custom_file)

