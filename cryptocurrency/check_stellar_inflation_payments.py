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
ALERT_MSG = config().get('stellar.inflation_payments', 'alert_msg')
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


def check_is_receiving_payments():
	payment = None
	msg = ''

	try:
		payment = get_last_inflation_payment()
	except Exception as e:
		msg += str(e)

	date = None
	days = 0
	amount = 0
	if (payment):
		date = payment.date
		days = days_since_last_payment(date)
		amount = '{0:0.6f}'.format(payment.amount)
		if is_receiving_sufficient_payments(date, amount):
			return

	balance = get_account_balance()
	if (payment):
		msg += ALERT_MSG.format(
			days=days, date=date, amount=amount, balance=balance)
	else:
		msg += 'No payments received so far. Balance: {balance}'.format(
			balance=balance)

	email = Email()
	email.send(ALERT_MSG_SUBJECT, msg, ADDR_TO)

def get_account_balance():
	try:
		account = get_account()
		return account['balance']
	except Exception as e:
		return 0

def get_last_inflation_payment():
	request = Request()
	data = fetch_last_payments(request)
	payments = map_payments(data)
	return last_inflation_payment(payments)

def fetch_last_payments(request):
	data = {}
	url = url_last_payments(ADDRESS)
	result = request.get(url)
	if result:
		data = json.loads(result)
	return data

def last_inflation_payment(payments):
	for payment in payments:
		if (payment.addr_from == INFLATION_DESTINATION):
			return payment

	return None

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

def get_account():
	request = Request()
	data = fetch_account(request)
	return map_account(data)

def fetch_account(request):
	data = {}
	url = url_account(ADDRESS)
	result = request.get(url)
	if result:
		data = json.loads(result)
	return data

def map_account(data):
	mapped = {}
	mapped['balance'] = data['balances'][0]['balance']
	return mapped

def is_receiving_sufficient_payments(date, amount):
	return amount > THRESHOLD_AMOUNT and days_since_last_payment(date) < THRESHOLD_DAYS
	
def days_since_last_payment(date):
	now = datetime.now(timezone.utc)
	return abs((now - date).days)

def url_last_payments(address):
	url = '{endpoint}/accounts/{address}/payments?limit=10&order=desc'
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
