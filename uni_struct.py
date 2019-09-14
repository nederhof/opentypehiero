# Tested with Python2 and Python3

Vert	= u'\U00013430'
Hor	= u'\U00013431'
St	= u'\U00013432'
Sb	= u'\U00013433'
Et	= u'\U00013434'
Eb	= u'\U00013435'
Over	= u'\U00013436'
Begin	= u'\U00013437'
End	= u'\U00013438'

class Fragment:
	# g is list of Vertical/Horizontal/Basic
	def __init__(self, g):
		self.groups = g
	def signs(self):
		return [s for g in self.groups for s in g.signs()]
	def __repr__(self):
		return u'-'.join([repr(g) for g in self.groups])
	def __str__(self):
		return u''.join([str(g) for g in self.groups])
	def __unicode__(self):
		return u''.join([unicode(g) for g in self.groups])
	def to_string(self):
		try:
			return unicode(self)
		except NameError:
			return str(self)

class Vertical:
	# g is list of Horizontal/Basic
	def __init__(self, g):
		self.groups = g
	def signs(self):
		return [s for g in self.groups for s in g.signs()]
	def __repr__(self):
		return u'(' + u'*'.join([repr(g) for g in self.groups]) + u')'
	def __str__(self):
		return Vert.join([str(g) for g in self.groups])
	def __unicode__(self):
		return Vert.join([unicode(g) for g in self.groups])
	def to_string(self):
		try:
			return unicode(self)
		except NameError:
			return str(self)

class Horizontal:
	# g is list of Vertical/Basic
	def __init__(self, g):
		self.groups = g
	def signs(self):
		return [s for g in self.groups for s in g.signs()]
	def __repr__(self):
		return u'(' + u':'.join([repr(g) for g in self.groups]) + u')'
	def __str__(self):
		groups = []
		for g in self.groups:
			if isinstance(g, Vertical):
				groups.append(Begin + str(g) + End)
			else:
				groups.append(str(g))
		return Hor.join([g for g in groups])
	def __unicode__(self):
		groups = []
		for g in self.groups:
			if isinstance(g, Vertical):
				groups.append(Begin + unicode(g) + End)
			else:
				groups.append(unicode(g))
		return Hor.join([g for g in groups])
	def to_string(self):
		try:
			return unicode(self)
		except NameError:
			return str(self)

class Basic:
	# g is Overlay/Sign
	# st,sb,et,eb is Vertical/Horizontal/Basic/None
	def __init__(self, g, st, sb, et, eb):
		self.core = g
		self.st = st
		self.sb = sb
		self.et = et
		self.eb = eb
	def signs(self):
		return self.core.signs() + \
			(self.st.signs() if self.st else []) + \
			(self.sb.signs() if self.sb else []) + \
			(self.et.signs() if self.et else []) + \
			(self.eb.signs() if self.eb else [])
	def __repr__(self):
		return u'(' + repr(self.core) + u',' + \
			repr(self.st) + u',' + repr(self.sb) + u',' + \
			repr(self.et) + u',' + repr(self.eb) + u')'
	def __str__(self):
		s = str(self.core)
		if self.st:
			if isinstance(self.st, Basic) and self.st.is_core():
				g = str(self.st)
			else:
				g = Begin + str(self.st) + End
			s += St + g
		if self.sb:
			if isinstance(self.sb, Basic) and self.sb.is_core():
				g = str(self.sb)
			else:
				g = Begin + str(self.sb) + End
			s += Sb + g
		if self.et:
			if isinstance(self.et, Basic) and self.et.is_core():
				g = str(self.et)
			else:
				g = Begin + str(self.et) + End
			s += Et + g
		if self.eb:
			if isinstance(self.eb, Basic) and self.eb.is_core():
				g = str(self.eb)
			else:
				g = Begin + str(self.eb) + End
			s += Eb + g
		return s
	def __unicode__(self):
		s = unicode(self.core)
		if self.st:
			if isinstance(self.st, Basic) and self.st.is_core():
				g = unicode(self.st)
			else:
				g = Begin + unicode(self.st) + End
			s += St + g
		if self.sb:
			if isinstance(self.sb, Basic) and self.sb.is_core():
				g = unicode(self.sb)
			else:
				g = Begin + unicode(self.sb) + End
			s += Sb + g
		if self.et:
			if isinstance(self.et, Basic) and self.et.is_core():
				g = unicode(self.et)
			else:
				g = Begin + unicode(self.et) + End
			s += Et + g
		if self.eb:
			if isinstance(self.eb, Basic) and self.eb.is_core():
				g = unicode(self.eb)
			else:
				g = Begin + unicode(self.eb) + End
			s += Eb + g
		return s
	def to_string(self):
		try:
			return unicode(self)
		except NameError:
			return str(self)
	def is_core(self):
		return self.st == None and self.sb == None and \
				self.et == None and self.eb == None

class Overlay:
	# g1,g2 is list of Sign
	def __init__(self, g1, g2):
		self.group1 = g1
		self.group2 = g2
	def signs(self):
		return [s for g in self.group1 + self.group2 for s in g.signs()]
	def __repr__(self):
		return u'(' + repr(self.group1) + u',' + repr(self.group2) + u')'
	def __str__(self):
		if len(self.group1) == 1:
			arg1 = str(self.group1[0])
		else:
			arg1 = Begin + Hor.join([str(g) for g in self.group1]) + End
		if len(self.group2) == 1:
			arg2 = str(self.group2[0])
		else:
			arg2 = Begin + Vert.join([str(g) for g in self.group2]) + End
		return arg1 + Over + arg2
	def __unicode__(self):
		if len(self.group1) == 1:
			arg1 = unicode(self.group1[0])
		else:
			arg1 = Begin + Hor.join([unicode(g) for g in self.group1]) + End
		if len(self.group2) == 1:
			arg2 = unicode(self.group2[0])
		else:
			arg2 = Begin + Vert.join([unicode(g) for g in self.group2]) + End
		return arg1 + Over + arg2

class Sign:
	def __init__(self, c):
		self.char = c
		self.code = ord(c)
	def signs(self):
		return [self]
	def __repr__(self):
		return str(self.code)
	def __str__(self):
		return self.char
	def __unicode__(self):
		return self.char
