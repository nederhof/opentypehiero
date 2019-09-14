# Only tested with Python3

# For debugging purposes.
# Typical use:
# if (code == 78643):
#	debug_im(im1, center, r)
def debug_im(im, center, r):
	draw = ImageDraw.Draw(im)
	print(center, r, center-r)
	draw.ellipse((-r,center-r,r,center+r), fill='blue', outline ='blue')
	im.save('test.jpg')

