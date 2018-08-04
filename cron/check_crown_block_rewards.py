#!/usr/bin/env python3

# Checks if crown master node is receiving block rewards
# Sends a notification email otherwise

import sys, traceback
import json

from datetime import datetime, timedelta, timezone
from dateutil import parser

from utils import email
from utils.config import config
from utils.apicall import perform_request

ALERT_MSG_SUBJECT = config().get('crown.block_rewards', 'alert_msg_subject')
ALERT_MSG = config().get('crown.block_rewards', 'alert_msg')
ADDRESS = config().get('crown.block_rewards', 'address')
SERVICE_ENDPOINT = config().get('crown.block_rewards', 'service_endpoint')
SERVICE_API_KEY = config().get('crown.block_rewards', 'service_api_key')
THRESHOLD_DAYS = config().getint('crown.block_rewards', 'threshold_days')
ADDR_TO = config().get('email', 'addr_to')

def check_is_receiving_rewards():
	msg = None
	mapped = {}

	try:
		data = fetch_data()
		mapped = map_data(data)
	except Exception as e:
		msg = str(e)
	
	date = mapped['date']
	if is_receiving_rewards(date):
		return

	days = days_since_last_reward(date)
	balance = mapped['balance']
	msg = ALERT_MSG.format(
		days=days,
		date=date,
		balance=balance)	

	email.send_email(ALERT_MSG_SUBJECT, msg, ADDR_TO)
	
def fetch_data():
	data = {}
	url = '{endpoint}?q=multiaddr&key={key}&active={address}'
	url = url.format(
		endpoint=SERVICE_ENDPOINT,
		key=SERVICE_API_KEY,
		address=ADDRESS)
	result = perform_request('GET', url)
	if result:
		data = json.loads(result)
	return data

def map_data(data):
	mapped = {}
	mapped['date'] = map_date_of_last_reward(data)
	mapped['balance'] = map_balance(data)
	return mapped

def map_date_of_last_reward(data):
	date = data['txs'][0]['time_utc']
	return parser.parse(date)

def map_balance(data):
	balance = data['addresses'][0]['final_balance']
	return str(balance/100000000)

def is_receiving_rewards(date):
	return days_since_last_reward(date) < THRESHOLD_DAYS
	
def days_since_last_reward(date):
	now = datetime.now(timezone.utc)
	return abs((now - date).days)

def run():
	try:
		check_is_receiving_rewards()
	except:
		traceback.print_exc(file=sys.stdout)
		sys.exit(0)

if __name__ == '__main__':
	run()
