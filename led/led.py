#!/usr/bin/env python3

# Switches LED bar on/off 

import os, sys
import signal
import time

import datetime

from optparse import OptionParser

from ledstrip import LEDStrip 

class GracefulKiller:
	kill_now = False

	def __init__(self):
		signal.signal(signal.SIGINT, self.exit_gracefully)
		signal.signal(signal.SIGTERM, self.exit_gracefully)


	def exit_gracefully(self, signum, frame):
		print('exiting')
		self.kill_now = True

def set_color(strip):
	now = datetime.datetime.now()
	if now.time() < datetime.time(12):
		strip.set_morning_color()
	else:
		strip.set_evening_color()

def run(strip):
	print('running')

if __name__ == '__main__':
	killer = GracefulKiller()
	strip = LEDStrip()

	try:
		set_color(strip)
		while not killer.kill_now:
			run(strip)
			time.sleep(10)

	except Exception as ex:
		print(ex)
		strip.switch_off()

	strip.switch_off()