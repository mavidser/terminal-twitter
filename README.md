Terminal Twitter
================
A Twitter CLI for hackers

![](http://sidverma.net/terminal-twitter/images/screenshot.png)

Install
==========

```bash
$ git clone https://github.com/mavidser/terminal-twitter.git
$ cd terminal-twitter
```

_Optional Step:_ It is highly recommended that you replace the keys in `main.py` with your own keys, which you can get by [creating an app on Twitter](https://dev.twitter.com/apps) and setting the permissions to Read/Write.

Now run setup.py file.
```bash
$ python setup.py install
```

_Note:_ Windows users should install colorama for colored output.
```bash
$ pip install colorama 
```

Usage
====

### Display your twitter feed

```bash
$ tt        # Use --no-pager flag if you want the tweets in a 
            # contiuous output instead of a pager.
```

### Display 50 tweets from your twitter feed

```bash
$ tt -n 50  # or $ tt --num 50
```

### Retweet a tweet

```bash
$ tt rt 5  # Retweets the tweet on index 5
```

### Favorite a tweet

```bash
$ tt fav 5  # Favorite the tweet on index 5
```

### Open a tweet in the browser

```bash
$ tt browse 5  # Opens the tweet on index 5
```

### Reply to a tweet

```bash
$ tt reply 5  # Replies to the tweet on index 5. 
              # Use --photo flag to reply with a photo.
```

### Compose a tweet

```bash
$ tt compose
```

### Compose a tweet containing an image

```bash
$ tt compose --photo # Insert filename/path to the picture when prompted.
                     # Alternatively, drag the picture in the terminal when prompted.
```

### Display help
```bash
$ tt --help
```
