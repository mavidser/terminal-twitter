#!/usr/bin/env python

from sys import platform as OPERATING_SYSTEM
import errno
import tweepy
import cPickle
import click
import os

USER_FILE = 'user.pkl'
TWEETS_FILE = 'tweets.pkl'
CONFIG_FILE = 'config.pkl'

#Defaults
DEFAULT_API_KEY = 'UN5oKvd5GRVmhc8n5TaOCtqtJ'
DEFAULT_API_SECRET = 'ZRTv5uWfu3zObcJg1d3dEQbibUtCfU89UAk6Gc5cyX92ivqlO5'

def load_config():
  """Load the last saved tweets details file."""
  with open(CONFIG_FILE, 'r') as f:
    return cPickle.load(f)

def set_file_path(path):
  try:
    os.makedirs(path)
  except OSError as e:
    if (e.errno == errno.EEXIST and os.path.isdir(path)) or path == '':
      pass
    else:
      click.secho('Error - %s' %e, fg="red")
  return os.path.join(path,USER_FILE),os.path.join(path,TWEETS_FILE),os.path.join(path,CONFIG_FILE)


path=''
if OPERATING_SYSTEM == "linux" or OPERATING_SYSTEM == "linux2":
  path = os.path.expandvars('$HOME/.local/share/terminal-twitter/')
elif OPERATING_SYSTEM == "darwin":
  path = os.path.expandvars('$HOME/Library/Application Support/terminal-twitter/')
elif OPERATING_SYSTEM == "win32":
  path = os.path.expandvars('%APPDATA%/terminal-twitter/')
USER_FILE, TWEETS_FILE, CONFIG_FILE = set_file_path(path)

#Sample Keys
try:
  current_config = load_config()
  API_KEY = current_config['apikey']
  API_SECRET = current_config['apisecret']
  PAGER = current_config['pager']
  if PAGER == 'n' or PAGER == 'N':
    PAGER = False
  else:
    PAGER = True
except Exception,e:
  API_KEY = DEFAULT_API_KEY
  API_SECRET = DEFAULT_API_SECRET
  PAGER = False


@click.group(invoke_without_command=True)
@click.option('--num','-n', default=25, help='The number of tweets to display (should be less than 200). Defaults to 25.', required = False)
@click.option('--pager/--no-pager', default=PAGER, help='Display tweets via pager (less). Defaults to pager.')
@click.pass_context
def main(context,num,pager):
  """A CLI to Twitter with support to display, open and compose tweeets."""
  if context.invoked_subcommand is None:
    get_tweets(num,pager)

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
  auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
  try:
    redirect_url = auth.get_authorization_url()
  except tweepy.TweepError as e:
    click.secho('Error - Failed to get request token. %s' %e, fg="red")
  click.echo('Open this link in your web browser:\n'+redirect_url)
  verifier = raw_input('Enter the displayed PIN: ')
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

def update_status(photo,n=False):
  api = login()
  try:
    if photo:
      photo = click.prompt('Enter the photo path').encode('utf_8')
      photo = photo.strip(' ')
      photo = photo.strip('\'')
      x=open(photo,'r')
      if n:
        reply_to = get_tweet_id(n)
        tweet = click.prompt('Enter the text to go along with the photo',default='@%s' %reply_to['author'])
        if tweet.find('@%s ' %reply_to['author']) >=0:
          pass
        else:
          tweet = '@%s ' %reply_to['author'] + tweet
        api.update_with_media(filename=x.name,status=tweet,file=x,in_reply_to_status_id=reply_to['id'])
      else:
        tweet = click.prompt('Enter the text to go along with the photo',default='')
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
@click.option('--photo', is_flag=True, help="Compose a tweet containing a photo.")
def compose(photo):
  """Composes a tweet."""
  update_status(photo,False)
  
@main.command()
@click.option('--photo', is_flag=True, help="Reply with a tweet containing a photo.")
@click.argument('index',type=int)
def reply(photo,index):
  """Reply to a given tweet."""
  update_status(photo,index)

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
def reset():
  """Logout from the application."""
  try:
    os.remove(USER_FILE)
  except:
    pass
  try:
    os.remove(CONFIG_FILE)
  except:
    pass
  try:
    os.remove(TWEETS_FILE)
  except:
    pass

@main.command()
def logout():
  """Logout from the application."""
  os.remove(USER_FILE)
  click.echo('The user is logged out')

@main.command()
def setup():
  """Set the configurations."""
  if API_KEY == DEFAULT_API_KEY:
    default_apikey='Currently using default'
  else:
    default_apikey='Current: '+API_KEY
  if API_SECRET == DEFAULT_API_SECRET:
    default_apisecret='Currently using default'
  else:
    default_apisecret='Current: '+API_SECRET
    
  click.echo('Leave blank for the current/default settings.')
  apikey = click.prompt('Enter the API key',default=default_apikey)
  apisecret = click.prompt('Enter the API secret',default=default_apisecret)
  pager = ''
  while not(pager == 'y' or pager == 'Y' or pager == 'n' or pager == 'N'):
    pager = click.prompt('Turn on pager?',default="y/N")
  if pager == 'y/N':
    pager = 'N'
  if apikey == 'Currently using default':
    apikey = API_KEY
  if apisecret == 'Currently using default':
    apisecret = API_SECRET
  # auth = load_user()
  # print auth.apikey
  settings = {
    'apikey': apikey,
    'apisecret': apisecret,
    'pager': pager
  }
  try:
    with open(CONFIG_FILE, 'wb') as f:
      cPickle.dump(settings, f, cPickle.HIGHEST_PROTOCOL)
    click.echo('Settings Saved.')
  except Exception as e:
    click.secho('Error - %s' %e, fg="red")

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
