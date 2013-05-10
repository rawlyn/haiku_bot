
import praw
import user # not in repo, used to store reddit user agent details

import haiku
import db

import time


db.init()

def main():
	print "fetching reddit comments..."
	
	# create an agent
	agent = praw.Reddit(user_agent=user.agent)
	agent.login(user.name, user.password)
	
	# read comments
	comments = agent.get_subreddit(user.subreddits).get_comments(limit=user.limit)
	
	# search for haikus
	print "looking for haikus..."
	
	for comment in comments:
		comment_body = comment.body
		comment_url = comment.permalink
		
		print "."
		comment_haiku = haiku.get_haiku(comment_body)
		
		if comment_haiku != "":
			print "-" * 17
			
			print "url: {0}".format(comment_url)
			print comment_haiku
			
			# store haiku to database
			db.store_comment_haiku(comment_url, comment_haiku)
			
			print "-" * 17
	
	
	# get list of comments that need replying to
	data = db.get_unreplied_haikus()
	
	# reply to haiku comments
	for row in data:
		comment_url = row["comment_url"]
		comment_haiku = row["comment_haiku"]
		
		formatted_haiku = comment_haiku.replace("\n", "\n\n")
		
		full_reply = """
*Your comment can be read as a (dodgy) haiku!*
	
***

{0}

***

*^Did ^I ^screw ^up? [^Let ^me ^know!](http://www.reddit.com/message/compose/?to={1}&subject=You%20screwed%20up%21)*"""
		full_reply = full_reply.format(formatted_haiku, user.name)
		
		print "-" * 17
		print "replying to {0}".format(comment_url)
		print "-" * 17
		
		comment = agent.get_submission(comment_url).comments[0]
		#comment.reply(full_reply)
		
		time.sleep(2)
		
		db.mark_as_replied(comment_url)
	
if __name__ == "__main__":
	main()
	
