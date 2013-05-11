
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
	connection.row_factory = sqlite3.Row
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


def init():
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
	comment_url VARCHAR(250) NOT NULL UNIQUE,
	comment_haiku VARCHAR(150),
	replied INT
	);
	"""
	cursor.execute(sql)
	
	disconnect()


def store_comment_haiku(comment_url, haiku):
	"""
	save detected comment haiku to the database, marked as unreplied
	"""
	global cursor
	
	connect()
	
	sql = """
	INSERT INTO haiku (comment_url, comment_haiku, replied) VALUES (?,?,?);
	"""
	
	try:
		cursor.execute(sql, (comment_url, haiku, 0))
		print "[stored - new haiku]".format(comment_url)
	except sqlite3.IntegrityError, e:
		print "[not stored - already detected]".format(comment_url)
		
	disconnect()
		

def get_unreplied_haikus():
	"""
	return a list of haikus that have not been replied to
	"""
	global cursor
	
	connect()
	
	sql = """
	SELECT id, comment_url, comment_haiku, replied
	FROM haiku
	WHERE replied = 0;
	"""
	cursor.execute(sql)
	
	data = cursor.fetchall()
	
	disconnect()
	
	return data


def mark_as_replied(comment_url):
	"""
	mark comment_url as replied
	"""
	global cursor
	
	connect()
	
	sql = """
	UPDATE haiku
	SET replied = 1
	WHERE comment_url = ?;
	"""
	cursor.execute(sql, (comment_url,))
	
	disconnect()

