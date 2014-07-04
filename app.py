#!/usr/bin/env python
from keys import *
import webbrowser
import tweepy
import cPickle

USER_FILE = 'user.pkl'
try:
	with open(USER_FILE, 'r') as f:
	  access_token = cPickle.load(f)
	  auth = tweepy.OAuthHandler(API_KEY, API_SECRET,'https://sidverma.net/tt/callback')
	  auth.set_access_token(access_token.key, access_token.secret)
except:
	auth = tweepy.OAuthHandler(API_KEY, API_SECRET,'https://sidverma.net/tt/callback')
	try:
	  redirect_url = auth.get_authorization_url()
	except tweepy.TweepError:
	  print 'Error! Failed to get request token.'
	print redirect_url
	verifier = raw_input('Verifier:')
	try:
	  auth.get_access_token(verifier)
	  with open(USER_FILE, 'wb') as f:
	    cPickle.dump(auth.access_token, f, cPickle.HIGHEST_PROTOCOL)
	except tweepy.TweepError:
	  print 'Error! Failed to get access token.'

api = tweepy.API(auth)