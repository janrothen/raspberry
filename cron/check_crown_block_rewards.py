#!/usr/bin/env python3

# Checks if bitcoin is reachable from outside
# Sends a notification email otherwise

import sys, traceback

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

from datetime import datetime, timedelta
from dateutil import parser

from utils import email
from utils.config import config

ALERT_MSG_SUBJECT = config().get('crown.block_rewards', 'alert_msg_subject')
ALERT_MSG = config().get('crown.block_rewards', 'alert_msg')
ADDRESS = config().get('crown.block_rewards', 'address')
BLOCK_EXPLORER_URL = config().get('crown.block_rewards', 'block_explorer_url')
XPATH_TO_LAST_TRX_DATE = config().get('crown.block_rewards', 'xpath_to_last_trx_date')
THRESHOLD_DAYS = config().getint('crown.block_rewards', 'threshold_days')

def check_is_receiving_rewards():
	success = False
	date = None
	msg = None
	try:
		date = fetch_date_of_last_trx()
		if is_receiving_rewards(date):
			print('receving')
			success = True
		else:
			days = abs((datetime.today() - date).days)
			msg = ALERT_MSG.format(days=days, date=date)
	except NoSuchElementException as e:
		msg = str(e)

	if success:
		return

	email.send_email(ALERT_MSG_SUBJECT, msg)
	
def fetch_date_of_last_trx():
	options = Options()
	options.set_headless(headless=True)
	driver = webdriver.Firefox(firefox_options=options, executable_path='/usr/local/bin/geckodriver')

	url_assembled = BLOCK_EXPLORER_URL.format(address=ADDRESS)
	driver.get(url_assembled)

	element = driver.find_element_by_xpath(XPATH_TO_LAST_TRX_DATE)
	date_string = element.get_attribute('innerHTML')
	date = parse_date(date_string)
	return date

def is_receiving_rewards(date_of_last_trx):
	treshold = datetime.today() - timedelta(days=THRESHOLD_DAYS)
	return date_of_last_trx > treshold
	
def parse_date(string):
	#hacky, 18-07-27 13:08:13 is returned instead of 2018-07-27 13:08:13
	#date_string = '20' + string 
	date = parser.parse(string)
	return date

def run():
	try:
		check_is_receiving_rewards()
	except:
		traceback.print_exc(file=sys.stdout)
		sys.exit(0)

if __name__ == '__main__':
	run()
