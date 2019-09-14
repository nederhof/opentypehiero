# Tested with Python2 and Python3

try:
    # python 2
    from HTMLParser import HTMLParser
except ImportError:
    # python 3
    from html.parser import HTMLParser
html = HTMLParser()
