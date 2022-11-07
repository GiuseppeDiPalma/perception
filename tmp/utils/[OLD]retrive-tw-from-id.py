import os, csv
import tweepy
import time

from dotenv import load_dotenv
load_dotenv()

# # API keys twitter
# api_key = os.environ['api_key_tw']
# api_secrets = os.environ['api_key_secret_tw']
# access_token = os.environ['access_token_tw']
# access_secret = os.environ['access_token_secret_tw']

# # Authenticate to twitter
# auth = tweepy.OAuthHandler(api_key,api_secrets)
# auth.set_access_token(access_token,access_secret)
# api = tweepy.API(auth, wait_on_rate_limit=True)

# try:
#     api.verify_credentials()
#     print('Successful Authentication')
# except:
#     print('Failed authentication')

def read_csv(csv_file_name):
    lista_id = []
    lista_type = []
    with open(csv_file_name, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            lista_id.append(row[0])
            lista_type.append(row[1])
    return lista_id, lista_type

def write_csv(csv_file_name, lista):
    csv_file_name = csv_file_name + ".csv"
    with open(csv_file_name, 'w') as csvfile:
        row = csv.writer(csvfile, delimiter='"')
        for i in lista:
            test_list = [i]
            row.writerow(test_list)
            test_list.clear()

def contatenate_two_string(string1, string2):
    return string1 +", "+ string2

client = tweepy.Client(
    bearer_token=os.environ['bearer_token_tw'],
    consumer_key=os.environ['api_key_tw'],
    consumer_secret=os.environ['api_key_tw'],
    access_token=os.environ['access_token_tw'],
    access_token_secret=os.environ['access_token_secret_tw']
)
# find tweet by id
# tweet = client.get_tweet(id=576372440210763777)
# ##extract data from tweet
# text = tweet.data
# print(text)

lista_id, lista_type = read_csv('data/dataset/NAACL_SRW_2016.csv')

# lista_tw = ['575957615760515072', '575957615760515072', '575957615760515072', '575957615760515072']
# lista_type_test = ['0', '1', '0', '1']
tweet_list = []

# print(len(lista_id))
# print(len(lista_type))

# arr_counter = -1
# while(True):
#     for (id, type) in zip(lista_id, lista_type):
#         if (arr_counter+1) != len(lista_id):
#             try:
#                 tweet = client.get_tweet(id=id)
#                 tweet_list.append(id +", "+ str(tweet.data) + ", " + type)
#                 print(tweet.data)
#             except:
#                 tweet_list.append(id +", "+ str(tweet.data) + ", " + type)
#                 print("ERROR: " + id)
#         else:
#             exit()
#         arr_counter += 1
#     #sleep for 16 minutes
#     write_csv('solo_un_test', tweet_list)
#     time.sleep(960)
#     # time.sleep(1)

# API keys twitter
api_key = os.environ['api_key_tw']
api_secrets = os.environ['api_key_secret_tw']
access_token = os.environ['access_token_tw']
access_secret = os.environ['access_token_secret_tw']

# Authenticate to twitter
auth = tweepy.OAuthHandler(api_key,api_secrets)
auth.set_access_token(access_token,access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

for status in tweepy.Cursor(api.search, q=lista_id, monitor_rate_limit=True, wait_on_rate_limit=True).items():
    print(status.text)
try:
    api.verify_credentials()
    print('Successful Authentication')
except:
    print('Failed authentication')

print(api.search_tweets(575957615760515072))
# for (id, type) in zip(lista_id, lista_type):
#     try:
#         tweet = api.get_status(id)
#         # tweet = client.get_tweet(id=id)
#         tweet_list.append(id +", "+ str(tweet.text) + ", " + type)
#         print(tweet.text)
#     except:
#         tweet_list.append("ERROR: " + id + ", " + type)
#         print("ERROR: " + id)
#     write_csv('solo_un_test', tweet_list)