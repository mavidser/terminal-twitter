#!/usr/bin/env python
from keys import *
import webbrowser
import tweepy
import cPickle
import click

USER_FILE = 'user.pkl'

def save_user():
	auth = tweepy.OAuthHandler(API_KEY, API_SECRET,'http://sidverma.net/tt/callback')
	try:
	  redirect_url = auth.get_authorization_url()
	except tweepy.TweepError:
	  print 'Error! Failed to get request token.'
	print redirect_url
	verifier = raw_input('Verifier:')
	try:
	  auth.get_access_token(verifier)
	  with open(USER_FILE, 'wb') as f:
	    cPickle.dump(auth, f, cPickle.HIGHEST_PROTOCOL)
	except tweepy.TweepError:
	  print 'Error! Failed to get access token.'
	return auth

def main():
	try:
		with open(USER_FILE, 'r') as f:
		  auth = cPickle.load(f)
	except:
		auth = save_user()
	api = tweepy.API(auth)

if __name__ == '__main__':
  main()

