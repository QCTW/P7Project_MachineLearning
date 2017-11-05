'''
Code reference:
https://thomassileo.name/blog/2013/01/25/using-twitter-rest-api-v1-dot-1-with-python/
'''
from __future__ import unicode_literals
from requests_oauthlib import OAuth1
from urlparse import parse_qs

import sys, getopt
import requests
import twitter_oauth

REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

def setup_oauth():
    """Authorize your app via identifier."""
    # Request token
    toauth = twitter_oauth.TwitterOauth("oauth.key")
    oauth = OAuth1(toauth.get_consumer_key(), client_secret=toauth.get_consumer_secret())
    r = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)

    resource_owner_key = credentials.get('oauth_token')[0]
    resource_owner_secret = credentials.get('oauth_token_secret')[0]

    # Authorize
    authorize_url = AUTHORIZE_URL + resource_owner_key
    print 'Please go here and authorize: ' + authorize_url

    verifier = raw_input('Please input the verifier: ')
    oauth = OAuth1(toauth.get_consumer_key(),
                   client_secret=toauth.get_consumer_secret(),
                   resource_owner_key=resource_owner_key,
                   resource_owner_secret=resource_owner_secret,
                   verifier=verifier)

    # Finally, Obtain the Access Token
    r = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)
    token = credentials.get('oauth_token')[0]
    secret = credentials.get('oauth_token_secret')[0]
    return token, secret


def get_oauth():
    toauth = twitter_oauth.TwitterOauth("oauth.key")
    oauth = OAuth1(toauth.get_consumer_key(), client_secret=toauth.get_consumer_secret(), resource_owner_key=toauth.get_oauth_token(), resource_owner_secret=toauth.get_oauth_token_secret())
    return oauth

if __name__ == "__main__":
    oauth = get_oauth()
    argv = sys.argv[1:]
    try:
      opts, args = getopt.getopt(argv,"hn:o:",["name=","output="])
    except getopt.GetoptError:
      print 'data_puller.py -n <twitter_screen_name> -o <output_file>'
      sys.exit(2)
    
    t_screen_name = "realDonaldTrump"
    outputfile = t_screen_name+".csv"
    for opt, arg in opts:
      if opt == '-h':
        print 'data_puller.py -n <twitter_screen_name> -o <output_file>'
        sys.exit()
      elif opt in ("-n", "--name"):
        t_screen_name = arg
      elif opt in ("-o", "--output"):
        outputfile = arg
    
    r = requests.get(url="https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name="+t_screen_name, auth=oauth)
    f = open(outputfile, 'w')
    if(r.status_code == 200):
	data = r.json()
	for e in data:
		txt = e['text']+"\n"
		f.write(txt.encode('utf-8'))
		print (e['text'])
    f.close()
