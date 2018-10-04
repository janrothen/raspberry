#!/usr/bin/env python3

# Checks if stellar lumens address is receiving inflation payments
# Sends a notification email otherwise

import sys, traceback
import json

from datetime import datetime, timedelta, timezone
from dateutil import parser

from utils import email
from utils.config import config
from utils.apicall import perform_request

ALERT_MSG_SUBJECT = config().get('stellar.inflation_payments', 'alert_msg_subject')
ALERT_MSG = config().get('stellar.inflation_payments', 'alert_msg')
ADDRESS = config().get('stellar.inflation_payments', 'address')
SERVICE_ENDPOINT = config().get('stellar.inflation_payments', 'service_endpoint')
THRESHOLD_DAYS = config().getint('stellar.inflation_payments', 'threshold_days')
THRESHOLD_AMOUNT = config().getint('stellar.inflation_payments', 'threshold_amount')
ADDR_TO = config().get('email', 'addr_to')

def check_is_receiving_payments():
	msg = ''
	payment = {}
	account = {}

	try:
		data = fetch_last_payment()
		payment = map_payment(data)
	except Exception as e:
		msg += str(e)

	try:
		data = fetch_account()
		account = map_account(data)
	except Exception as e:
		msg += str(e)

	date = payment['date']
	amount = payment['amount']
	if is_receiving_sufficient_payments(date, amount):
		return

	days = days_since_last_payment(date)
	balance = account['balance']
	amount = '{0:0.6f}'.format(amount)
	msg = ALERT_MSG.format(
		days=days,
		date=date,
		amount=amount,
		balance=balance)

	email.send_email(ALERT_MSG_SUBJECT, msg, ADDR_TO)

def fetch_last_payment():
	data = {}
	url = url_last_payment(ADDRESS)
	result = perform_request('GET', url)
	if result:
		data = json.loads(result)
	return data

def fetch_account():
	data = {}
	url = url_account(ADDRESS)
	result = perform_request('GET', url)
	if result:
		data = json.loads(result)
	return data

def map_payment(data):
	trx = data['_embedded']['records'][0]
	mapped = {}
	mapped['date'] = parser.parse(trx['created_at'])
	mapped['amount'] = float(trx['amount'])
	mapped['from'] = trx['from']
	return mapped

def map_account(data):
	mapped = {}
	mapped['balance'] = data['balances'][0]['balance']
	return mapped

def is_receiving_sufficient_payments(date, amount):
	return amount > THRESHOLD_AMOUNT and days_since_last_payment(date) < THRESHOLD_DAYS
	
def days_since_last_payment(date):
	now = datetime.now(timezone.utc)
	return abs((now - date).days)

def url_last_payment(address):
	url = '{endpoint}/accounts/{address}/payments?limit=1&order=desc'
	url = url.format(
		endpoint=SERVICE_ENDPOINT,
		address=address)
	return url

def url_account(address):
	url = '{endpoint}/accounts/{address}'
	url = url.format(
		endpoint=SERVICE_ENDPOINT,
		address=address)
	return url

def run():
	try:
		check_is_receiving_payments()
	except:
		traceback.print_exc(file=sys.stdout)
		sys.exit(0)

if __name__ == '__main__':
	run()
