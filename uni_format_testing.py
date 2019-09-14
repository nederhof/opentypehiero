# Tested with Python2 and Python3

from PIL import Image, ImageFont, ImageDraw
import codecs

from escapes import html
from uni_syntax import parser
from uni_format import format_top_group, format_fragment, width_top, width_fragment
from uni_draw import draw_top, draw_fragment
from uni_dimensions import Dimensions

WHITE = (255,255,255)
font = 'fonts/NewGardinerSMP'
dim = Dimensions(font)
resolution = 100
margin = 2

f1 = codecs.open('tests/hieropage.html', encoding='utf-8')
m = 0
while True:
	line = f1.readline()
	if not line:
		break
	line = line.strip()
	data = html.unescape(line)
	fragment = parser.parse(data)
	if fragment:
		format_fragment(fragment, dim)
		margin = 2
		im = Image.new('RGB', (int(round(width_fragment(fragment, dim) * resolution)) + margin * 2, resolution + margin * 2), WHITE)
		draw_fragment(fragment, margin, margin, ImageDraw.Draw(im), font, resolution)
		im.save('testline' + str(m) + '.jpg')
		m += 1
	
top_groups = {}

f2 = codecs.open('tests/hierotestsuite.html', encoding='utf-8')
while True:
	line = f2.readline()
	if not line:
		break
	line = line.strip()
	data = html.unescape(line)
	fragment = parser.parse(data)
	if fragment:
		for g in fragment.groups:
			top_groups[g.to_string()] = g

def bylength(w1, w2):
	return len(w2)-len(w1)

strings = sorted(top_groups.keys(), key=len, reverse=True)

n = 0
# strings = [html.unescape("&#x13171;&#x13433;&#x133cf;")]
for g in strings:
	group = top_groups[g]
	format_top_group(group, dim)
	im = Image.new('RGB', (int(round(width_top(group, dim) * resolution)), resolution), WHITE)
	draw_top(group, 0, 0, ImageDraw.Draw(im), font, resolution)
	im.save('testgroup' + str(n) + '.jpg')
	n += 1
