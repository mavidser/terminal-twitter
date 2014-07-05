#!/usr/bin/env python

from keys import *
import webbrowser
import tweepy
import cPickle
import click
import os

USER_FILE = 'user.pkl'
TWEETS_FILE = 'tweets.pkl'

@click.group(invoke_without_command=True)
@click.option('--num','-n', default=25, help='The number of tweets to display (should be less than 200). Defaults to 25.', required = False)
@click.option('--pager/--no-pager', default=True, help='Display tweets via pager (less). Defaults to pager.')
@click.pass_context
def main(context,n,pager):
  """A CLI to Twitter with support to display, open and compose tweeets."""
  if context.invoked_subcommand is None:
    get_tweets(n,pager)

def login():
  """Authenticate and save the user."""
  try:
    auth=load_user()
  except:
    auth = save_user()
  return tweepy.API(auth)
  
def load_user():
  """Load the user authentication details file."""
  with open(USER_FILE, 'r') as f:
    return cPickle.load(f)

def save_user():
  """Save the user authentication details in a file."""
  auth = tweepy.OAuthHandler(API_KEY, API_SECRET,'http://sidverma.net/tt/callback')
  try:
    redirect_url = auth.get_authorization_url()
  except tweepy.TweepError:
    click.secho('Error - Failed to get request token.', fg="red")
  print redirect_url
  verifier = raw_input('Verifier:')
  try:
    auth.get_access_token(verifier)
    with open(USER_FILE, 'wb') as f:
      cPickle.dump(auth, f, cPickle.HIGHEST_PROTOCOL)
  except tweepy.TweepError:
    click.secho('Error - Failed to get access token.', fg="red")
  return auth

def load_tweets():
  """Load the last saved tweets details file."""
  with open(TWEETS_FILE, 'r') as f:
    return cPickle.load(f)

def save_tweets(tweets):
  """Save the user loaded tweets in a file."""
  with open(TWEETS_FILE, 'wb') as f:
    cPickle.dump(tweets, f, cPickle.HIGHEST_PROTOCOL)

def get_tweet_id(n):
  """Get the twitter id of a tweet, when supplied with the index."""
  tweets = load_tweets();
  tweet = tweets[n-1]
  return {'author':tweet.author.screen_name,'id':tweet.id}

def print_home_timeline(tweets,pager):
  """Print the home timeline of the user."""
  s=""
  for i,tweet in enumerate(tweets):  
    s += ((click.style('[%d] ' %(i+1), bold=True, fg="blue") + 
           click.style('@%s - ' %tweet.author.screen_name, bold=True, fg="cyan") + 
           click.style('%s' %tweet.text)).encode('utf_8')+'\n\n')
  if pager:
    click.echo_via_pager(s)
  else:
    click.echo(s)

def update_status(media,n=False):
  api = login()
  try:
    if media:
      media = click.prompt('Enter the media path').encode('utf_8')
      media = media.strip(' ')
      media = media.strip('\'')
      x=open(media,'r')
      if n:
        reply_to = get_tweet_id(n)
        tweet = click.prompt('Enter the text to go along with the media',default='@%s' %reply_to['author'])
        if tweet.find('@%s ' %reply_to['author']) >=0:
          pass
        else:
          tweet = '@%s ' %reply_to['author'] + tweet
        api.update_with_media(filename=x.name,status=tweet,file=x,in_reply_to_status_id=reply_to['id'])
      else:
        tweet = click.prompt('Enter the text to go along with the media',default='')
        api.update_with_media(filename=x.name,status=tweet,file=x)        
    else:
      if n:
        reply_to = get_tweet_id(n)
        tweet = click.prompt('Enter the reply to @%s'%reply_to['author'])
        if tweet.find('@%s ' %reply_to['author']) >=0:
          pass
        else:
          tweet = '@%s ' %reply_to['author'] + tweet
        api.update_status(status=tweet,in_reply_to_status_id=reply_to['id'])
      else:
        tweet = click.prompt('Enter the tweet')
        api.update_status(tweet)
    click.echo('Your tweet has been published')
  except Exception as e:
    click.secho('Error - %s' %e, fg="red")

@main.command()
@click.option('--media', is_flag=True, help="Compose a tweet containing a media.")
def compose(media):
  """Composes a tweet."""
  update_status(media,False)
  
@main.command()
@click.option('--media', is_flag=True, help="Reply with a tweet containing a media.")
@click.argument('index',type=int)
def reply(media,index):
  """Reply to a given tweet."""
  update_status(media,index)

@main.command()
@click.argument('index',type=int)
def rt(index):
  """Retweet a given tweet."""
  api = login()
  id=get_tweet_id(index)['id']
  try:
    api.retweet(id)
    click.echo('Retweeted')
  except Exception as e:
    click.secho('Error - %s' %e, fg="red")
  
@main.command()
@click.argument('index',type=int)
def fav(index):
  """Favorite a tweet."""
  api = login()
  id=get_tweet_id(index)['id']
  try:
    api.create_favorite(id)
    click.echo('Marked as Favorite')
  except Exception as e:
    click.secho('Error - %s' %e, fg="red")

@main.command()
@click.argument('index',type=int)
def browse(index):
  """Opens the tweet in web browser."""
  details = get_tweet_id(index)
  link = 'http://twitter.com/%s/status/%d' %(details['author'], details['id'])
  try:
    click.launch(link)
    click.echo('Opening link %s' %link)
  except Exception as e:
    click.secho('Error - %s' %e, fg="red")

@main.command()
def logout():
  """Logout from the application."""
  os.remove('USER_FILE')
  click.echo('The user is logged out')

def get_tweets(n,pager):
  """Display the user's Twiter feed."""
  api = login()
  try:
    tweets = api.home_timeline(count=n)
    save_tweets(tweets)
    print_home_timeline(tweets,pager)
  except Exception as e:
    click.secho('Error - %s' %e, fg="red")

if __name__ == '__main__':
  main()
