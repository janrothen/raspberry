#!/usr/bin/env python3

# Checks if bitcoin node is reachable from outside
# Sends a notification email otherwise

import sys, traceback

import json

from utils.Email import Email
from utils.Request import Request
from utils.config import config

ALERT_MSG_SUBJECT = config().get('bitcoin.reachability', 'alert_msg_subject')
SERVICE_ENDPOINT = config().get('bitcoin.reachability', 'service_endpoint')
ADDR_TO = config().get('email', 'addr_to')

def check():
	if is_reachable():
		return

	email = Email()
	email.send(ALERT_MSG_SUBJECT, msg, ADDR_TO)

def is_reachable():
	status = None
	success = False
	msg = None

	try:
		request = Request()
		status = retrieve_status(request)
		success = status['success']
	except ConnectionError as e:
		msg = str(e)
	except KeyError:
		msg = json.dump(status)

	return success

def retrieve_status(request):
	data = {}
	result = request.get(SERVICE_ENDPOINT)
	if result:
		data = json.loads(result)
	return data

def run():
	try:
		check()
	except:
		traceback.print_exc(file=sys.stdout)
		sys.exit(0)

if __name__ == '__main__':
	run()
