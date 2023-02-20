# Tested with Python2 and Python3

try:
    # python 2
    # html.escape from HTMLParser
    from HTMLParser import HTMLParser
    html = HTMLParser()
except ImportError:
    # python 3
    # html.escape directly available
    import html
