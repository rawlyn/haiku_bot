
import sqlite3


# open database
connection = sqlite3.connect("data.db")
cursor = connection.cursor()

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


def commit():
	"""
	convenience function
	"""
	connection.commit()
	
	
def close():
	"""
	convenience function
	"""
	connection.commit()
	connection.close()


def store_comment_haiku(comment_id, haiku):
	"""
	save detected comment haiku to the database, marked as unreplied
	"""
	
	sql = """
	INSERT INTO haiku (comment_id, comment_haiku, replied) VALUES (?,?,?);
	"""
	
	try:
		cursor.execute(sql, (comment_id, haiku, 0))
		print "[stored - new haiku]".format(comment_id)
	except sqlite3.IntegrityError, e:
		print "[not stored - already detected]".format(comment_id)
		

def get_unreplied_haikus():
	"""
	return a list of haikus that have not been replied to
	"""
	
	sql = """
	SELECT id, comment_id, comment_haiku, replied
	FROM haiku
	WHERE replied = 0;
	"""
	cursor.execute(sql)
	
	data = cursor.fetchall()
	
	return data



