
import praw
import user

import haiku
import sqlite3
import db


# create an agent
agent = praw.Reddit(user_agent=user.agent)
agent.login(user.name, user.password)

# read comments
comments = agent.get_subreddit("test").get_comments(limit=None)

# search for haikus
detected = {}

for comment in comments:
	comment_dict = dict(vars(comment))
	
	comment_body = comment_dict["body"]
	comment_id = comment_dict["id"]
	
	comment_haiku = haiku.get_haiku(comment_body)
	if comment_haiku != "":
		print "id: {0}".format(comment_id)
		print comment_haiku
		print "-" * 17
		detected["{0}".format(comment_id)] = comment_haiku

# open database
db = sqlite3.connect("data.db")
cursor = db.cursor()

# don't uncomment this unless you have to. duh.
#cursor.execute("DROP TABLE haiku")

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

# store detected haikus
for comment_id, comment_haiku in detected.iteritems():
	sql = """
INSERT INTO haiku (comment_id, comment_haiku, replied) VALUES (?,?,?);
	"""
	
	try:
		cursor.execute(sql, (comment_id, comment_haiku, 0))
		print "comment '{0}' stored".format(comment_id)
	except sqlite3.IntegrityError, e:
		print "comment '{0}' not stored - already detected".format(comment_id)

db.commit()

# get list of comments that need replying to
sql = """
SELECT id, comment_id, comment_haiku, replied
FROM haiku
WHERE replied = 0;
"""
cursor.execute(sql)

data = cursor.fetchall()
print data

# close db
db.commit()
db.close()

