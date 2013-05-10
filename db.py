
import sqlite3


connection = None
cursor = None


def connect():
	"""
	open and initialise database
	"""
	global connection, cursor
	
	# open database
	connection = sqlite3.connect("data.db")
	cursor = connection.cursor()


def disconnect():
	"""
	commit and close connection
	"""
	global connection, cursor
	
	connection.commit()
	connection.close()
	
	connection = None
	cursor = None


def init_db():
	"""
	initialises db
	"""
	global cursor
	
	connect()
	
	# create table if it doesn't exist
	sql = """
	CREATE TABLE IF NOT EXISTS haiku
	(
	id INTEGER PRIMARY KEY,
	comment_id VARCHAR(10) NOT NULL UNIQUE,
	comment_haiku VARCHAR(150),
	replied INT
	);
	"""
	cursor.execute(sql)
	
	disconnect()


def store_comment_haiku(comment_id, haiku):
	"""
	save detected comment haiku to the database, marked as unreplied
	"""
	global cursor
	
	connect()
	
	sql = """
	INSERT INTO haiku (comment_id, comment_haiku, replied) VALUES (?,?,?);
	"""
	
	try:
		cursor.execute(sql, (comment_id, haiku, 0))
		print "[stored - new haiku]".format(comment_id)
	except sqlite3.IntegrityError, e:
		print "[not stored - already detected]".format(comment_id)
		
	disconnect()
		

def get_unreplied_haikus():
	"""
	return a list of haikus that have not been replied to
	"""
	global cursor
	
	connect()
	
	sql = """
	SELECT id, comment_id, comment_haiku, replied
	FROM haiku
	WHERE replied = 0;
	"""
	cursor.execute(sql)
	
	data = cursor.fetchall()
	
	disconnect()
	
	return data



