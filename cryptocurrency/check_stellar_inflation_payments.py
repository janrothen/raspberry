#!/usr/bin/env python3

# Checks if stellar lumens address is receiving inflation payments
# Sends a notification email otherwise

import sys, traceback
import json

from datetime import datetime, timedelta, timezone
from dateutil import parser

from utils.Email import Email
from utils.Request import Request
from utils.config import config

ALERT_MSG_SUBJECT = config().get('stellar.inflation_payments', 'alert_msg_subject')
ALERT_MSG_INSUFFICIENT = config().get('stellar.inflation_payments', 'alert_msg_insufficient')
ALERT_MSG_NONE = config().get('stellar.inflation_payments', 'alert_msg_none')
SERVICE_ENDPOINT = config().get('stellar.inflation_payments', 'service_endpoint')
ADDRESS = config().get('stellar.inflation_payments', 'address')
INFLATION_DESTINATION = config().get('stellar.inflation_payments', 'inflation_dest')
THRESHOLD_DAYS = config().getint('stellar.inflation_payments', 'threshold_days')
THRESHOLD_AMOUNT = config().getint('stellar.inflation_payments', 'threshold_amount')
ADDR_TO = config().get('email', 'addr_to')

class Payment(object):
	def __init__(self):
		self._date = None
		self._amount = 0
		self._from = None

def check_payment():
	payment = get_last_inflation_payment()

	if not is_sufficient(payment):
		email_msg = assemble_msg(payment)
		email = Email()
		email.send(ALERT_MSG_SUBJECT, email_msg, ADDR_TO)

def get_last_inflation_payment():
	try:
		data = fetch_last_payments_data()
		payments = map_payments(data)
		return last_inflation_payment(payments)
	except Exception as e:
		return None

def fetch_last_payments_data():
	data = {}
	url = url_last_payments()

	request = Request()
	result = request.get(url)
	if result:
		data = json.loads(result)
	return data

def map_payments(data):
	transactions = data['_embedded']['records']

	payments = []
	for trx in transactions:
		if (trx['type'] == 'payment'):
			payment = map_payment(trx)
			payments.append(payment)

	return payments

def map_payment(data):
	p = Payment()
	p.date = parser.parse(data['created_at'])
	p.amount = float(data['amount'])
	p.addr_from = data['from']
	return p

def last_inflation_payment(payments):
	filtered = list(filter(lambda p: p.addr_from == INFLATION_DESTINATION, payments))
	if (filtered):
		filtered.sort(key=lambda p: p.date, reverse=False)
		return filtered[0]
	return None

def is_sufficient(payment):
	if (not payment):
		return False

	return payment.amount > THRESHOLD_AMOUNT and days_since_last_payment(payment.date) < THRESHOLD_DAYS

def get_account_balance():
	try:
		account = get_account()
		return account['balance']
	except Exception as e:
		return 0

def get_account():
	data = fetch_account_data()
	return map_account(data)

def fetch_account_data():
	data = {}
	url = url_account()

	request = Request()
	result = request.get(url)
	if result:
		data = json.loads(result)
	return data

def map_account(data):
	mapped = {}
	mapped['balance'] = data['balances'][0]['balance']
	return mapped

def days_since_last_payment(date):
	now = datetime.now(timezone.utc)
	return abs((now - date).days)

def assemble_msg(payment):
	balance = get_account_balance()

	if (payment):
		days = days_since_last_payment(payment.date)
		amount = '{0:0.6f}'.format(payment.amount)
		return ALERT_MSG_INSUFFICIENT.format(
			days=days,
			date=payment.date,
			amount=amount,
			balance=balance)

	return ALERT_MSG_NONE.format(
			balance=balance)

# URLs
def url_last_payments():
	url = '{endpoint}/accounts/{address}/payments?limit={limit}&order=desc'
	url = url.format(
		endpoint=SERVICE_ENDPOINT,
		address=ADDRESS,
		limit=10) # increase if necessary
	return url

def url_account():
	url = '{endpoint}/accounts/{address}'
	url = url.format(
		endpoint=SERVICE_ENDPOINT,
		address=ADDRESS)
	return url

def run():
	try:
		check_payment()
	except:
		traceback.print_exc(file=sys.stdout)
		sys.exit(0)

if __name__ == '__main__':
	run()
