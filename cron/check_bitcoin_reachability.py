#!/usr/bin/env python3

# Checks if bitcoin is reachable from outside
# Sends a notification email otherwise

import sys, traceback

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
import json

SERVICE_ENDPOINT = 'https://bitnodes.earn.com/api/v1/nodes/me-8333/'

FROM_ADDR = 'from@gmail.com'
FROM_PWD = 'password'
SMTP_ENDPOINT = 'smtp.gmail.com'
SMTP_PORT = 587

TO_ADDR = 'to@gmail.com'
ALERT_MESSAGE = 'Alert: Bitcoin node not reachable'

def checkIsReachable():
	status = retrieveStatus()
	success = status['success']

	if success:
		return
	
	sendEmail(json.dumps(status))

def retrieveStatus():
	r = requests.get(SERVICE_ENDPOINT)
	return r.json()

def sendEmail(message):
	msg = MIMEMultipart()
	msg['From'] = FROM_ADDR
	msg['To'] = TO_ADDR
	msg['Subject'] = ALERT_MESSAGE
	msg.attach(MIMEText(message, 'plain'))

	server = smtplib.SMTP(SMTP_ENDPOINT, SMTP_PORT)
	server.ehlo
	server.starttls()
	server.login(FROM_ADDR, FROM_PWD)
	text = msg.as_string()
	server.sendmail(FROM_ADDR, TO_ADDR, text)
	server.quit()

def run():
	try:
		checkIsReachable()
	except:
		traceback.print_exc(file=sys.stdout)
		sys.exit(0)

if __name__ == '__main__':
	run()
