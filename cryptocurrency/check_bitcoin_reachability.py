#!/usr/bin/env python3

# Checks if bitcoin node is reachable from outside
# Sends a notification email otherwise

import sys, traceback

import json

from utils.Request import Request
from utils.config import config

SERVICE_ENDPOINT = config().get('bitcoin.reachability', 'service_endpoint')
AWS_ENDPOINT = config().get('bitcoin.reachability', 'aws_endpoint')

def check():
	if is_reachable():
		add_uptime_information_entry()

def is_reachable():
	status = None
	success = False

	try:
		request = Request()
		status = retrieve_status(request)
		success = status['success']
	except ConnectionError as e:
		msg = str(e)

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

def add_uptime_information_entry():
	data = {
		'source': 'lasvegas'
	}
	
	try:
		request = Request()
		result = request.post(AWS_ENDPOINT, data)
		print(result)
	except ConnectionError as e:
		msg = str(e)

if __name__ == '__main__':
	run()
