
import praw
import user # not in repo, used to store reddit user agent details

import haiku
import db

import time


db.init()

def main():
	time_start = time.time()
	haiku_count = 0
	total_count = 0
	
	print "fetching reddit comments..."
	
	# create an agent
	agent = praw.Reddit(user_agent=user.agent)
	agent.login(user.name, user.password)
	
	# read comments
	comments = agent.get_subreddit(user.subreddits).get_comments(limit=user.limit)
	
	# search for haikus
	print "looking for haikus..."
	
	for comment in comments:
		total_count += 1
		
		comment_body = comment.body
		comment_haiku = haiku.get_haiku(comment_body)
		
		if comment_haiku != "":
			print "-" * 17
			
			comment_url = comment.permalink
			
			print "url: {0}".format(comment_url)
			print comment_haiku
			
			# store haiku to database
			db.store_comment_haiku(comment_url, comment_haiku)
			
			print "-" * 17
			
			haiku_count += 1
			
			time.sleep(1)
	
	# get list of comments that need replying to
	data = db.get_unreplied_haikus()
	
	reply_success_count = 0
	reply_total_count = 0
	
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
		
		comment = agent.get_submission(comment_url).comments[0]
		
		reply_total_count += 1
		
		try:
			comment.reply(full_reply)
			db.mark_as_replied(comment_url)
			print "success"
			reply_success_count +=1
		except praw.errors.RateLimitExceeded, e:
			print "failed ({0})".format(e.message)
		
		print "-" * 17
		
		time.sleep(2)
		
	time_end = time.time()
	time_total = time_end - time_start
	
	comments_per_sec = int(total_count / time_total)
	
	print "#" * 68
	
	print "{0} / {1} comments were haikus".format(haiku_count, total_count)
	print "took {0} seconds".format(time_total)
	print "~{0} comments/second".format(comments_per_sec)
	print "{0} / {1} replies sent".format(reply_success_count, reply_total_count)
	
	print "#" * 68
	
	
if __name__ == "__main__":
	main()
	
