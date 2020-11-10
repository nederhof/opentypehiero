# Tested with Python2 and Python3

# Glyphs for which insert in start-top should be 1/5 lower:
st_lower = {
# "A16","A29","A36"
int('0x13013', 0), int('0x13021', 0), int('0x13029', 0),
# "C4","F5"
int('0x13060', 0), int('0x13103', 0), 
# "G3","G6a","G7"
int('0x13141', 0), int('0x13145', 0), int('0x13146', 0),
# "G7a","G7b","G8"
int('0x13147', 0), int('0x13148', 0), int('0x13149', 0),
# "G16","G32","G40"
int('0x13152', 0), int('0x13164', 0), int('0x1316E', 0),
# "U1","U2"
int('0x13333', 0), int('0x13334', 0), 
}

# Glyphs for which insert in start-bottom should be 1/5 higher:
sb_raise = {
# "A17","A24","A25","A26"
int('0x13014', 0), int('0x1301C', 0), int('0x1301D', 0), int('0x1301E', 0),
# "A27","A28","A30","A33"
int('0x1301F', 0), int('0x13020', 0), int('0x13022', 0), int('0x13026', 0),
# "A59","A66","A68",
int('0x13044', 0), int('0x1304B', 0), int('0x1304D', 0),
# "D54a","D57","D59",
int('0x130BC', 0), int('0x130BF', 0), int('0x130C1', 0),
# "E1","E2","E3","E6"
int('0x130D2', 0), int('0x130D3', 0), int('0x130D4', 0), int('0x130D7', 0),
# "E7","E8","E10","E11" 
int('0x130D8', 0), int('0x130D9', 0), int('0x130DD', 0), int('0x130DE', 0),
# "E13","E14","E17",
int('0x130E0', 0), int('0x130E1', 0), int('0x130E5', 0),
# "E17a","E20","E22","E28"
int('0x130E6', 0), int('0x130E9', 0), int('0x130EC', 0), int('0x130F2', 0),
# "E29","E30","E31"
int('0x130F4', 0), int('0x130F5', 0), int('0x130F6', 0),
# "E32","E33","E38",
int('0x130F7', 0), int('0x130F8', 0), int('0x130FD', 0),
# "F8","F22","F26",
int('0x13106', 0), int('0x13116', 0), int('0x1311A', 0),
# "G1","G2","G4","G5"
int('0x1313F', 0), int('0x13140', 0), int('0x13142', 0), int('0x13143', 0),
# "G6","G9","G14","G15"
int('0x13144', 0), int('0x1314A', 0), int('0x13150', 0), int('0x13151', 0),
# "G17","G18","G19",
int('0x13153', 0), int('0x13154', 0), int('0x13155', 0),
# "G20","G20a","G21","G22"
int('0x13156', 0), int('0x13157', 0), int('0x13158', 0), int('0x13159', 0),
# "G23","G25","G26a"
int('0x1315A', 0), int('0x1315C', 0), int('0x1315E', 0),
# "G27","G28","G29",
int('0x1315F', 0), int('0x13160', 0), int('0x13161', 0),
# "G30","G31","G33","G34"
int('0x13162', 0), int('0x13163', 0), int('0x13165', 0), int('0x13166', 0),
# "G35","G36","G36a"
int('0x13167', 0), int('0x13168', 0), int('0x13169', 0),
# "G37","G37a","G38",
int('0x1316A', 0), int('0x1316B', 0), int('0x1316C', 0),
# "G39","G41","G42"
int('0x1316D', 0), int('0x1316F', 0), int('0x13170', 0),
# "G43","G44","G45","G45a",
int('0x13171', 0), int('0x13173', 0), int('0x13174', 0), int('0x13175', 0),
# "H2","I7","M3a","O35"
int('0x13180', 0), int('0x1318F', 0), int('0x131B2', 0), int('0x13284', 0),
# "T11a","T32","U13"
int('0x13316', 0), int('0x1332C', 0), int('0x13341', 0),
# "U17","V7b","W25"
int('0x13345', 0), int('0x13374', 0), int('0x133CE', 0),
}

# Glyphs for which insert should not extend the half-cirle.
st_shallow = {
}
sb_shallow = {
}
et_shallow = {
# "G43","G43a","G44"
int('0x13171', 0), int('0x13172', 0), int('0x13173', 0)
}
eb_shallow = {
}

suppress_margin = {
	int('0x13193', 0)
}

