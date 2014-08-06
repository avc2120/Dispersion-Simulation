LOG_PATH = "logs/"
BATTERY_THRESH = 6.2
_promptTime = 3
sim = True
FOV = 0.37175
SIZE = 1000
if True:
	import bot_sim as bot
	ROBOT_LIST_ALL = (
	(("Anders", 6665, "scribbler"), 
	("Boomer", 6666, "scribbler"),
	("Caprica", 6667, "scribbler"), 
	("Caval", 6668, "scribbler"),
	("Hera", 6669, "scribbler"), 
	("Leoben", 6670, "scribbler"),
	("Sharon", 6671, "scribbler"), 
	("Tigh", 6672, "scribbler"),
    ("Tory", 6673, "scribbler"), 
    ("Tyrol", 6674, "scribbler")
	),
	(("Delenn", 6680, "scribbler"), 
	("G'Kar", 6681, "scribbler"),
	("Ivanova", 6682, "scribbler"), 
	("Lennier", 6683, "scribbler"),
	("Marcus", 6684, "scribbler"), 
	("Mollari", 6685, "scribbler"),
	("Sheridan", 6686, "scribbler"), 
	("Vir", 6687, "scribbler"),
	)
	)

else:
    import bot
    ROBOT_LIST_ALL = (
    ("Anders",  '00:1E:19:01:06:60', "scribbler"), 
    ("Boomer",  '00:1E:19:01:05:E2', "scribbler"),
    ("Caprica", '00:1E:19:01:06:4C', "scribbler"), 
    ("Caval",   '00:1E:19:01:06:68', "scribbler"),
    ("Hera",    '00:1E:19:01:06:12', "scribbler"), 
    ("Leoben",  '00:1E:19:01:05:E8', "scribbler"),
    ("Sharon",  '00:1E:19:01:06:2B', "scribbler"), 
    ("Tigh",    '00:1E:19:01:05:6B', "scribbler"),
    ("Tory",    '00:1E:19:01:05:DD', "scribbler"), 
    ("Tyrol",   '00:1E:19:01:05:FB', "scribbler")
    )

