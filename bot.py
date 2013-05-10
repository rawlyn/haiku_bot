
import praw
import user # not in repo, used to store reddit user agent details

import haiku
import db

db.init()


print "fetching reddit comments..."

# create an agent
agent = praw.Reddit(user_agent=user.agent)
agent.login(user.name, user.password)

# read comments
comments = agent.get_subreddit(user.subreddits).get_comments(limit=user.limit)


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


# get list of comments that need replying to
data = db.get_unreplied_haikus()

# reply to haiku comments
for row in data:
	comment_id = row["comment_id"]
	comment_haiku = row["comment_haiku"]
	
	formatted_haiku = comment_haiku.replace("\n", "\n\n")
	
	full_reply = """
*Your comment appears to be expressible as a haiku!*

***

{0}

***

*^Did ^I ^screw ^up? [^Let ^me ^know!](http://www.reddit.com/message/compose/?to={1}&subject=You%20screwed%20up%21)*
	""".format(formatted_haiku, user.name)
	
	print "#{0}#".format(full_reply)
	

