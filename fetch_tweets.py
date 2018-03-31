#!/usr/bin/python

import tweepy
import json
import sys
import traceback
from tweepy.error import TweepError

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key = ""
consumer_secret = ""

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token = ""
access_token_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

if len(sys.argv) < 3:
	print("You must supply a file containing tweet ids, and the name of the output file.")
	exit(-1)

id_file_name = sys.argv[1]
id_file = open(id_file_name, "r")

out_file = open(sys.argv[2], "w")

for line in id_file:
	done = False
	while not done:
		try:
			splits = line.split("\t")
			id = splits[0]
			tweet = api.get_status(int(id))
			out_file.write(json.dumps(tweet._json) + "\t" + splits[1] + "\t" + splits[2] + "\n")
			done = True
		except TweepError as e:
			if tweepy.error.is_rate_limit_error_message(e):
				print("rate limit exceeded; sleeping...")
				sleep(60 * 15)
			else:
				done = True
				count += 1

id_file.close()
out_file.close()
