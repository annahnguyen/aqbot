import tweepy
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from credentials import *
from datetime import datetime
from threading import Timer

#x = datetime.today()
#y = x.replace(day=x.day+1, hour=1, minute=0, second=0, microsecond=0)
#delta_t = y - x
#t = Timer(secs, )

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

driver = webdriver.Firefox()
driver.get("https://iqair.com/us/usa/oregon/eugene")

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

		if 'air in eugene' in mention.full_text.lower():
			print('found air in eugene')
			print('responding back...')
			aqi = get_aqi(driver)
			api.update_status('@' + mention.user.screen_name + 
				' The AQI is ' + aqi +'. Stay safe!', mention.id)

def get_aqi(driver):
	aq = ''
	driver.refresh()
	value = driver.find_element(By.CLASS_NAME, "aqi-value__value")
	quality = driver.find_element(By.CLASS_NAME, "aqi-status__text")
	aq = value.text + ' (' + quality.text + ')'
	return aq

while True:
	reply_to_tweets()
	time.sleep(20)
