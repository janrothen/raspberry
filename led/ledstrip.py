#!/usr/bin/env python3

import os, sys

import re
import time
from time import sleep

from random import randint

from utils.config import config

R = 'red'
G = 'green'
B = 'blue'

PIN_RED = config().getint('pins', R)
PIN_GREEN = config().getint('pins', G)
PIN_BLUE = config().getint('pins', B)

PROFILE_MORNING = 'profile.morning'
PROFILE_EVENING = 'profile.evening'

MAX_CV = 255
MIN_CV = 0

class LEDStrip(object):
	def __init__(self):
		self._r = 0.0
		self._g = 0.0
		self._b = 0.0

		self._interrupt = False
		self._sequence = None

	def set_morning_color(self):
		self.fade_in(PROFILE_MORNING)

	def set_evening_color(self):
		self.fade_in(PROFILE_EVENING)

	def fade_in(self, profile_name):
		c = self.get_profile_color(profile_name)
		self.fade_to_rgb(*c, 30000)

	def change_colors_randomly(self):
		red = randint(MIN_CV, MAX_CV)
		green = randint(MIN_CV, MAX_CV)
		blue = randint(MIN_CV, MAX_CV)
		self.set_rgb(red, green, blue)
	
	def run_sequence(self, func, *args, **kwargs):
		self.stop_current_sequence()
		self.start_sequence(func, args, kwargs)

	def start_sequence(self, func, *args, **kwargs):
		self._sequence = threading.Thread(target=func, args=args, kwargs=kwargs)
		self._interrupt = False
		self._sequence.start()

	def stop_current_sequence(self, timeout=60):
		self.interrupt()
		try:
			self._sequence._sequence_stop_signal = True
			self._sequence.join(timeout)
		except AttributeError:
			pass
		
		self.reset_sequence()

	#region Sequences
	def fade_to_rgb(self, r=0, g=0, b=0, fade=1000):
		r_start = self._r
		g_start = self._g
		b_start = self._b

		r_diff = r - self._r
		g_diff = g - self._g
		b_diff = b - self._b

		steps = int(float(fade) / 20.0) #50Hz = 20 milliseconds

		for step in range(0, steps):
			increment = float(step) / steps
			r_c = r_start + (r_diff * increment)
			g_c = g_start + (g_diff * increment)
			b_c = b_start + (b_diff * increment)
			self.set_rgb(r_c, g_c, b_c)
			sleep(0.02) #20ms
			if self._interrupt:
				break

		return self.set_rgb(r, g, b)

	def switch_on(self):
		self.interrupt()
		self.fade_to_rgb(MAX_CV, MAX_CV, MAX_CV, 1000)

	def switch_off(self):
		self.interrupt()
		self.fade_to_rgb(MIN_CV, MIN_CV, MIN_CV, 1000)

	def set_rgb(self, red, green, blue):
		msg = '{0:5.2f} {1:5.2f} {2:5.2f}'.format(red, green, blue)
		print(msg)
		self.set_red_value(red)
		self.set_green_value(green)
		self.set_blue_value(blue)

	#region Private basic
	def interrupt(self):
		self._interrupt = True

	def reset_sequence(self):
		self._sequence = None

	def get_profile_color_value(self, profile, color):
		return config().getint(profile, color)

	def get_profile_color(self, profile):
		r = self.get_profile_color_value(profile, R)
		g = self.get_profile_color_value(profile, G)
		b = self.get_profile_color_value(profile, B)
		return (r, g, b)

	def set_red_value(self, value):
		self._r = value
		self.set_pin_value(PIN_RED, value)

	def set_green_value(self, value):
		self._g = value
		self.set_pin_value(PIN_GREEN, value)

	def set_blue_value(self, value):
		self._b = value
		self.set_pin_value(PIN_BLUE, value)

	def set_pin_value(self, pin, value):
		rounded = int(round(value))
		if rounded < 0:
			rounded = 0
		if rounded > MAX_CV:
			rounded = MAX_CV

		command = 'pigs p {} {}'.format(pin, rounded)
		os.system(command)
	#endregion