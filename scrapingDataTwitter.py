import os, re, csv
import tweepy

from dotenv import load_dotenv
load_dotenv()

# API keyws twitter
api_key = os.environ['api_key_tw']
api_secrets = os.environ['api_key_secret_tw']
access_token = os.environ['access_token_tw']
access_secret = os.environ['access_token_secret_tw']

# Authenticate to twitter
auth = tweepy.OAuthHandler(api_key,api_secrets)
auth.set_access_token(access_token,access_secret)
api = tweepy.API(auth)
 
try:
    api.verify_credentials()
    print('Successful Authentication')
except:
    print('Failed authentication')

user = api.get_user(screen_name='guardian')

def remove_comma(input_string):
    changed = input_string.replace(",","")
    return changed

def remove_new_line(input_string):
    changed = input_string.replace("\n","")
    return changed

def remove_url(input_string):
    """Remove URLs from a text string"""
    changed = re.sub(r"https\S+", "", input_string)
    return changed

def remove_symbols(input_string):
    regex = re.compile('[^a-zA-Z ]')
    #First parameter is the replacement, second parameter is your input string
    changed = regex.sub('', input_string)
    return changed

def grep_tweets(nickname_twitter, count):
    tweet_list = []
    for tweet in tweepy.Cursor(api.user_timeline, screen_name=nickname_twitter, tweet_mode='extended').items(count):
        #print(f"text: {tweet._json['text']}, created_at: {tweet._json['created_at']}, retweet_count: {tweet._json['retweet_count']}, favorite_count: {tweet._json['favorite_count']}, possibly_sensitive: {str(tweet._json['possibly_sensitive'])}")
        text = remove_comma(tweet._json['full_text'])
        text = remove_new_line(text)
        text = remove_url(text)
        text = remove_symbols(text)
        try:
            tweet_list.append(text + ", " + tweet._json['created_at'] + ", " + str(tweet._json['retweet_count']) + ", " + str(tweet._json['favorite_count']) + ", " + str(tweet._json['possibly_sensitive']))
        except:
            continue
    return tweet_list

def write_csv(csv_file_name, lista):
    csv_file_name = csv_file_name + ".csv"
    with open(csv_file_name, 'w') as csvfile:
        header = ['tweet_text', 'creation_date', 'retweet_count', 'favorite_count', 'possibly_sensitive']
        row = csv.writer(csvfile, delimiter='"')
        row.writerow(header)
        
        for i in lista:
            test_list = [i]
            row.writerow(test_list)
            test_list.clear()

account_list = ['guardian', 'nytimes']

for name in account_list:
    print(f"Scraping tweets from [{name}]")
    tweet_list = grep_tweets(name, 10)
    write_csv(name, tweet_list)