    
#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys
import os
import time
import math
import random

DIRECTORY = os.path.dirname(os.path.abspath(__file__))

DIR_LIB = os.path.join(DIRECTORY, 'lib')
DIR_MEDIA = os.path.join(DIRECTORY, 'media')
if os.path.exists(DIR_LIB):
    sys.path.append(DIR_LIB)

from lib import epd2in13_V2
from PIL import Image, ImageDraw, ImageFont

import logging

WHITE = 255
BLACK = 0

class PriceTicker(object):
    def __init__(self, price_client):
        self.price_client = price_client

        self.WIDTH = 0
        self.HEIGHT = 0
        self.RUNNING = True
        self.IMAGE_MODE = '1' # 1 (1-bit pixels, black and white, stored with one pixel per byte)

        self.init_epd()

    def init_epd(self):
        self.epd = epd2in13_V2.EPD()
        self.epd.init(self.epd.FULL_UPDATE)
        self.epd.Clear(0xFF)

        self.WIDTH = self.epd.height # 250 pixels
        self.HEIGHT = self.epd.width # 122 pixels

    def start(self):
        try:
            #self.display_white()
            #self.wait()
            #self.clear_display()

            #self.display_black()
            #self.wait()
            #self.clear_display()

            self.display_image()
            self.wait()
            self.display_price()
        except Exception as ex:
            logging.error(ex)
            self.stop()
        self.stop()
    
    def stop(self):
        logging.info("shutting down")
        if self.RUNNING:
            self.RUNNING = False
            self.shutdown()

    def shutdown(self):
        self.clear_display()
        self.epd.sleep()

    def display_image(self):
        image = self.load_image()
        image_width, image_height = image.size
        padding_left = int((self.WIDTH - image_width) / 2)

        frame = self.create_frame()
        frame.paste(image, (padding_left,0))    
        
        self.epd.display(self.epd.getbuffer(frame))
 
    def display_white(self):
        frame = Image.new(self.IMAGE_MODE, (self.WIDTH, self.HEIGHT), 255)
        draw = ImageDraw.Draw(frame)

        self.epd.init(self.epd.FULL_UPDATE)
        self.epd.displayPartBaseImage(self.epd.getbuffer(frame))
        self.epd.init(self.epd.PART_UPDATE)

        sec = 0
        increment = 1
        while (sec < 60):
            draw.rectangle((0, 0, self.WIDTH, self.HEIGHT), fill = WHITE)                            
            self.epd.displayPartial(self.epd.getbuffer(frame))
            sec = sec + increment
            time.sleep(increment)

    def display_black(self):
        frame = Image.new(self.IMAGE_MODE, (self.WIDTH, self.HEIGHT), 0)
        draw = ImageDraw.Draw(frame)

        self.epd.init(self.epd.FULL_UPDATE)
        self.epd.displayPartBaseImage(self.epd.getbuffer(frame))
        self.epd.init(self.epd.PART_UPDATE)

        sec = 0
        increment = 1
        while (sec < 60):
            draw.rectangle((0, 0, self.WIDTH, self.HEIGHT), fill = BLACK)                            
            self.epd.displayPartial(self.epd.getbuffer(frame))
            sec = sec + increment
            time.sleep(increment)

    def display_price_with_progress_bar(self):
        font = self.load_font()
        font_size = int(math.ceil(font.size * 1.333)) # points * 1+1/3 = pixels

        frame = self.create_frame()
        draw = ImageDraw.Draw(frame)

        self.epd.init(self.epd.FULL_UPDATE)
        self.epd.displayPartBaseImage(self.epd.getbuffer(frame))
        self.epd.init(self.epd.PART_UPDATE)

        sec = 0
        increment = 1
        price_refresh_interval_in_sec = 60
        progress_bar_color = BLACK
        price = 'N/A'
        while (self.RUNNING):    
            if sec % price_refresh_interval_in_sec == 0:
                price = self.price_client.retrieve_price()

                draw.rectangle((0, 0, self.WIDTH, self.HEIGHT), fill = BLACK)
                draw.text((0, 32), price, font = font, fill = WHITE, align='center')
                #draw.text((8, 32), price, font = font, fill = WHITE)
                
                draw.rectangle((0, 0, self.WIDTH, 2), fill = progress_bar_color)
                progress_bar_color = WHITE if progress_bar_color == BLACK else BLACK                
            else:
                progress = int((self.WIDTH / price_refresh_interval_in_sec) * sec)
                draw.rectangle((0, 0, progress, 2), fill = progress_bar_color)
            
            self.epd.displayPartial(self.epd.getbuffer(frame))

            sec = sec + increment
            time.sleep(increment)
            if sec >= price_refresh_interval_in_sec:
                sec = 0 # reset sec counter

            logging.info(sec)
    
    def display_price(self):
        font = self.load_font()
        font_size = int(math.ceil(font.size * 1.333)) # points * 1+1/3 = pixels

        frame = self.create_frame()
        draw = ImageDraw.Draw(frame)

        self.clear_display()

        sec = 0
        increment = 1
        price_refresh_interval_in_sec = 300
        price = 'N/A'
        while (self.RUNNING):
            if sec % price_refresh_interval_in_sec == 0:
                self.clear_display()

                color_bg = self.get_random_color()
                draw.rectangle((0, 0, self.WIDTH, self.HEIGHT), fill = color_bg)

                color_text = WHITE if color_bg == BLACK else BLACK
                price = self.price_client.retrieve_price()

                x = random.randint(0, 64)
                y = random.randint(0, height - font_size)
                logging.info('x: %s y: %s', x, y)
                draw.text((x, y), price, font = font, fill = color_text, align='left')

                self.epd.display(self.epd.getbuffer(frame))
                self.epd.sleep()
            
            sec = sec + increment
            time.sleep(increment)
            if sec >= price_refresh_interval_in_sec:
                sec = 0 # reset sec counter

            logging.info(sec)

    def get_random_color(self):
        r = random.randint(0, 1)
        return WHITE if k == 1 else BLACK   

    def create_frame(self):
        return Image.new(self.IMAGE_MODE, (self.WIDTH, self.HEIGHT))

    def wait(self):
        time.sleep(3)

    def clear_display(self):
        self.epd.init(self.epd.FULL_UPDATE)
        self.epd.Clear(0xFF)

    def load_image(self):
        try:
            image_file_name = 'bitcoin122x122_b.bmp'
            return Image.open(os.path.join(DIR_MEDIA, image_file_name))
        except IOError as e:
            logging.error(e)    

    def load_font(self):
        try:
            font_file_name = 'UbuntuBoldItalic-Rg86.ttf'
            font_file = os.path.join(DIR_MEDIA, font_file_name)
            FONT_SIZE_IN_POINTS = 48 # 48 points = 64 pixels
            return ImageFont.truetype(font_file, FONT_SIZE_IN_POINTS)
        except IOError as e:
            logging.error(e)