#!/usr/bin/env python3

# Checks if bitcoin node is reachable from outside
# Sends a notification email otherwise

import sys, traceback

import requests
import json

from utils import email
from utils.config import config

ALERT_MSG_SUBJECT = config().get('bitcoin.reachability', 'alert_msg_subject')
SERVICE_ENDPOINT = config().get('bitcoin.reachability', 'service_endpoint')
ADDR_TO = config().get('email', 'addr_to')

def check_is_reachable():
	status = retrieve_status()
	success = status['success']

	if success:
		return
	
	email.send_email(ALERT_MSG_SUBJECT, json.dumps(status), ADDR_TO)

def retrieve_status():
	r = requests.get(SERVICE_ENDPOINT)
	return r.json()

def run():
	try:
		check_is_reachable()
	except:
		traceback.print_exc(file=sys.stdout)
		sys.exit(0)

if __name__ == '__main__':
	run()
