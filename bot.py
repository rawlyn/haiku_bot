
import praw
import user # not in repo, used to store reddit user agent details

import haiku
import sqlite3
import db


print "fetching reddit comments..."

# create an agent
agent = praw.Reddit(user_agent=user.agent)
agent.login(user.name, user.password)

# read comments
comments = agent.get_subreddit(user.subreddits).get_comments(limit=None)

# search for haikus
print "looking for haikus..."

for comment in comments:
	comment_dict = dict(vars(comment))
	
	comment_body = comment_dict["body"]
	comment_id = comment_dict["id"]
	
	comment_haiku = haiku.get_haiku(comment_body)
	if comment_haiku != "":
		print "-" * 17
		
		print "id: {0}".format(comment_id)
		print comment_haiku
		
		# store haiku to database
		db.store_comment_haiku(comment_id, comment_haiku)
		
		print "-" * 17

db.commit()

# get list of comments that need replying to
data = db.get_unreplied_haikus()
print data

# close db
db.close()

