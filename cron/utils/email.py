import os
import sys, traceback

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from utils.config import config

ADDR_TO = config().get('email', 'addr_to')
ADDR_FROM = config().get('email', 'addr_from')
SMTP_ENDPOINT = config().get('email', 'smtp_endpoint')
SMTP_PORT = config().get('email', 'smtp_port')
PWD = config().get('email', 'pwd')

def send_email(subject, message):
	msg = MIMEMultipart()
	msg['From'] = ADDR_TO
	msg['To'] = ADDR_FROM
	msg['Subject'] = subject
	msg.attach(MIMEText(message,_subtype='plain'))

	server = smtplib.SMTP(SMTP_ENDPOINT, SMTP_PORT)
	server.ehlo
	server.starttls()
	server.login(ADDR_FROM, PWD)
	text = msg.as_string()
	server.sendmail(ADDR_FROM, ADDR_TO, text)
	server.quit()
