import tweepy
import time

CONSUMER_KEY = 'l5C8MuU5eR8fzXsr1Gzimhj56'
CONSUMER_SECRET = 'I2J0HiTHJYtY8Zy1Onqi1pf2AiKInaE4HvTpXWwmY6WwsKXDwg'
ACCESS_KEY = '1311317261160857601-I0BAoKPSi47EK1zGfjRgqkrFscAdhU'
ACCESS_SECRET = 'EYCkVPThZmnl9erEb0NCCeVGnj84wIA46YW0bljK6JhOW'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME = 'last_id.txt'

def retrieve_last_id(file_name):
    f_read = open(file_name, 'r')
    last_id = int(f_read.read().strip())
    f_read.close()
    return last_id

def store_last_id(last_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_id))
    f_write.close()
    return

def reply_to_tweets():
	print('retrieving and replying to tweets...')
	last_id = retrieve_last_id(FILE_NAME)
	mentions = api.mentions_timeline(last_id, tweet_mode='extended')

	for mention in reversed(mentions):
		print(str(mention.id) + ' - ' + mention.full_text)
		last_id = mention.id
		store_last_id(last_id, FILE_NAME)

		if '#helloworld' in mention.full_text.lower():
			print('found #helloworld!')
			print('responding back...')
			api.update_status('@' + mention.user.screen_name + 
				' hello world back to you!', mention.id)

while True:
	reply_to_tweets()
	time.sleep(15)
