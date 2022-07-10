from dotenv import load_dotenv
import os
import sys
import requests
import tweepy


load_dotenv()
# API keyws that yous saved earlier
api_key = os.environ['api_key_tw']
api_secrets = os.environ['api_key_secret_tw']
access_token = os.environ['access_token_tw']
access_secret = os.environ['access_token_secret_tw']

# Authenticate to Twitter
auth = tweepy.OAuthHandler(api_key,api_secrets)
auth.set_access_token(access_token,access_secret)
 
api = tweepy.API(auth)
 
try:
    api.verify_credentials()
    print('Successful Authentication')
except:
    print('Failed authentication')